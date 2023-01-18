#! /usr/bin/env python3

import sys
import datetime
import logging

from enum import Enum
from dataclasses import dataclass

# log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    # filename="logfile.log",
    stream=sys.stdout,
    filemode="w",
    # format=log_Format,
    level=logging.INFO,
)


class ActivityType(Enum):
    Running = 0
    Cycling = 1
    Tennis = 2
    Pilates = 3
    Yoga = 4
    Circuits = 5
    Swimming = 6
    Weights = 7
    TeamSport = 8
    Other = 9


@dataclass
class Location:
    city: str
    region: str
    country: str


@dataclass
class Activity:
    date: datetime.date
    activity_type: ActivityType
    duration: datetime.timedelta
    distance: float
    location: Location

    @property
    def average_speed(self) -> float:
        return self.distance / self.duration.total_seconds() * 3600


def activity_test():
    my_activity = Activity(date=datetime.date(2023, 1, 18),
                           activity_type=ActivityType.Running,
                           duration=datetime.timedelta(minutes=29, seconds=31),
                           distance=4.66,
                           location=Location("Berkeley", "California", "USA"))
    logging.info(f"Average speed: {my_activity.average_speed: .2f} km/h")


if __name__ == "__main__":
    activity_test()
