from Control.Bot import Bot
from Model.BBCTable import BBC_table, By
from Model.constants import BBC_URL


class BBCbot(Bot):
    def __init__(self):
        super(BBCbot, self).__init__()
        self.get(BBC_URL)
        self.table = BBC_table()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    """loads the data and articles from the website"""

    def get_data(self):
        links = self.__get_links()
        return self.table.data_extract(self, links)

    """searches all the articles for said keyword/s"""

    def search(self, keys):
        df = self.table.search(keys)
        titles = df['Title'].tolist()
        urls = df['URL'].tolist()
        for url, title in zip(urls, titles):
            print(f'URL: {url} Title: {title} \n')
        return df

    """a function used to save the dataframe"""

    def save_table(self):
        self.table.save_dataframe()

    def load_table(self):
        return self.table.load_dataframe()

    """This function is used to iterate over all the 'li' elements in BCC.com website
    and get the links and headlines of every article , i however noticed that there are some sections
    which arent news , so i only want the articles with '/news/' in their urls
    """

    def __get_links(self):
        articles = self.find_elements(By.TAG_NAME, "li")
        links = []
        for art in articles:
            try:
                url = art.find_element(By.CSS_SELECTOR, 'a[class$="link"]').get_attribute("href")
                if ("/news/" in url) or ("/article/" in url):
                    links.append((url, art.text))
            except:
                pass
        return links
