from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class Article:
    def __init__(self, url, title, driver):
        self.url = url
        self.driver = driver
        self.title = title
        self.contents = ""

    """This function is used to get the title of each article,
    which can be found as the child element of 'article' element
    on the website.
    if there is a problem , i want the title to be blank instead of gibberish
    so it will not interfere with the whole article"""

    def get_title(self, elem: WebElement):
        try:
            self.title = elem.find_element(By.TAG_NAME, 'header').text

        except:
            self.title = "BAD TITLE"

    """This function is used to close the popup which appears
    from time to time and can interfere with the data gathering"""

    def close_popup(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
        except:
            pass

    """This Function is used to get the contents of current article.
    it works in this manner: the webdriver moves to the current article website,
    finds the 'article' element by tag name,if there are more than 1 'article' element in the website
    it means that it's a live article and we need to read all the the article elements,after which
    it iterate all over the paragraph elements (TAG NAME 'p') and creates a final text
    which includes the entire article,and finally returns to the main page."""

    def get_contents(self):
        try:
            self.driver.get(self.url)
            article_body = self.driver.find_elements(By.TAG_NAME, "article")
            self.contents = self.title  # art-for article contents
            self.close_popup()
            flag = False
            if len(article_body) > 1:  # this if statment is in the case of a live article , which i noticed works a bit different#
                flag = True
            for body in article_body:
                if flag:
                    self.get_title(body)
                    self.contents += self.title + '\n\n'
                for para in body.find_elements(By.TAG_NAME, "p"):
                    self.contents += para.text + "\n"
                self.contents += "\n----------------------------------------------------\n"
            self.driver.back()
        except:
            self.contents = "bad"  # incase the data extraction fails because of any reason, we want a blank article rather than half

    """this function is used to serialize the article inorder to save it as txt"""

    def serialize(self):
        full = (f"\nURL:{self.url}\n\n" + self.contents + "\n")
        full += "------------------------------------------------------------------------------------------------"
        return full
