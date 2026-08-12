import os
from fastapi import FastAPI, HTTPException, UploadFile, File
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
    return {"message": "Backend Upload Service is running"}

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the specified container in Azure Blob Storage.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        
        # Read file content
        content = await file.read()
        
        # Upload to Azure
        blob_client.upload_blob(content, overwrite=True)
        
        return {"message": f"File '{file.filename}' uploaded successfully.", "name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
