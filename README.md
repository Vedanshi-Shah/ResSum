# ResSum
Research Paper Summarization

# Getting Started
1) Download the t5-large folder from https://drive.google.com/drive/folders/1ykaq5CnIVT02MPqPNth_50RhNShgeFW3?usp=sharing and place it in the root folder
2) Get API credentials from Adobe Extract API at https://developer.adobe.com/document-services/apis/pdf-extract/. Get their 'Getting Started' files and place *pdfservices-api-credentials.json* and *private.key* in the *backend* folder
3) Setup Firebase and put *serviceAccountKey.json* in the *backend* folder
4) Create a collection in Firestore Database by the name **users** and you're good to go
5) Ensure all libraries are installed for backend by running **pip install -r backend/requirements.txt** from the root folder
6) Run backend/main.py or run **uvicorn main:app --reload** to start the backend
7) Ensure all packages are installed for the frontend using **npm i**
8) Start the frontend by running **npm start**
9) Summarize some research papers!

# Example
![Page showing Research Paper's pdf on left and its summary on the right](main.png)
