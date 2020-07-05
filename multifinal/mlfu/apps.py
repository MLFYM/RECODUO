from django.apps import AppConfig
from keras.models import load_model
from django.conf import settings
import keras
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

class MlfuConfig(AppConfig):
    name = 'mlfu'

sess = tf.Session()
set_session(sess)
print("**set_session 성공**")
Lgraph = tf.get_default_graph()
print("**get_default_graph 성공**")
Lmodel = load_model(settings.MODEL_ROOT + '/cnn0525(imagegenerator, 250, haar cascade).h5') #'/cnn0522(SeparableConv2D, minus1000)2.h5'
