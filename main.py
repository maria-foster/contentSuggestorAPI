import requests
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True) 
        parser.add_argument('password', required=True) 
        args = parser.parse_args()
        print(args["email"])
        print(args["password"])
        data_dict = getByFieldFromCSV(args["email"], args["password"], 'data/users.csv')
        return data_dict, 200 

class Influencers(Resource):
    def get(self):
        list = []
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, location='args')
        args = parser.parse_args()
        data_dict = getByOneFieldFromCSV(args["email"], 'data/users.csv')
        infl = data_dict[0]["favoriteInfluencers"].split(".")
        print(infl)
        for inf in infl:
            response = requests.get("https://www.instagram.com/web/search/topsearch/?query=" + inf)
            #  breaking down the response
            if(response.status_code != 200):
                return csv_to_json("data/influencerBackup.csv"), 200
            else:
                data = response.json()["users"][0]["user"]
                user = {
                "id" : data["pk"],
                "username" : data["username"],
                "privateStatus" : data["is_private"],
                "verifiedStatus": data["is_verified"],
                "profilePic" : data["profile_pic_url"]
                }
            print(user)
            list.append(user)
        return list, 200 
class Instagram(Resource):
    def get(self):
        results = []
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True) 
        args = parser.parse_args()
        query = args["query"]
        response = requests.get("https://www.instagram.com/web/search/topsearch/?query=" + query)
        return response.json()
class InstagramFeed(Resource):
    def get(self):
        results = []
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='args')
        args = parser.parse_args()
        id = args["id"]
        response = requests.get("https://instagram.com/graphql/query/?query_id=17888483320059182&variables={\"id\":\"" + id + "\",\"first\":20,\"after\":null}")
        resp2 = response.json()["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for edge in resp2:
            capt = edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            print(capt)
            results.append(capt)
        return results, 200
class Questions(Resource):
    def get(self):
        f = open('data/questions.json')
        data = json.load(f)
        return data, 200
    pass

class Categories(Resource):
    def get(self):
        f = open('data/categories.json')
        data = json.load(f)
        return data, 200
    pass

class Trends(Resource):
    def get(self):
        f = open('data/trends.json')
        data = json.load(f)
        return data, 200
    pass
class Hashtags(Resource):
    def get(self):
        f = open('data/hashtags.json')
        data = json.load(f)
        return data, 200
    pass

class TwitterTrends(Resource):
    def get(self):
        f = open('data/twitterTrends.json')
        data = json.load(f)
        return data, 200
    pass
class InstagramTrends(Resource):
    def get(self):
        f = open('data/instagramTrends.json')
        data = json.load(f)
        return data, 200
    pass
class TiktokTrends(Resource):
    def get(self):
        f = open('data/tiktokTrends.json')
        data = json.load(f)
        return data, 200
    pass

class Users(Resource):
    def get(self):
        # f = open('data/users.json')
        # data = json.load(f)
        # return data, 200
        data = pd.read_csv('data/users.csv')  # read CSV
        # data = data.to_dict()  # convert dataframe to dictionary
        data_dict = csv_to_json('data/users.csv')
        return data_dict, 200 

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('twitterUsername', required=True)  # add args
        parser.add_argument('tiktokUsername', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('lastName', required=True)
        parser.add_argument('firstName', required=True)
        parser.add_argument('instagramUsername', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('categories', required=True)
        parser.add_argument('favoritePlatform', required=True)
        parser.add_argument('favoriteInfluencers', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        
        # create new dataframe containing new values
        new_data = pd.DataFrame([{
            'twitterUsername': args['twitterUsername'],
            'tiktokUsername': args['tiktokUsername'],
            'password': args['password'],
            'lastName': args['lastName'],
            'firstName': args['firstName'],
            'instagramUsername': args['instagramUsername'],
            'email': args['email'],
            'categories': args['categories'],
            'favoritePlatform': args['favoritePlatform'],
            'favoriteInfluencers': args['favoriteInfluencers']
            
        }])
        # read our CSV
        data = pd.read_csv('data/users.csv')
        # add the newly provided values
        data = pd.concat([data, pd.DataFrame(new_data)], ignore_index=True)
        # data = data.concat(new_data, ignore_index=True)
        # save back to CSV
        data.to_csv('data/users.csv', index=False)
        data_dict = csv_to_json('data/users.csv')
        return {'data': data_dict}, 200 # return data with 200 OK
    pass

api.add_resource(Questions, '/questions') 
api.add_resource(TiktokTrends, '/Tiktok') 
api.add_resource(TwitterTrends, '/Twitter') 
api.add_resource(InstagramTrends, '/Instagram') 
api.add_resource(Users, '/users') 
api.add_resource(Influencers, '/influencers') 
api.add_resource(Instagram, '/instagram') 
api.add_resource(InstagramFeed, '/instagramFeed') 
api.add_resource(Login, '/login') 
api.add_resource(Categories, '/Categories') 
api.add_resource(Hashtags, '/Hashtags') 
api.add_resource(Trends, '/Trends') 

import csv
import json

def getByOneFieldFromCSV(email, csv_file_path):
    list = []
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for row in csv_reader:
            
            #assuming a column named 'No'
            if row["email"] == email:
                list.append(row)
    return list

def getByFieldFromCSV(email, password, csv_file_path):
    list = []
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for row in csv_reader:
            
            #assuming a column named 'No'
            if row["email"] == email and row["password"]== password:
                list.append(row)
    return list

def csv_to_json(csv_file_path):
    list = []
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for row in csv_reader:
 
            #assuming a column named 'No'
            #to be the primary key
            list.append(row)
    return list
 

if __name__ == "__main__":
    app.run(debug=True)