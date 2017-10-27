import numpy as np
import tflearn
import tensorflow as tf
import pickle
import random
import nltk
from pymongo import MongoClient
from nltk.stem.lancaster import LancasterStemmer


# restore all of our data structures
data = pickle.load(open("training_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents data from mongo
connection = MongoClient("mongodb://mongo:27017")
db = connection.gary_db
intents = db.intents.find()

# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# load our saved model
model.load('./model.tflearn')


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    stemmer = LancasterStemmer()
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, local_words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(local_words)
    for s in sentence_words:
        for i, w in enumerate(local_words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return np.array(bag)


context = {}
ERROR_THRESHOLD = 0.25


def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list


def chat_response(sentence, user='1', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details:
                            print ('context:', i['context_set'])
                        context[user] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if 'context_filter' not in i or \
                            (user in context and 'context_filter' in i and i['context_filter'] == context[user]):
                        if show_details:
                            print ('tag:', i['tag'])
                        # a random response from the intent
                        return random.choice(i['responses'])
            results.pop(0)
