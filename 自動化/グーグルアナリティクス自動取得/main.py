from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import datetime
import os
import sys
import gspread
from pytz import timezone
import time

VIEW_IDs = []
names = []

def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

def define_row(ws,delta_time):
    i = 4
    while True:
        dt_now = datetime.datetime.now(timezone('Asia/Tokyo')) - datetime.timedelta(hours=delta_time)
        tmp_str = str(dt_now.month)+"/"+str(dt_now.day)
        if tmp_str == ws.acell(f'A{i}').value:
            return i
        i += 1
        if i % 10 == 0:
            time.sleep(5)

for k in range(len(VIEW_IDs)):
    delta_time = 20
    VIEW_ID = VIEW_IDs[k]
    name = names[k]
    print(name)
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    KEY_FILE_LOCATION = ''
    jsonf = ""
    spread_sheet_key = ""
    ws = connect_gspread(jsonf,spread_sheet_key)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    ws = gc.open_by_key("").worksheet(name)
    row = define_row(ws,delta_time)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    service = build('analytics', 'v3', credentials=credentials)
    
    exec_date = (datetime.datetime.today() - datetime.timedelta(hours=delta_time)).strftime("%Y-%m-%d")
    results = service.data().ga().get(ids='ga:' + VIEW_ID,start_date=exec_date,end_date=exec_date,
                                      metrics='ga:users,ga:newUsers,ga:sessions,ga:pageviews,ga:organicSearches',
                                      dimensions='ga:browser',max_results=20000).execute()
    ws.update_acell(f'B{str(row)}', results["totalsForAllResults"]["ga:users"])
    ws.update_acell(f'C{str(row)}', results["totalsForAllResults"]["ga:pageviews"])
    ws.update_acell(f'D{str(row)}', results["totalsForAllResults"]["ga:sessions"])
    ws.update_acell(f'E{str(row)}', results["totalsForAllResults"]["ga:newUsers"])
    results = service.data().ga().get(ids='ga:' + VIEW_ID,start_date=exec_date,end_date=exec_date,
                                      metrics='ga:users,ga:newUsers,ga:sessions,ga:pageviews,ga:organicSearches',
                                      dimensions='ga:fullReferrer',max_results=20000).execute()
    for i in range(len(results["rows"])):
        if results["rows"][i][0] == "(direct)":
            ws.update_acell(f'F{str(row)}', results["rows"][i][1])
            ws.update_acell(f'G{str(row)}', results["rows"][i][2])
        if results["rows"][i][0] == "t.co/":
            ws.update_acell(f'H{str(row)}', results["rows"][i][1])
            ws.update_acell(f'I{str(row)}', results["rows"][i][2])
    time.sleep(10)