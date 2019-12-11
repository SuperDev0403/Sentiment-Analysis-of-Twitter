from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import socket
from pyspark.sql import SQLContext
from pyspark.sql import Row
import sys
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from nltk.classify import ClassifierI
from statistics import mode


class VoteClassifier(ClassifierI):

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, transformer):
        votes = []
        for c in self._classifiers:
            v = c.predict(transformer)
            votes.append(v)
        return mode(votes)


conf = SparkConf()
conf.setAppName("TA")
sc = SparkContext(conf=conf)
tre = StreamingContext(sc, 10)
htf = HashingTF(50000)

NB_directory = 'hdfs://master:9000/user/hadoop/NaiveBayes'
NB_model = NaiveBayesModel.load(sc, NB_directory)

LR_directory = 'hdfs://master:9000/user/hadoop/LogisticRegression'
LR_model = LogisticRegressionModel.load(sc, LR_directory)

DT_output_dir = 'hdfs://master:9000/user/hadoop/DT'
DT_model = DecisionTreeModel.load(sc, DT_output_dir)

voted_classifier = VoteClassifier(NB_model, LR_model, DT_model)


def sentiment(test_sample):
    sample_data_test= test_sample.split(" ")
    cli = htf.transform(sample_data_test)
    return voted_classifier.classify(cli)


lines = tre.socketTextStream(socket.gethostbyname(socket.gethostname()), 10000)
lines.pprint()
tweets = lines.flatMap(lambda text: [(text)])
tweets.pprint()


def s(rdd):
    r3 = rdd.collect()
    r1 = map(lambda f: (f, sentiment(f)), r3)
    r5 = sc.parallelize(r1)
    process_rdd(r5)


def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


def process_rdd(rdd):
    try:

        sql_context = get_sql_context_instance(rdd.context)

        row_rdd = rdd.map(lambda w: Row(text=w[0], senti=w[1]))

        df_hashtags = sql_context.createDataFrame(row_rdd)
        print (df_hashtags.collect())

        df_hashtags.registerTempTable("hashtags")

        counts_df_hashtag = sql_context.sql("select text, senti from hashtags")

        counts_df_hashtag.show()

    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


tweets.foreachRDD(lambda r: s(r))
tre.start()
tre.awaitTermination()
