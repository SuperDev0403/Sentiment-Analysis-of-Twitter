import pandas as pd
import matplotlib.pyplot as plt
from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession

result1 = []
df = pd.read_csv("/Users/nehajadhavsarnaik/Downloads/code121/Sentiment-Analysis-of-Twitter/Sentiment Analysis Dataset.csv")
xx = df["SentimentSource"]
for x in xx:
    print(x)
    result1.append(x)
plt.plot(result1)
plt.show()