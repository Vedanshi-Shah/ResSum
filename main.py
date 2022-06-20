import urllib
from xml.etree.ElementInclude import include
from extract import extract
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib
from parsing import parse
from exsum import lex_rank
from summarize import trial
import os
import shutil
from uvicorn import run
# using flask_restful
# from flask_restful import reqparse, abort, Api, Resource
# from flask import Flask, jsonify, request
# import flask
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def remove_files(name):
    os.remove(f"{name}.json")
    os.remove(f"{name}.txt")
    os.remove(f"{name}.zip")
    os.remove(f"{name}.pdf")

@app.get("/")
def test():
    return {"message": "Hello"}

@app.get("/extract/{filename}")
def get(filename: str):
    users=db.collection(u'users')
    docs=users.stream()
    users_list=[]
    for doc in docs:
        users_list.append(doc.to_dict())
    l = None
    for u in users_list:
        if(u['file_name']==filename):
            l=u['file_url']
    NAME = filename[0:filename.find(".pdf")]
    if (not(l)): 
        print("File Not Found")
        return {"summary": None}
    urllib.request.urlretrieve(l,filename)
    extract(NAME)
    parse(NAME)
    lex_rank(NAME)
    summary = trial(f"{NAME}.txt")
    remove_files(NAME)
    return {"summary": summary}
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)
    