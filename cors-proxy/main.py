from typing import Union
import secrets

import logging
import requests
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

konnektor_url=os.environ.get("KONNEKTOR_URL", "http://localhost:8081")

security = HTTPBasic()

origins = [
    "https://cors-ui.h3.spilikin.dev",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "konnektor")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

@app.get("/connector.sds")
async def services(request: Request, username: str = Depends(get_current_username)):
    r = requests.get(f"{konnektor_url}/connector.sds",
        headers={
            "User-Agent":request.headers["User-Agent"],
            "Accept":request.headers["Accept"],
        })
    logging.debug(r.text)
    return Response(content=r.text, media_type="application/xml")

@app.post("/soap-api/{path:path}", )
async def soap_proxy(path: str, request: Request, username: str = Depends(get_current_username)):
    body = await request.body()
    logging.debug(request.headers)
    #logging.debug(body)
    r = requests.post(f"{konnektor_url}/soap-api/{path}",
        headers={
            "SOAPAction":request.headers["SOAPAction"],
            "User-Agent":request.headers["User-Agent"],
            "Accept":request.headers["Accept"],
            "Content-Length":request.headers["Content-Length"],
            "Content-Type":request.headers["Content-Type"],
        },
        data=body)
    logging.debug(r.text)
    return Response(content=r.text, media_type="application/xml")

#https://www.crcind.com/csp/samples/SOAP.Demo.CLS?WSDL=1
