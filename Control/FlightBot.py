import threading

from Control.Bot import Bot
from Model.constants import FLIGHTS_URL
import time
from datetime import datetime
from Model.FlightTable import Flight_table, By


class FlightBot(Bot):
    def __init__(self):
        super(FlightBot, self).__init__()
        self.thread_flag = True
        self.last_update = datetime.now()
        self.flight_table = Flight_table()

    """This function is used to start the Flight data extraction bot,
    it starts by getting to the corresponding flight website,check the last update time
    ,create a thread which checks the website table last update and update the data
    correspondingly,and start the data extraction for the first time"""

    def start(self):
        self.get(FLIGHTS_URL)
        self.last_update = datetime.strptime(
            self.find_element(By.ID, "lastUpdateTime").get_attribute('innerHTML'),
            '%H:%M')
        update_thread = threading.Thread(target=self.__check_time, daemon=True)
        self.__click_next()
        self.flight_table.update_data(self)
        update_thread.start()

    """This function is used to search the json file for specific keyword/s"""

    def search(self, keys):
        data = self.flight_table.search_json(keys)
        self.flight_table.print_df(data)
        return data
    """this function is used to save the table to json"""
    def save_data(self):
        self.flight_table.json_save()

    """This function is used to check each time the table updates , since the table
    updates each 60 seconds i let the thread which calls this function check the last update time in the website
     , if its more than the last update in the data update the flight table in the data,
     else sleep for 60 seconds."""

    def __check_time(self):
        while self.thread_flag:
            try:
                cur_time = datetime.strptime(self.find_element(By.ID, "lastUpdateTime").get_attribute('innerHTML'),
                                             '%H:%M')
                if self.last_update < cur_time:
                    self.flight_table.update_data(self)
                    self.last_update = cur_time
                time.sleep(60)
            except:
                pass

    """In order to see and download the entire flight table we need to nonstop press the 
    "see more" button which id is 'next' and click it until it disappears"""

    def __click_next(self):
        try:
            while True:
                next_btn = self.find_element(By.ID, 'next')
                next_btn.click()
        except:
            pass
