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
graphAuthURL = ""
accessToken = "" 
grantType = ""


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
    with open("./config/config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            graphAuthURL = str(data["instagram"]["graph"]["auth"])
            appIDQuery = str(data["instagram"]["appID"])
            clientSecretQuery = str(data["instagram"]["clientSecret"])
            grantType = str(data["instagram"]["grantType"])
        except yaml.YAMLError as exc:
            logging.warning(exc)

#  eventually move this out to main file or some sort of config setup 
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


if __name__ == '__main__':
    setupLogging()
    readConfig()
    unmarshalSecrets()