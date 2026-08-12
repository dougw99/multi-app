import streamlit as st
import requests

# Configuration for backend URLs
BACKEND_LIST_URL = "http://172.17.0.2:8001/list-files"
BACKEND_UPLOAD_URL = "http://172.17.0.3:8002/upload-file"

st.set_page_config(page_title="Azure File Manager", layout="wide")

st.title("☁️ Azure File Manager SPA")
st.markdown("This application demonstrates a single-page interface interacting with two separate backend services.")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["📂 List Files", "📤 Upload File"])

# --- Tab 1: List Files ---
with tab1:
    st.header("List Files from Azure Storage")
    if st.button("Refresh File List"):
        try:
            with st.spinner("Fetching file list..."):
                response = requests.get(BACKEND_LIST_URL)
                if response.status_code == 200:
                    data = response.json()
                    files = data.get("files", [])
                    
                    if not files:
                        st.info("No files found in the container.")
                    else:
                        st.success(f"Found {len(files)} files.")
                        # Display files in a table-like format
                        for file in files:
                            col1, col2, col3 = st.columns([3, 2, 2])
                            with col1:
                                st.write(f"📄 {file['name']}")
                            with col2:
                                st.write(f"📏 {file['size']} bytes")
                            with col3:
                                st.write(f"📅 {file['last_modified']}")
                            st.divider()
                else:
                    st.error(f"Failed to fetch files. Status Code: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred while connecting to the List Service: {e}")

# --- Tab 2: Upload File ---
with tab2:
    st.header("Upload File to Azure Storage")
    uploaded_file = st.file_uploader("Choose a file to upload", type=None)

    if uploaded_file is not None:
        if st.button("Upload Now"):
            try:
                with st.spinner(f"Uploading '{uploaded_file.name}'..."):
                    # Prepare the file for multipart/form-data upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    response = requests.post(BACKEND_UPLOAD_URL, files=files)
                    
                    if response.status_code == 200:
                        st.success(f"Successfully uploaded: {response.json().get('message')}")
                    else:
                        st.error(f"Failed to upload file. Status Code: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred while connecting to the Upload Service: {e}")
    else:
        st.info("Please select a file to upload.")

st.sidebar.markdown("---")
st.sidebar.info("Backend Services Status:")
st.sidebar.write("- **List Service**: `http://localhost:8001`")
st.sidebar.write("- **Upload Service**: `http://localhost:8002`")
