import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.storage import Storage

load_dotenv()


def get_appwrite_storage() -> Storage:
    client = Client()
    client.set_endpoint(os.getenv("APPWRITE_ENDPOINT"))
    client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
    client.set_key(os.getenv("APPWRITE_API_KEY"))
    return Storage(client)
