from app.appwrite_client import get_appwrite_storage
import os

storage = get_appwrite_storage()

files = storage.list_files(
    bucket_id=os.getenv("APPWRITE_BUCKET_ID")
)

print("Connected to Appwrite. Files:", files["total"])
