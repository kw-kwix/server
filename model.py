from keras.models import load_model, Model
import numpy as np


def scalered_height(height):
    return (height-170)/30


def scalered_wight(weight):
   return (weight-70)/30


def scalered_sex(sex):
   return sex/2


def scalered_bmi(bmi):
   return (bmi-30)/30


def scalered_proficiency(proficiency):
   return (proficiency-170)/30


def input(height, weight, sex, bmi, proficiency):
    return np.array([height, weight, sex, bmi, proficiency])


def predict(x):

   model: Model = load_model("chest_model.h5")
   y = model.predict(x)
   return y
