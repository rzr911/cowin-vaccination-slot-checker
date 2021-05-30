from enum import Enum


class NotificationType(Enum):
    ALL = "all"
    TELEGRAM = "telegram"
    SLACK = "slack"

class AgeGroup(Enum):
    ALL = "all"
    EIGHTEEN_PLUS = "18"
    FORTY_FIVE_PLUS = "45"


class Dose(Enum):
    ALL = "all"
    FIRST = "first"
    SECOND = "second"