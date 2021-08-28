# Nahom Ketema
'''
This is the part of the program where api calls are done.
'''
import requests
from datetime import date, datetime
import time
from textblob import TextBlob
import plotly.express as px

#API Keys below
alphavantage_api_key = "YH4KR847HP6RMI4Q"
twitter_bearer_token = "AAAAAAAAAAAAAAAAAAAAAIiESwEAAAAAkv%2BmuzDlEAuhs88e7uj1qV%2B%2BEB0%3DHxcycitfog1TYKZyetEiwpyj2pIfnZ3oOuAKcHvtZXv5JbzuRe"

#Alphavantage API calls below
def search_tickers(searchname):
    search_json = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="+searchname+"&apikey="+alphavantage_api_key).json()
    try:
        search_json["bestMatches"]
    except Exception as e:
        print("no matches found")
        return []
    matches = []
    for search_match in search_json["bestMatches"]:
        match_dict = {}
        match_dict["name"] = search_match["2. name"]
        match_dict["region"] = search_match["4. region"]
        match_dict["ticker symbol"] = search_match["1. symbol"]
        matches.append(match_dict.copy())
    return matches

# This only gets used when saving
def find_name_from_ticker(tickername):
    # returns the name if found but if not, this function returns back a ""
    matches = search_tickers(tickername)
    if(matches == []):
        return ""
    for match in matches:
        if(match["ticker symbol"] == tickername):
            return match["name"]
    return ""

def recent_value(ticker_name):
    #This is to be used for data visualization of a ticker. Note that this only goes back one day
    recent_json = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+ticker_name+"&interval=5min&apikey="+alphavantage_api_key).json()
    #to parse the data you can do a "  for val in recent_json["Time Series (5min)"].keys():  "
    parsed_data = {}
    parsed_data["last updated"] = recent_json["Meta Data"]["3. Last Refreshed"]
    parsed_data["interval"] = recent_json["Meta Data"]["4. Interval"]
    ticker_value = recent_json["Time Series ("+parsed_data["interval"]+")"]
    parsed_data["values"] = []
    for key in ticker_value.keys():
        value_dict = {}
        value_dict["time"] = key
        value_dict["high"] = ticker_value[key]["2. high"]
        value_dict["low"] = ticker_value[key]["3. low"]
        value_dict["volume"] = ticker_value[key]["5. volume"]
        parsed_data["values"].append(value_dict.copy()) # makes a copy because otherwise all added dicts will get overwritten
    return parsed_data

#Twitter API calls below
twitter_headers = {
    'Authorization': "Bearer " + twitter_bearer_token
}

def one_day_ago():
    #This returns 
    time_yesterday_in_seconds = time.time() -86400 #86400 is 24 hours in seconds
    date_yesterday = str(datetime.fromtimestamp(time_yesterday_in_seconds))
    date_yesterday = date_yesterday[:10]
    return date_yesterday

def twitter_search_hashtag(tickersymbol):
    #The %23 in the request refers to the '#' symbol
    data_json = requests.get("https://api.twitter.com/2/tweets/search/recent?query=%23"+tickersymbol+"&max_results=10&start_time="+one_day_ago()+"T00:00:00.00Z", headers=twitter_headers).json()
    if(data_json["data"] == []):
        return []
    tweets = []
    for data in data_json["data"]:
        tweets.append(data["text"])
    return tweets

def sentiment_analysis(text):
    sum = 0
    count = 0
    sentences = TextBlob(text).sentences
    for sentence in sentences:
        sum += sentence.sentiment.polarity
        count += 1
    try:
        average = sum/count
    except Exception as e:
        return 0
    else:
        return average

def generate_graph(data):
    x = []
    y = []
    for price in data["values"]:
        x.append(price["time"])
        y.append((float(price["high"])+float(price["low"]))/2)
    fig = px.line(x=x, y=y)
    fig.write_html('static/pages/figure.html') # export to HTML file


#Testing below
#generate_graph(recent_value("tsla"))