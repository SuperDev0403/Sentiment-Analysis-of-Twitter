import matplotlib.pyplot as plt
import pandas as pd


result1 = []
df = pd.read_csv("/Users/nehajadhavsarnaik/Downloads/code121/Sentiment-Analysis-of-Twitter/Sentiment Analysis Dataset.csv",low_memory=False)
xx = df["ItemID"]
for x in xx:
    result1.append(x)

result2 = []
yy = df["Sentiment"]
ages = yy

# setting the ranges and no. of intervals
range = (0, 5000)
bins = 10


plt.hist(ages, bins, range, color='green', histtype='bar', rwidth=0.8)

plt.xlabel('sentiment')
# frequency label
plt.ylabel('count of sentiment')
# plot title
plt.title('My sentiment')

plt.show()