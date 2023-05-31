
import requests
import logging 
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

import instagramConfig

#  getting instagram access token
def getBasicAccessToken():
    global basicAccessToken
    logging.info("Starting Get Basic Access Token...")
    response = requests.get(instagramConfig.basicAuthURL +  instagramConfig.appIDQuery + instagramConfig.basicClientID + instagramConfig.redirectURL + instagramConfig.url  + instagramConfig.authScope )
    #  breaking down the response
    if(response.status_code != 200):
        return 
    else:
        data = response.json()
 
        

if __name__ == '__main__':
    instagramConfig.setupLogging()
    instagramConfig.readConfig()
    instagramConfig.unmarshalSecrets()
    getBasicAccessToken()