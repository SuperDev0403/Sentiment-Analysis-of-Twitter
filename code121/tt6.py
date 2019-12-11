import matplotlib.pyplot as plt
import pandas as pd


result1 = []
df = pd.read_csv("/Users/nehajadhavsarnaik/Downloads/code121/Sentiment-Analysis-of-Twitter/Sentiment Analysis Dataset.csv")
xx = df["ItemID"]
for x in xx:
    print(x)
    result1.append(x)

result2 = []
yy = df["Sentiment"]
for y in yy:
    result2.append(y)

# x values
x = result1

# y values
y = result2

# plotting points as a scatter plot
plt.scatter(x, y, label="stars", color="green",marker="*", s=30)

# x label
plt.xlabel('x - ItemID')
# frequency label
plt.ylabel('y - Sentiment')
# plot title
plt.title('sentiment scatter plot!')

# showing legend
plt.legend()

# function to show the plot
plt.show()