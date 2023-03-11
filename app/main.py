import os
import logging
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from mastodon import Mastodon


class Account(BaseModel):
    # see AccountSerializer for the full list of properties:
    #   https://github.com/mastodon/mastodon/blob/main/app/serializers/rest/admin/account_serializer.rb
    username: str


class Status(BaseModel):
    id: str
    uri: str
    url: str
    account: Account
    in_reply_to_id: Optional[str]
    in_reply_to_account_id: Optional[str]


class Notification(BaseModel):
    id: str
    created_at: str
    type: str
    account: Account
    status: Optional[Status]


class AccountCreatedEvent(BaseModel):
    event: str
    created_at: str
    object: Account


class NotificationEvent(BaseModel):
    notification: dict


load_dotenv()

app = FastAPI()
logger = logging.getLogger("gunicorn.info")


@app.on_event("startup")
def startup_event():
    logger.info(f"Starting up muninn app.")

    app.state.mastodon = Mastodon(
        access_token=os.environ.get("ACCESS_TOKEN"),
        api_base_url=os.environ.get("API_BASE_URL"),
    )
    app.state.instance_name = (os.environ.get("INSTANCE_NAME"),)
    app.state.admin_account_name = (os.environ.get("ADMIN_ACCOUNT_NAME"),)
    app.state.onboarding_link = os.environ.get("ONBOARDING_LINK")

    muninn_listener_url = os.environ.get("MUNINN_LISTENER_URL")
    private_key, public_key = app.state.mastodon.push_subscription_generate_keys()
    logger.info(f"Got subscription_keys")

    result = app.state.mastodon.push_subscription_set(
        muninn_listener_url, public_key, follow_events=True, mention_events=True
    )

    logger.info(f"Subscription result:{result}")


@app.get("/")
def read_root():
    logger.info(f"It works!")
    return {"Hello": "World"}


@app.post("/")
def root(event: AccountCreatedEvent, request: Request):
    #   Set up Mastodon

    account_id = f"@{event.object.username}"
    message = (
        account_id
        + f" Welcome to {app.state.instance_name}! I'm your friendly welcome bot, Muninn. \n"
        "Don't forget to set up your profile and write an #introduction post. \n"
        f"Reach out to our admin, {app.state.admin_account_name}, if you have any questions or concerns. \n"
        f"New to Mastodon? Here's a quick getting started guide: {app.state.onboarding_link}"
    )

    app.state.mastodon.status_post(message, visibility="direct")

    return {"message": f"Sent welcome message to {account_id}."}


@app.post("/listener")
def notification(event: NotificationEvent):
    logger.info(f"received:{event.json()}")
    return {"message": f"Received {event.json()}"}
