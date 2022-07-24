import streamlit as st
import base64
import tempfile
from pathlib import Path
from extract import extract
from parsing import parse
from exsum import lex_rank
from summarize import trial
from firebase_admin import credentials, initialize_app, storage
import os
import shutil
import json
# Init firebase with your credentials
cred = credentials.Certificate("serviceAccountKey.json")
try:
    initialize_app(cred, {'storageBucket': 'text-summarizer-storage.appspot.com/files'})
except ValueError:
    pass

def show_pdf(file_path:str):
    """Show the PDF in Streamlit
    That returns as html component

    Parameters
    ----------
    file_path : [str]
        Uploaded PDF file path
    """
    # fileName = file_path
    # bucket = storage.bucket()
    # blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)
    # blob.make_public()
    print(file_path)
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    f.close()
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def remove_files(name):
    os.remove(f"{name}.json")
    os.remove(f"{name}.txt")
    os.remove(f"{name}.zip")
    os.remove(f"{name}.pdf")

def get(filename: str):
    extract(filename)
    parse(filename)
    lex_rank(filename)
    # return {"summary": summary}

def summarizePlease(filename: str):
    summary = trial(f"{filename}.txt")
    remove_files(filename)
    # print(summary)
    display(summary)

def buildTabs(tabs, name):
    with open("sections.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    f.close()
    i = 0
    for tab in data:
        print(tab)
        tabs.append(tab)
        i+=1

    ts = st.tabs(tabs)
    with ts[0]:
        show_pdf(name)
    while i>1:
        with ts[i-1]:
            st.markdown(f"# {tabs[i-1]}")
            st.markdown(data[tabs[i-1]])
        i-=1

def display(summary: list):
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 500px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for text in summary:
        st.sidebar.markdown("""* <div style="background-color: #337def; margin-bottom: 5px; padding: 5px 5px; padding-left: 10px"><span style="color: #fcc729;"><b> %s <b></span></div>""" % text, unsafe_allow_html=True)

def main():
  st.title("Research Paper Summarization")
  uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
  if uploaded_file is not None:
        # Make temp file path from uploaded file
        with open(uploaded_file.name, "r", encoding="utf-8") as f:
            f.write()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            f.close()
            tabs = ['Paper']
            get('temp')
            buildTabs(tabs, tmp_file.name)
            summarizePlease('temp')
            # st.write(show_pdf(tmp_file.name))

if __name__=="__main__":
    main()
