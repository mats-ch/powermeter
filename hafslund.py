#!/usr/bin/python

import ConfigParser
import pyrebase

config = ConfigParser.RawConfigParser()
config.read('hafslund.conf')

fb_config = {"apiKey": config.get("hafslund", "apiKey"),
        "authDomain": config.get("hafslund", "authDomain"),
        "databaseURL": config.get("hafslund", "databaseURL"),
        "projectId": config.get("hafslund", "projectId"),
        "storageBucket": config.get("hafslund", "storageBucket"),
        "messagingSenderId": config.get("hafslund", "messagingSenderId")}

refreshtoken = config.get("hafslund", "refreshtoken")

firebase = pyrebase.initialize_app(fb_config)
db = firebase.database()

def refresh_token(refreshtoken):
    data = firebase.auth().refresh(refreshtoken)
    return data["idToken"], data["userId"]

def get_auth(uid, accesstoken):
    data = db.child("hafslund").child("erna").child(uid).get(token=accesstoken)
    out = {}
    for i in data.each():
        out[i.key()] = i.val()

    return out

def get_user(uid, accesstoken):
    data = db.child("hafslund").child("users").child(uid).get(token=accesstoken)
    out = {}
    for i in data.each():
        out[i.key()] = i.val()

    return out

def get_meter_data(uid, meter, accesstoken):
    data = db.child("hafslund").child("consumptions").child(uid).child(meter).get(token=accesstoken)
    out = {}
    for i in data.each():
        out[i.key()] = i.val()

    return out

if __name__ == "__main__":
    at, uid = refresh_token(refreshtoken)
    user = get_auth(uid, at)["customerId"]
    meter = get_user(user, at)["meteringPoints"].keys()[0]
    print get_meter_data(user, meter, at)
