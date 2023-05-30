import requests
import json
import yaml
import logging 
from datetime import date

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

appID = ""
clientSecret = ""
clientSecretQuery = ""
appIDQuery = ""
authURL = ""
accessToken = "" 
grantType = ""

def setupLogging():
    logging.basicConfig(filename='out.log', encoding='utf-8', level=logging.DEBUG)
    logging.info(date.today())

def readConfig():
    logging.info("Starting read Config... ")
    global authURL
    global appIDQuery
    global grantType
    global clientSecretQuery
    with open("./config/config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            authURL = str(data["instagram"]["auth"])
            appIDQuery = str(data["instagram"]["appID"])
            clientSecretQuery = str(data["instagram"]["clientSecret"])
            grantType = str(data["instagram"]["grantType"])
        except yaml.YAMLError as exc:
            logging.warning(exc)

def unmarshalSecrets():
    logging.info("Starting Unmarshal Secrets ... ")
    global appID
    global clientSecret
    with open("./config/secrets.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            appID = str(data["instagram"]["appId"])
            clientSecret = str(data["instagram"]["clientSecret"])
        except yaml.YAMLError as exc:
            logging.warning(exc)

def getAccessToken():
    global accessToken
    logging.info("Starting Get Access Token")
    response = requests.get(authURL +  appIDQuery + appID + clientSecretQuery + clientSecret + grantType  )
    #  breaking down the response
    if(response.status_code != 200):
        return 
    else:
        data = response.json()
        accessToken = data["access_token"]

if __name__ == '__main__':
    setupLogging()
    readConfig()
    unmarshalSecrets()
    getAccessToken()

