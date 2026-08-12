import os
from fastapi import FastAPI, HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get connection string and container name from environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

if not AZURE_STORAGE_CONNECTION_STRING or not CONTAINER_NAME:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING and CONTAINER_NAME must be set in environment variables.")

# Initialize BlobServiceClient
try:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
except Exception as e:
    raise RuntimeError(f"Failed to initialize BlobServiceClient: {e}")

@app.get("/")
async def root():
    return {"message": "Backend List Service is running"}

@app.get("/list-files")
async def list_files():
    """
    Lists all blobs in the specified container.
    """
    try:
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_list = container_client.list_blobs()
        
        files = []
        for blob in blob_list:
            files.append({
                "name": blob.name,
                "size": blob.size,
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None
            })
        
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
