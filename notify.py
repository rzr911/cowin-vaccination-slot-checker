from slack_sdk import WebClient

from enums import Dose, NotificationType, AgeGroup


def send_notification(filtered_centers, user, slack_token, telegram_token, available_capacity):
    message = "Hey {}, following vaccination centres are available:  \n".format(
        user["name"])
    is_message_valid = False
    for i, key in enumerate(filtered_centers.keys()):
        center = filtered_centers[key]
        is_center_valid = False
        center_message = "\n{} *{}* {} Cost *{}*\n".format(i+1,
                                           center["name"], center["pincode"], center["fee_type"])
        for session in filtered_centers[key]["sessions"]:
            if check_user_filters(center_session=session, user=user, available_capacity=available_capacity):
                is_message_valid = True
                is_center_valid = True
                center_message += "\tDate *{}* Age Limit=*{}*+ Available capacity Dose1=*{}* Available capacity Dose2=*{}* Vaccine=*{}*\n".format(
                    session["date"], session["min_age_limit"], session["available_capacity_dose1"], session["available_capacity_dose2"], session["vaccine"])
        if is_center_valid:
            message += center_message

    if is_message_valid:
        if user["notification_type"] == NotificationType.SLACK:
            send_slack_message(
                message=message, user_id=user["user_id"], slack_token=slack_token)
        elif user["notification_type"] == NotificationType.TELEGRAM:
            send_telegram_message()
        elif user["notification_type"] == NotificationType.ALL:
            send_slack_message(
                message=message, user_id=user["user_id"], slack_token=slack_token)
            send_telegram_message()

def check_user_filters(center_session, user, available_capacity):
    session_age_limit = int(center_session["min_age_limit"])
    capacity_dose_1 = int(center_session["available_capacity_dose1"])
    capacity_dose_2 = int(center_session["available_capacity_dose2"])

    if user["age_limit"] == AgeGroup.ALL or session_age_limit == int(user["age_limit"].value):
        if user["dose"] == Dose.ALL:
            return True
        elif user["dose"] == Dose.FIRST:
            return capacity_dose_1 > available_capacity
        elif user["dose"] == Dose.SECOND:
            return capacity_dose_2 > available_capacity
    
    return False

def send_slack_message(message, user_id, slack_token):
    client = WebClient(token=slack_token)
    client.api_call(
        api_method='chat.postMessage',
        json={'channel': user_id, 'text': message}
    )

    if user_id != "UGNCYFTBP":
        client.api_call(
            api_method='chat.postMessage',
            json={'channel': "UGNCYFTBP", 'text': message}
        )


def send_telegram_message():
    pass


def send_error_notification(message, slack_token):
    client = WebClient(token=slack_token)
    client.api_call(
        api_method='chat.postMessage',
        json={'channel': "UGNCYFTBP", 'text': message}
    )
