import csv
from enums import NotificationType


def load_users(file_name):
    users = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count != 0:
                pincodes = row[1].split("-")
                users.append({"name": row[0], "pincodes": pincodes, "user_id": row[2],
                              "phone": row[3], "notification_type": NotificationType(row[4])})
            line_count += 1
    return users
