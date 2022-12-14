import tweepy
from ssl import ALERT_DESCRIPTION_INSUFFICIENT_SECURITY
import time
import subprocess
import requests
import time
import numpy as np
from subprocess import PIPE
import pandas as pd
import random
import socket
import requests
import re
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from pytz import timezone
from gspread_dataframe import get_as_dataframe, set_with_dataframe

CONSUMER_KEY = ""
CONSUMER_SECRET =  ""
ACCESS_TOKEN =  ""
ACCESS_TOKEN_SECRET =  ""
delta_time = 6

def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

def define_row(ws):
    i = 1
    while True:
        dt_now = datetime.datetime.now(timezone('Asia/Tokyo')) - datetime.timedelta(hours=delta_time)
        print(dt_now)
        tmp_str = str(dt_now.month)+"/"+str(dt_now.day)
        if tmp_str == ws.acell(f'A{i}').value:
            return i
        i += 1

jsonf = ""
spread_sheet_key = ""
ws = connect_gspread(jsonf,spread_sheet_key)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
gc = gspread.authorize(credentials)
ws = gc.open_by_key("").worksheet("")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit = True)
row = define_row(ws)

users = []
cols = ["E","G","I","K","M","O","Q","S","U","W","Y","AA","AC","AE","AG"]
for i in range(len(users)):
    user = users[i]
    col=cols[i]
    data = api.get_user(screen_name=user)
    follower = int(data.followers_count)
    print(f'{col}{str(row)}')
    ws.update_acell(f'{col}{str(row)}',follower)