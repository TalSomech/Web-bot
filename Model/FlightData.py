from Model.constants import FLIGHT_DATA
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Flight:
    def __init__(self, flight_info):
        self.info = flight_info
        pass

    """Used to serialize the object into a json object"""

    def serialize(self):
        return self.info

    """This function is used to create a Flight object from website data
    by iterating over all the sub-element of 'flight_row' element in the website
    and gather the innerText attribute"""

    @staticmethod
    def from_web(flight: WebElement):
        info = {}
        for data in FLIGHT_DATA:
            info[data] = flight.find_element(By.CLASS_NAME, f'td-{data}').get_attribute("innerText")
        return Flight(info)

    """This function is used to create a Flight object from json object by iterating over the data
    and creating the flight information dict"""

    @staticmethod
    def from_json(flight):
        info = {}
        for data in FLIGHT_DATA:
            info[data] = flight[data]
        return Flight(info)
