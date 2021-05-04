import json
import requests
import os
from datetime import datetime, timedelta
from environs import Env
import csv
from slack_sdk import WebClient
import redis



env = Env()
env.read_env()
r = redis.Redis()

API_ENDPOINT_URL = "https://cdn-api.co-vin.in/api"

slot_endpoint = "/v2/appointment/sessions/public/calendarByPin"
week_range = env.int("WEEK_RANGE")
available_capacity = env.int("AVAILABILITY", 1)
slack_token = env('slack_token')


users = []

def load_users(users):
  with open('users.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            pincodes = row[1].split("-")
            users.append({"name": row[0], "pincodes": pincodes, "user_id": row[2]})
        line_count +=1
        


def find_slots():
    users = []
    load_users(users=users)
    filtered_centers = {}
    today = datetime.today()

    for user in users:
      if not r.get(user["user_id"]):
        for i in range(week_range):
            day = today + timedelta(days=(i * 7))
            day = day.strftime('%d-%m-%Y')

            for pincode in user["pincodes"]:
                params = {'pincode': pincode, 'date': day}
                centers = call_vaccination_slot_api(params=params)
                filter_centers(centers=centers, filtered_centers=filtered_centers)
        if filtered_centers:
          send_notification(filtered_centers=filtered_centers, user_id=user["user_id"])
        filtered_centers = {}


def filter_centers(centers, filtered_centers):
  for center in centers:
    for session in center['sessions']:
      if session['available_capacity'] >= available_capacity:
        process_center(filtered_centers, center, session)
  return filtered_centers


def process_center(filtered_centers, center, session):
  if center['center_id'] in filtered_centers:
    filtered_centers[center['center_id']]['sessions'].append(session)
  else:
    filtered_centers[center['center_id']] = center
    filtered_centers[center['center_id']]['sessions'] = [session]


def send_notification(filtered_centers, user_id):
    r.setex(user_id, timedelta(hours=2), "set")
    # r.setex(user_id, timedelta(minutes=2), "set")
    message = "Hey following vaccinations centres are available:  \n"
    for i, key in enumerate(filtered_centers.keys()):
        center = filtered_centers[key]
        message += "\n{} *{}* {}\n".format(i+1, center["name"], center["pincode"])
        for session in filtered_centers[key]["sessions"]:
            message += "\tDate {} Available capacity {} Vaccine {}\n".format(session["date"], session["available_capacity"], session["vaccine"])
    send_slack_message(message=message, user_id=user_id)


def send_slack_message(message, user_id):
  client = WebClient(token=slack_token)
  response = client.api_call(
    api_method='chat.postMessage',
    json={'channel': user_id,'text': message}
  )
  client.api_call(
    api_method='chat.postMessage',
    json={'channel': "UGNCYFTBP",'text': message}
  )


def call_vaccination_slot_api(params):
  s = requests.Session()
  s.headers.update({'Accept-Language': 'en-US'})
  url = API_ENDPOINT_URL + slot_endpoint
  response = s.get(url=url, params=params)
  data = response.json()
  return data['centers']
