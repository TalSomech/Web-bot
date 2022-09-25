from Model.FlightData import Flight, FLIGHT_DATA, By
from Model.constants import FLIGHTS_TABLE
import json
import pandas as pd
import threading


class Flight_table():
    def __init__(self):
        self.table = []

    """"This function is used to convert the list of flight objects
    into a pandas dataframe for easier search,handling and viewing of the data
    it is static since we sometimes want to convert only some of the table and not the entire table
    like when searching for a keyword"""

    """This function is used to update the flights table and data,
    since it needs to be updated every time the website updates it
    i used a thread lock so the main and the update thread wont collide,
    as the website continuously updates the table, the elements in the website can disappear
    and so we toggle the auto uMessage: invalid session id
    date to stop,than the function finds all the flight rows
    in the website by class name 'flight_row',iterate over each row and creates a Flight objects
    until finally load it into a flight table object and saved as json"""

    def update_data(self, driver):
        lock = threading.Lock()
        lock.acquire()
        try:
            driver.find_element(By.ID, "toggleAutoUpdate").click()
            flight_rows = driver.find_elements(By.CLASS_NAME, "flight_row")
            for fl in flight_rows:
                self.table.append(Flight.from_web(fl))
            self.json_save()
        except Exception as e:
            print(e)
        finally:
            lock.release()
            driver.find_element(By.ID, "toggleAutoUpdate").click()

    """function which is used to find specific keyword/s in the
    json file , it works as such : 
    loads the entire json and converts it into a list of flight objects
    than iterate over the list and search the keyword the flight info ,
    if found it will add all the corresponding objects to the list and returns the list."""

    def search_json(self, keys):
        self.json_load()
        keys = [keys]
        out = []
        for fl in self.table:
            for data in FLIGHT_DATA:
                for key in keys:
                    if key in fl.info[data]:
                        out.append(fl)
        return out

    """"Used to save the list of Flight objects into json"""

    def json_save(self):
        with open(FLIGHTS_TABLE, 'w', encoding='utf-8') as file:
            json_string = json.dumps(self.table, default=Flight.serialize, indent=4)
            file.write(json_string)

    """Used to load a list of flight objects from a json file"""

    def json_load(self):
        with open(FLIGHTS_TABLE, 'r') as file:
            self.table = json.loads(file.read(), object_hook=lambda f: Flight(f))


    @staticmethod
    def to_pandas(flights):
        rows = {'airline': [], 'flight': [], 'city': [], 'terminal': [], 'scheduledTime': [],
                'updatedTime': [], 'status': []}
        for fl in flights:
            for data in FLIGHT_DATA:
                rows[data].append(fl.info[data])
        return pd.DataFrame.from_dict(rows)

    """"This function prints the pandas table,it is static since we sometimes want to convert only some of the table
     and not the entire table like when searching for a keyword"""

    @staticmethod
    def print_df(flights):
        flight_df = Flight_table.to_pandas(flights)
        print(flight_df.to_string())
