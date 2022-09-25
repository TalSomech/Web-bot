from selenium import webdriver
from selenium.webdriver.chrome.options import Options

""""This is a main class which both Flight and BBC bots classes derive from,
its used to define the options of the web driver , the options marked in the comments
are used so the chrome app wont load everytime i activate the program"""


class Bot(webdriver.Chrome):
    def __init__(self, driver_path=r"/"):
        self.driver_path = driver_path
        # chrome_options=Options()
        # chrome_options.add_argument("--headless")
        # super(Bot, self).__init__(chrome_options=chrome_options)
        super(Bot, self).__init__()
        self.implicitly_wait(1)
