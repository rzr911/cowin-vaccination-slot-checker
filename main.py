from datetime import datetime, timedelta
import time
import csv
import json

import schedule
import redis
from environs import Env

from enums import NotificationType
from vaccination_slots import find_slots, filter_centers
from utils import load_users
from notify import send_notification, send_error_notification

env = Env()
env.read_env()

redis_cli = redis.Redis(decode_responses=True)

total_api_calls = env.int("TOTAL_API_CALLS", 100)
duration_in_seconds = env.int("DURATION", 300)
cache_expiration = env.int("CACHE_EXPIRATION", 6)
slack_token = env('slack_token')
available_capacity = env.int("AVAILABILITY", 1)
user_file = 'users.csv'

def main():
    try:
        users = load_users(user_file)
        pincode_set = {
            str(pincode) for user in users for pincode in user["pincodes"]}
        today = datetime.today()
        today_string = today.strftime('%d-%m-%Y')
        pincodes_with_new_centres = set()
        filtered_centers = {}

        for pincode in pincode_set:
            # load and pass availability value
            updated_centres = find_slots(
                pincode=pincode, day=today_string, available_capacity=available_capacity, slack_token=slack_token)
            if updated_centres:
                result = check_and_set_cache(
                    pincode=pincode, centres=updated_centres)
                if result:
                    pincodes_with_new_centres.add(pincode)

        for pincode in pincodes_with_new_centres:
            centres = redis_cli.get(pincode)
            centres = json.loads(centres)
            users = [user for user in users if pincode in user["pincodes"]]

            for user in users:
                send_notification(filtered_centers=centres, user=user,
                                  slack_token=slack_token, telegram_token=None)
    except Exception as err:
        raise err
        send_error_notification(message=str(err), slack_token=slack_token)


def check_and_set_cache(pincode, centres):
    cache_result = redis_cli.get(pincode)

    if cache_result:
        cache_result = json.loads(cache_result)
    
    centres = json.loads(json.dumps(centres))
    if not cache_result or cache_result != centres:
        redis_cli.setex(pincode, timedelta(
            hours=cache_expiration), json.dumps(centres))
        return True

    return False



all_users = load_users(user_file)
total_pincodes = len({
    str(pincode) for user in all_users for pincode in user["pincodes"]})

seconds = (duration_in_seconds * total_pincodes)/total_api_calls
schedule.every(seconds).seconds.do(main)


while 1:
    schedule.run_pending()
    time.sleep(1)
