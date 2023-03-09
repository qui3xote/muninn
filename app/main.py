import os

from mastodon import Mastodon
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

class Account(BaseModel):
    # see AccountSerializer for the full list of properties: 
    #   https://github.com/mastodon/mastodon/blob/main/app/serializers/rest/admin/account_serializer.rb
    username: str


class AccountCreatedEvent(BaseModel):
    event: str
    created_at: str
    object: Account

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def root(event: AccountCreatedEvent):
    #   Set up Mastodon
    mastodon = Mastodon(
        access_token=os.environ.get("ACCESS_TOKEN"),
        api_base_url=os.environ.get("API_BASE_URL"),
        instance_name=os.environ.get("INSTANCE_NAME"),
        admin_account_name=os.environ.get("ADMIN_ACCOUNT_NAME"),
        onboarding_link=os.environ.get("ONBOARDING_LINK")
    )

    account_id = f"@{event.object.username}"
    message = account_id + \
        f" Welcome to {instance_name}! I'm your friendly welcome bot, Muninn. \n" \
        "Don't forget to set up your profile and write an #introduction post. \n" \
        f"Reach out to our admin, {admin_account_name}, if you have any questions or concerns. \n" \
        f"New to Mastodon? Here's a quick getting started guide: {onboarding_link}"

    mastodon.status_post(message, visibility='direct')

    return {"message": f"Sent welcome message to {account_id}."}