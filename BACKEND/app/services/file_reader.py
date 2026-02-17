""" def read_file_from_local(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(" Failed to read local file:", str(e))
        return ""
 """
 
import os
from app.appwrite_client import get_appwrite_storage


""" def read_file_from_appwrite(file_id: str) -> str:
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
    return content.decode("utf-8", errors="ignore") """
""" 
import base64

def read_file_from_appwrite(file_id: str) -> str:
    storage = get_appwrite_storage()

    response = storage.get_file_download(
        bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
        file_id=file_id
    )

    # Case 1: bytes
    if isinstance(response, bytes):
        return response.decode("utf-8", errors="ignore")

    # Case 2: dict
    if isinstance(response, dict):

        # Case 2A: Node buffer style
        if response.get("type") == "Buffer" and "data" in response:
            byte_array = bytes(response["data"])
            return byte_array.decode("utf-8", errors="ignore")

        # Case 2B: base64 encoded
        if "data" in response and isinstance(response["data"], str):
            decoded = base64.b64decode(response["data"])
            return decoded.decode("utf-8", errors="ignore")

        # Case 2C: raw bytes inside dict
        for key in ["body", "file"]:
            if key in response and isinstance(response[key], bytes):
                return response[key].decode("utf-8", errors="ignore")
    if hasattr(response, "read"):
        return response.read().decode("utf-8", errors="ignore")

    raise Exception(f"Unsupported Appwrite response type: {type(response)}") """
import json

def read_file_from_appwrite(file_id: str) -> str:
    storage = get_appwrite_storage()

    response = storage.get_file_download(
        bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
        file_id=file_id
    )

    # If already string
    if isinstance(response, str):
        return response

    # If dict (already parsed JSON)
    if isinstance(response, dict):
        return json.dumps(response)

    # If bytes
    if isinstance(response, bytes):
        return response.decode("utf-8", errors="ignore")

    # If stream
    if hasattr(response, "read"):
        return response.read().decode("utf-8", errors="ignore")

    raise Exception(f"Unsupported Appwrite response type: {type(response)}")
