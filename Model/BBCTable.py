from Model.Article import Article, By
import pandas as pd
import numpy as np


class BBC_table():
    def __init__(self):
        self.table = pd.DataFrame()

    """This function is used to extract the data from the website and each article,
    it first get all the article links and iterate over them , for each
    article it creates an Article object and get its contents which afterwards add to the bbc dataframe
    and finally saves the whole data as text file and csv file,it returns the bbc dataframe
    for the nlp use."""

    def data_extract(self, driver, articles):
        data = {'Title': [], 'URL': [], 'Text': []}
        final_text = ""
        for url, title in articles:
            try:
                art_obj = Article(url, title, driver)
                art_obj.get_contents()
                if title == '':# this if statement is since some of the titles arent possible to get.
                    title = "BAD TITLE"
            except:
                continue
            data['Title'].append(title.strip())
            data['URL'].append(url)
            data['Text'].append(art_obj.contents)
            final_text += art_obj.serialize()
        self.table = pd.DataFrame.from_dict(data)
        BBC_table.save_file(final_text)
        self.save_dataframe()
        self.table.drop(self.table.loc[self.table['Text'] == "bad"], axis=1)# some of the articles are bad Text so we need to drop them
        return self.table

    """function which is used to find specific keyword/s in the
    json file , it works as such : 
    search the entire dataframe and searches for rows with correpsonding keys 
    and return a new dataframe with only said articles"""

    def search(self, keys):
        keys = [keys]
        mask = np.column_stack([self.table[col].str.contains(*keys) for col in self.table])
        df = self.table.loc[mask.any(axis=1)]
        return df

    """function used to load the dataframe from csv"""

    def load_dataframe(self):
        self.table = pd.read_csv("BBC_articles.csv")
        self.table = self.table.drop(self.table.columns[0], axis=1)
        return self.table

    """This function is used to save the bbc dataframe into csv for comfort and maybe future use"""

    def save_dataframe(self):
        self.table.to_csv("BBC_articles.csv")

    @staticmethod
    def save_file(articles):
        with open("BBC articles", "w", encoding="utf-8") as file:
            file.write(articles)
            file.close()
