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

# filename = Deep learning for grapes variety recognition



def remove_files(name):
    os.remove(f"json-output/{name}.json")
    #os.mkdir("json-output")
    
    os.remove(f"parsed-output/{name}.txt")
    #os.mkdir("parsed-output")

    os.remove(f"output/{name}.zip")
    #os.mkdir("output")
    
    os.remove(f"papers/{name}.pdf")

@app.get("/")
def test():
    return {"message": "Hello"}

@app.get("/extract/{filename}")
def get(filename: str):
    # print(filename)
    # Use a service account
    users=db.collection(u'users')
    docs=users.stream()
    users_list=[]
    for doc in docs:
        users_list.append(doc.to_dict())
    # print(users_list)
    # print(filename)
    l = None
    for u in users_list:
        if(u['file_name']==filename):
            l=u['file_url']
            # print("Here")
    NAME = filename[0:filename.find(".pdf")]
    if (not(l)): 
        print("File Not Found")
        # response = flask.jsonify({'summary': None})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return {"summary": None}
    urllib.request.urlretrieve(l,"papers/"+filename)
    extract(NAME)
    parse(NAME)
    lex_rank(NAME)
    summary = trial(f"parsed-output/{NAME}.txt")
    remove_files(NAME)
    #print(summary)
    # response = flask.jsonify({'summary': summary})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return {"summary": summary}
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)
    