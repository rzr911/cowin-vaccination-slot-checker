from slack_sdk import WebClient

from enums import NotificationType


def send_notification(filtered_centers, user, slack_token, telegram_token):
    message = "Hey {}, following vaccination centres are available:  \n".format(
        user["name"])

    for i, key in enumerate(filtered_centers.keys()):
        center = filtered_centers[key]
        message += "\n{} *{}* {} Cost *{}*\n".format(i+1,
                                           center["name"], center["pincode"], center["fee_type"])
        for session in filtered_centers[key]["sessions"]:
            message += "\tDate *{}* Age Limit=*{}*+ Available capacity Dose1=*{}* Available capacity Dose2=*{}* Vaccine=*{}*\n".format(
                session["date"], session["min_age_limit"], session["available_capacity_dose1"], session["available_capacity_dose2"], session["vaccine"])

    if user["notification_type"] == NotificationType.SLACK:
        send_slack_message(
            message=message, user_id=user["user_id"], slack_token=slack_token)
    elif user["notification_type"] == NotificationType.TELEGRAM:
        send_telegram_message()
    elif user["notification_type"] == NotificationType.ALL:
        send_slack_message(
            message=message, user_id=user["user_id"], slack_token=slack_token)
        send_telegram_message()


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
