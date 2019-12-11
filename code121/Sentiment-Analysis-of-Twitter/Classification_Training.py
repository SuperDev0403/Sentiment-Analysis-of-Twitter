import shutil
import nltk
from pyspark import SparkConf, SparkContext
from nltk.tokenize import word_tokenize
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel

if __name__ == "__main__":

    conf = SparkConf()
    conf.setAppName("SentimentAnalysis")
    cc = SparkContext(conf=conf)

    pos_data = cc.textFile("hdfs://master:9000/user/hadoop/pos_data.txt")
    neg_data = cc.textFile("hdfs://master:9000/user/hadoop/neg_data.txt")

    pos_data_sp = pos_data.flatMap(lambda line: line.split("\n")).collect()
    neg_data_sp = neg_data.flatMap(lambda line: line.split("\n")).collect()

    results_words = []
    results = []
    checked = ["J", "R", "V", "N"]

    for p in pos_data_sp:
        results.append({"text": p, "label": 1})

    for p in neg_data_sp:
        results.append({"text": p, "label": 0})

    def wc(data):
        words = word_tokenize(data)
        wf = nltk.pos_data_tag(words)
        for w in wf:
            if w[1][0] in checked:
                results_words.append(w[0].lower())
        return results_words


    record_data = cc.parallelize(results)
    raw_tokenized = record_data.map(lambda dic: {"text": wc(dic["text"]), "label": dic["label"]})

    htf = HashingTF(50000)
    record_hashed = raw_tokenized.map(lambda dic: LabeledPoint(dic["label"], htf.transform(dic["text"])))
    record_hashed.persist()

    trained_hashed, check_hashed = record_hashed.randomSplit([0.7, 0.3])

    NB_modeling = NaiveBayes.train(trained_hashed)
    NB_prediction = check_hashed.map(lambda point: (NB_modeling.predict(point.features), point.label))
    NB_right = NB_prediction.filter(lambda predicted, actual: predicted == actual)
    NB_accuracy = NB_right.count() / float(check_hashed.count())
    print ("NB training accuracy:" + str(NB_accuracy * 100) + " %")
    NB_output_dir = 'hdfs://master:9000/user/hadoop/NaiveBayes'
    shutil.rmtree("hdfs://master:9000/user/hadoop/NaiveBayes/metadata", ignore_errors=True)
    NB_modeling.save(cc, NB_output_dir)

    LR_model = LogisticRegressionWithLBFGS.train(trained_hashed)
    LR_prediction_and_labels = check_hashed.map(lambda point: (LR_model.predict(point.features), point.label))
    LR_correct = LR_prediction_and_labels.filter(lambda predicted, actual: predicted == actual)
    LR_accuracy = LR_correct.count() / float(check_hashed.count())
    print ("LR training accuracy:" + str(LR_accuracy * 100) + " %")
    LR_output_dir = 'hdfs://master:9000/user/hadoop/LogisticRegression'
    shutil.rmtree("hdfs://master:9000/user/hadoop/LogisticRegression/metadata", ignore_errors=True)
    LR_model.save(cc, LR_output_dir)

    SVM_model = SVMWithSGD.train(trained_hashed, iterations=10)
    SVM_prediction_and_labels = check_hashed.map(lambda point: (SVM_model.predict(point.features), point.label))
    SVM_model.clearThreshold()
    SVM_correct = SVM_prediction_and_labels.filter(lambda predicted, actual: predicted == actual)
    SVM_accuracy = SVM_correct.count() / float(check_hashed.count())
    print ("SVM training accuracy:" + str(SVM_accuracy * 100) + " %")
    SVM_output = 'hdfs://master:9000/user/hadoop/SVM'
    shutil.rmtree("hdfs://master:9000/user/hadoop/SVM/metadata", ignore_errors=True)
    SVM_model.save(cc, SVM_output)

    model = DecisionTree.trainClassifier(trained_hashed, numClasses=2, categoricalFeaturesInfo={},
                                         impurity='gini', maxDepth=5, maxBins=32)
    predictions = model.predict(check_hashed.map(lambda x: x.features))
    labelsAndPredictions = check_hashed.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(
        lambda lp: lp[0] != lp[1]).count() / float(check_hashed.count())
    print('Test Error = ' + str(testErr))
    print('Learned classification tree model:')
    print(model.toDebugString())
    model.save(cc, "hdfs:///user/hadoop/DT")

