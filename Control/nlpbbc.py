from nltk.sentiment.sentiment_analyzer import SentimentAnalyzer
from transformers import pipeline
import spacy
from textblob import TextBlob
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration

"""This function is used to summarize the text of each article,it uses the T5 transformer in order to summarize
which is a pretrained model,for each article in the dataframe it strips and replace \n to '' in the text"""


def summarize(data: pd.DataFrame):
    articles = data['Text'].tolist()
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    summaries = []
    for article in articles:
        article = article.strip().replace("\n", "")
        summaries.append(__article_sum(article, model, tokenizer))
    return summaries


"""This function iterates over the text of each article and checks the sentiment analysis of the article
and adds it to the list"""


def sentiment_analysis(data: pd.DataFrame):
    articles = data['Text'].tolist()
    analysis = []
    for article in articles:
        article = article.strip().replace("\n", " ")
        analysis.append(__article_analysis(article))
    data['analysis'] = analysis
    print(data.to_string())
    return data


""""This function uses the T5 model and tokenizer inorder to encode and decode the text
to get the most important features and summarize the text"""


def __article_sum(article, model, tokenizer):
    t5_prepared_text = "summarize: " + article
    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt")
    summary_ids = model.generate(tokenized_text,
                                 num_beams=4,
                                 no_repeat_ngram_size=2,
                                 min_length=30,
                                 max_length=100,
                                 early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


"""This function uses the spacy and text blob libraries inorder to analyse the sentiment of an article
it works by splitting the entire article text into sub sentences (like paragraphs) , compute the sentiment polarity of
each sentence (ranges from [-1,1]) , adds it to a certain score , and the final score decides the sentiment of 
the entire article"""


def __article_analysis(article):
    nlp = spacy.load("en_core_web_sm")
    sentence = []
    tokens = nlp(article)
    for sent in tokens.sents:
        sentence.append(sent.text)
    score = 0
    for s in sentence:
        txt = TextBlob(s)
        score += txt.polarity
    return __find_sentiment(score)


"""This function converts the sentiment polarity score of the article into categorial """


def __find_sentiment(sentiment_score):
    if sentiment_score > 0:
        return "POSITIVE"
    elif sentiment_score < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"
