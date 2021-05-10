import requests
from notify import send_error_notification

API_ENDPOINT_URL = "https://cdn-api.co-vin.in/api"
slot_endpoint = "/v2/appointment/sessions/public/calendarByPin"


def find_slots(pincode, day, available_capacity, slack_token):
    try:
        filtered_centers = {}
        params = {'pincode': pincode, 'date': day}
        centers = call_vaccination_slot_api(params=params)
        filter_centers(centers=centers, filtered_centers=filtered_centers,
                       available_capacity=available_capacity)
        if filtered_centers:
            return filtered_centers
        return None
    except Exception as e:
        print(e)
        send_error_notification(message=str(e), slack_token=slack_token)


def filter_centers(centers, filtered_centers, available_capacity):
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


def call_vaccination_slot_api(params):
    s = requests.Session()
    s.headers.update({'Accept-Language': 'en-US',
                      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/87.0.664.75'})
    url = API_ENDPOINT_URL + slot_endpoint
    response = s.get(url=url, params=params)
    data = response.json()
    return data['centers']
