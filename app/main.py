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
        api_base_url=os.environ.get("API_BASE_URL")
    )

    account_id = f"@{event.object.username}"
    message = account_id + \
        " Welcome to StatisticallyHuman! I'm your friendly welcome bot, Muninn. \n" \
        "Don't forget to set up your profile and write an #introduction post. \n" \
        "Reach out to our admin, @thatguy, if you have any questions or concerns. \n" \
        "New to Mastodon? Here's a quick getting started guide: https://www.zdnet.com/article/how-to-get-started-with-mastodon/"

    mastodon.status_post(message, visibility='direct')

    return {"message": f"Sent welcome message to {account_id}."}