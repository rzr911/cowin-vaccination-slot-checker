import json
import requests
import os
from datetime import datetime, timedelta
from environs import Env

env = Env()
env.read_env()

API_ENDPOINT_URL = "https://cdn-api.co-vin.in/api"

slot_endpoint = "/v2/appointment/sessions/public/calendarByPin"
pincodes = env.list("PINCODES")
week_range = env.int("WEEK_RANGE")
available_capacity = env.int("AVAILABILITY", 1)
slack_api_endpoint = env('SLACK_HOOK_URL')

def find_slots():
    filtered_centers = {}
    today = datetime.today()

    for i in range(week_range):
        day = today + timedelta(days=(i * 7))
        day = day.strftime('%d-%m-%Y')

        for pincode in pincodes:
            params = {'pincode': pincode, 'date': day}
            centers = call_vaccination_slot_api(params=params)
            filter_centers(centers=centers, filtered_centers=filtered_centers)
    if filtered_centers:
      send_notification(filtered_centers=filtered_centers)


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


def send_notification(filtered_centers):
    message = "Hey following vaccinations centres are available:  \n"
    for i, key in enumerate(filtered_centers.keys()):
        center = filtered_centers[key]
        message += "\n{} *{}* {}\n".format(i+1, center["name"], center["pincode"])
        for session in filtered_centers[key]["sessions"]:
            message += "\tDate {} Available capacity {} Vaccine {}\n".format(session["date"], session["available_capacity"], session["vaccine"])
    send_slack_message(message=message)


def send_slack_message(message):
    s = requests.Session()
    s.headers.update({'Content-type': 'application/json'})
    s.post(url=slack_api_endpoint, json={"text": message})


def call_vaccination_slot_api(params):
  s = requests.Session()
  s.headers.update({'Accept-Language': 'en-US'})
  url = API_ENDPOINT_URL + slot_endpoint
  response = s.get(url=url, params=params)
  data = response.json()
  return data['centers']
