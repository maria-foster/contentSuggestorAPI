import requests
import logging 
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

import instagramConfig


graphAccessToken = "" 

#  getting instagram access token
def getGraphAccessToken():
    global graphAccessToken
    logging.info("Starting Get Access Token")
    response = requests.get(instagramConfig.graphAuthURL +  instagramConfig.appIDQuery + instagramConfig.appID + instagramConfig.clientSecretQuery + instagramConfig.clientSecret + instagramConfig.grantType  )
    #  breaking down the response
    if(response.status_code != 200):
        return 
    else:
        data = response.json()
        graphAccessToken = data["access_token"]

def generalSearch(searchTerm):
    logging.info("Starting Get Access Token")
    # response = requests.get(instagramConfig.generalSearchURL + searchTerm)
    response = requests.get("https://www.instagram.com/web/search/topsearch/?query=aspynovard")
    #  breaking down the response
    if(response.status_code != 200):
        return 
    else:
        data = response.json()
        print(data)


if __name__ == '__main__':
    instagramConfig.setupLogging()
    instagramConfig.readConfig()
    instagramConfig.unmarshalSecrets()
    getGraphAccessToken()
    generalSearch("aspynOvard")

