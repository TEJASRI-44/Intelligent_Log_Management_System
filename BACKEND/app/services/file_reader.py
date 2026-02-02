""" def read_file_from_local(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print("❌ Failed to read local file:", str(e))
        return ""
 """
 
import os
from app.appwrite_client import get_appwrite_storage


def read_file_from_appwrite(file_id: str) -> str:
    storage = get_appwrite_storage()

    response = storage.get_file_download(
        bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
        file_id=file_id
    )

    # Appwrite may return bytes or stream-like object
    if isinstance(response, bytes):
        return response.decode("utf-8", errors="ignore")

    # Fallback for streamed responses
    content = response.read()
    return content.decode("utf-8", errors="ignore")

