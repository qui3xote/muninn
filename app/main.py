import os

from mastodon import Mastodon
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

class Account(BaseModel):
    # see AccountSerializer for the full list of properties: 
    #   https://github.com/mastodon/mastodon/blob/main/app/serializers/rest/admin/account_serializer.rb
    username: str

class Status(BaseModel):
    id: str
    uri: str
    url: str
    account: Account
    in_reply_to_id: Optional(str)
    in_reply_to_account_id: Optional(str)

class Notification(BaseModel):
    id: str
    created_at: str
    type: str
    account: Account
    status: Optional(Status)

class AccountCreatedEvent(BaseModel):
    event: str
    created_at: str
    object: Account

class NotificationEvent(BaseModel):
    notification: dict
    

async def lifespan():
    app.state.mastodon = Mastodon(
        access_token=os.environ.get("ACCESS_TOKEN"),
        api_base_url=os.environ.get("API_BASE_URL")
    )
    app.state.instance_name = os.environ.get("INSTANCE_NAME"),
    app.state.admin_account_name = os.environ.get("ADMIN_ACCOUNT_NAME"),
    app.state.onboarding_link = os.environ.get("ONBOARDING_LINK")
    
    muninn_listener_url = os.environ.get("MUNINN_LISTENER_URL")
    subscription_keys = app.state.mastodon.push_subscription_generate_keys()

    app.state.push_subscription_set(
        muninn_listener_url, 
        subscription_keys,
        follow_events=True,
        mention_events=True
    )

    yield
    # do something after shutdown

load_dotenv()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def root(event: AccountCreatedEvent, request: Request):
    #   Set up Mastodon

    account_id = f"@{event.object.username}"
    message = account_id + \
        f" Welcome to {app.state.instance_name}! I'm your friendly welcome bot, Muninn. \n" \
        "Don't forget to set up your profile and write an #introduction post. \n" \
        f"Reach out to our admin, {app.state.admin_account_name}, if you have any questions or concerns. \n" \
        f"New to Mastodon? Here's a quick getting started guide: {app.stateonboarding_link}"

    mastodon.status_post(message, visibility='direct')

    return {"message": f"Sent welcome message to {account_id}."}


@app.post("/listener")
def notification(event: NotificationEvent):
    print(f"received:{event.json()}")
    return {"message": f"Received {event.json()}"}