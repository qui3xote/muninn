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


@app.post("/")
def root(event: AccountCreatedEvent):
    #   Set up Mastodon
    mastodon = Mastodon(
        access_token=os.environ.get("ACCESS_TOKEN"),
        api_base_url=os.environ.get("API_BASE_URL")
    )

    account_id = f"@{event.object.username}"
    message = account_id + \
        " Welcome to graphics.social! \n" \
        "Introduce yourself to everyone by posting a toot with the #introductions hashtag. \n" \
        "If you are new to Mastodon, you'll need to follow people to get posts in your Home timeline. \n" \
        "You can also check out the local timeline to see what others are posting on this instance. \n" \
        "Checkout the federated timeline to see a collection of all posts everyone on this instance follows. \n" \
        "Reach out to our admin, brian, if you have any questions or concerns!"

    mastodon.status_post(message, visibility='direct')

    return {"message": f"Sent welcome message to {account_id}."}