import tweepy
import numpy as np
import pandas as pd
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS


df = pd.read_csv("/Users/nehajadhavsarnaik/Downloads/code121/Sentiment-Analysis-of-Twitter/Sentiment Analysis Dataset.csv", low_memory=False)

all_tweets = ' '.join(str(tweet) for tweet in df['SentimentText'])
wordcloud = WordCloud(stopwords=STOPWORDS).generate(all_tweets)

plt.figure(figsize = (10,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



# f = pd.DataFrame(columns = ['Tweets', 'User', 'User_statuses_count',
#                              'user_followers', 'User_location', 'User_verified',
#                              'fav_count', 'rt_count', 'tweet_date'])

#
# df_popular = df[df['ItemID'] <= 100]
# df_popular['Sentiment'].value_counts().iplot(kind='bar', xTitle='Sentiment',yTitle='Count', title = 'Sentiment Distribution for <br> popular tweets (Above 50k)')
# df.show()