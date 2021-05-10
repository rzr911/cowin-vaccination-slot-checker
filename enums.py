from enum import Enum


class NotificationType(Enum):
    ALL = "all"
    TELEGRAM = "telegram"
    SLACK = "slack"
