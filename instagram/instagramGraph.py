import requests
import logging 
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

import instagramConfig


accessToken = "" 

#  getting instagram access token
def getAccessToken():
    global accessToken

    logging.info("Starting Get Access Token")
    response = requests.get(instagramConfig.graphAuthURL +  instagramConfig.appIDQuery + instagramConfig.appID + instagramConfig.clientSecretQuery + instagramConfig.clientSecret + instagramConfig.grantType  )
    #  breaking down the response
    if(response.status_code != 200):
        return 
    else:
        data = response.json()
        accessToken = data["access_token"]

if __name__ == '__main__':
    instagramConfig.setupLogging()
    instagramConfig.readConfig()
    instagramConfig.unmarshalSecrets()
    getAccessToken()

