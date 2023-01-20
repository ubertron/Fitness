#! /usr/bin/env python3

import sys
import datetime
import logging
import pickle
import os
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

import logging_utils

from enum import Enum
from dataclasses import dataclass
from typing import List


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

    def __repr__(self) -> str:
        return f"{self.city}, {self.region}, {self.country}"


@dataclass
class Activity:
    date: datetime.date
    activity_type: ActivityType
    duration: datetime.timedelta
    distance: float
    location: Location

    def __repr__(self) -> str:
        info = f"{self.activity_type.name} [{self.location}] {self.date_string} | time: {self.duration}"
        if self.distance > 0:
            info += f" | distance: {self.distance} km | average speed: {self.average_speed: .2f} km/h"
        return info

    @property
    def average_speed(self) -> float:
        return self.distance / self.duration.total_seconds() * 3600

    @property
    def date_string(self) -> str:
        return self.date.strftime('%Y_%m_%d')

    @property
    def name(self) -> str:
        return f"{self.activity_type.name}_{self.date_string}.activity"


class ActivityManager:
    DATA_FOLDER = "activities"

    def __init__(self):
        pass

    @property
    def activities(self):
        return [self.load(x) for x in self.activity_files]

    def load(self, activity_file: str) -> Activity:
        file_path = os.path.join(self.DATA_FOLDER, activity_file)
        activity = pickle.load(open(file_path, "rb"))
        return activity

    @property
    def activity_files(self) -> List[str]:
        return [file for file in os.listdir(self.DATA_FOLDER) if file.endswith(".activity")]

    def add_activity(self, *args, **kwargs):
        activity = Activity(*args, **kwargs)
        self.save(activity)

    def save(self, activity: Activity):
        if not os.path.isdir(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)
        pickle.dump(activity, open(os.path.join(self.DATA_FOLDER, activity.name), "wb"))

    def format_activities(self):
        for x in self.activities:
            logging.info(x)

    @property
    def running_activities(self) -> List[Activity]:
        return [x for x in self.activities if x.activity_type == ActivityType.Running]

    def plot_running(self):
        plt.bar([x.date for x in self.running_activities],
                [x.average_speed for x in self.running_activities])
        plt.show()


def add_activities():
    activity_manager = ActivityManager()
    data = [datetime.date(2023, 1, 18), ActivityType.Running, datetime.timedelta(minutes=29, seconds=31), 4.66,
            Location("Berkeley", "California", "USA")]
    activity_manager.add_activity(*data)
    data = [datetime.date(2022, 12, 11), ActivityType.Running, datetime.timedelta(minutes=32, seconds=40), 5.01,
            Location("Bingley", "West Yorkshire", "UK")]
    activity_manager.add_activity(*data)
    data = [datetime.date(2022, 12, 23), ActivityType.Running, datetime.timedelta(minutes=26, seconds=2), 3.6,
            Location("Bingley", "West Yorkshire", "UK")]
    activity_manager.add_activity(*data)
    activity_manager.format_activities()


if __name__ == "__main__":
    # add_activities()
    ActivityManager().plot_running()
