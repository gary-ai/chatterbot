import numpy as np

from chatbot import clean_up_sentence
from chatbot import bow
from chatbot import classify
from chatbot import chat_response


def test_clean_up_hello_sentence_():
    assert clean_up_sentence("Hi, HoW are you?!") == ['hi', ',', 'how', 'ar', 'you', '?', '!']


def test_bow_with_no_equality_():
    assert bow("test", ["plop"]) == [0]


def test_bow_with_one_equality_():
    assert bow("test", ["test"]) == [1]


def test_classify_greeting_sentence_():
    assert classify("Hi")[0][0] == "greeting"


def test_classify_shutter_sentence_():
    assert classify("bye")[0][0] == "goodbye"


def test_classify_camera_sentence_():
    assert classify("camera")[0][0] == "take_photo"


def test_classify_light_sentence_():
    assert classify("light")[0][0] == "hue"


def test_classify_type_greeting_():
    assert type(classify("hi")[0][1]) == np.float32


def test_classify_type_thanks_():
    assert type(classify("thanks")[0][1]) == np.float32


def test_classify_type_hue_():
    assert type(classify("hue")[0][1]) == np.float32


def test_classify_type_rollers_():
    assert type(classify("rollers")[0][1]) == np.float32


def test_chat_greeting_response_():
    assert chat_response("Hi, HoW are you?!") == "Good to see you again" or "Hello, thanks for visiting" \
           or "Hi there, how can I help?"


def test_chat_camera_response_():
    assert chat_response("camera") == "exec camera_photo"


def test_chat_thanks_response_():
    assert chat_response("thanks") == "Happy to help!" or "Any time!" or "My pleasure"


def test_chat_light_response_():
    assert chat_response("philips hue") == "Ok, what mood do you want ?"


def test_contextual_hue_response_():
    assert chat_response("philips hue") == "Ok, what mood do you want ?"
    assert chat_response("relax") == "exec hue_relax"


def test_contextual_rollers_response_():
    assert chat_response("rollers") == "Ok, do you want to open, close or stop ?"
    assert chat_response("open") == "exec open_shutter"
