
from nltk.classify import NaiveBayesClassifier

def word_feats(words):
    return dict([(word, True) for word in words])

words_pos_counti = ['awesome','outstanding','fantastic','good','terrific','nice','great',':)']
words_neg_counta = ['useless','bad','terrible',':(','hate']
words_neutral = ['movie','sound','was','words','the','actors','is', 'did','know','not']

pos_counti_features1 = [(word_feats(pos_count), 'pos_count') for pos_count in words_pos_counti]
neg_counta_features2 = [(word_feats(neg_count), 'neg_count') for neg_count in words_neg_counta]
neutral_features3 = [(word_feats(neu), 'neu') for neu in words_neutral]

print("pos_counti_features1: ", pos_counti_features1)
print("neg_counta_features2: ", neg_counta_features2)
print("neutral_features3: ", neutral_features3)

train_set_va = neg_counta_features2 + pos_counti_features1 + neutral_features3
classifier_va = NaiveBayesClassifier.train(train_set_va)

print("train_set_va: " , train_set_va)
print("classifier_va: " , classifier_va)

# Predict
neg_count = 0
pos_count = 0
sentence = "Awesome movie, I liked it"
sentence = sentence.lower()
key_words = sentence.split(' ')
for word in key_words:
    classResult = classifier_va.classify(word_feats(word))
    if classResult == 'neg_count':
        neg_count = neg_count + 1
    if classResult == 'pos_count':
        pos_count = pos_count + 1

print('pos_countitive result: ' + str(float(pos_count) / len(key_words)))
print('neg_countative result: ' + str(float(neg_count) / len(key_words)))