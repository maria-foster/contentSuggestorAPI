import requests
import json
import yaml
import logging 
from datetime import date

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
# my URL

url = ""

#  URLS 
generalSearchURL = "" 
clientSecretQuery = ""
appIDQuery = ""
graphAuthURL = ""
basicAuthURL = "" 
grantType = ""
redirectURL = "" 
authScope = "" 

#  Secrets
appID = ""
clientSecret = ""
basicClientID = "" 
graphAccessToken = ""
basicAccessToken = "" 



#  eventually move this out to main file or some sort of config setup 
def setupLogging():
    logging.basicConfig(filename='out.log', encoding='utf-8', level=logging.DEBUG)
    logging.info(date.today())

#  eventually move this out to main file or some sort of config setup 
def readConfig():
    logging.info("Starting read Config... ")
    global graphAuthURL
    global appIDQuery
    global grantType
    global clientSecretQuery
    global generalSearchURL
    global basicAuthURL
    global authScope
    global url
    global redirectURL
    with open("./config/config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            url = str(data["url"])
            redirectURL = str(data["instagram"]["redirectURL"])
            graphAuthURL = str(data["instagram"]["graph"]["auth"])
            basicAuthURL = str(data["instagram"]["basic"]["auth"])
            authScope = str(data["instagram"]["basic"]["authScope"])
            appIDQuery = str(data["instagram"]["appID"])
            clientSecretQuery = str(data["instagram"]["clientSecret"])
            grantType = str(data["instagram"]["grantType"])
            generalSearchURL = str(data["instagram"]["generalSearch"])
        except yaml.YAMLError as exc:
            logging.warning(exc)

#  eventually move this out to main file or some sort of config setup 
def unmarshalSecrets():
    logging.info("Starting Unmarshal Secrets ... ")
    global appID
    global clientSecret
    global basicClientID

    with open("./config/secrets.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            appID = str(data["instagram"]["appId"])
            clientSecret = str(data["instagram"]["clientSecret"])
            basicClientID = str(data["instagram"]["basicClientId"])
        except yaml.YAMLError as exc:
            logging.warning(exc)


if __name__ == '__main__':
    setupLogging()
    readConfig()
    unmarshalSecrets()