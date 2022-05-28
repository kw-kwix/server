from keras.models import load_model, Model
import numpy as np
import mongo


def scalered_height(height):
    return (int(height)-170)/30


def scalered_weight(weight):
   return (int(weight)-70)/30


def scalered_sex(sex):
   return int(sex)/2


def scalered_age(age):
   return (int(age)-30)/30


def scalered_bmi(bmi):
   return (int(bmi)-30)/30


def scalered_proficiency(proficiency):
   return (int(proficiency)/3)


def input_data(height, weight, sex, age, bmi, proficiency):
    return np.array([height, weight, sex, age, bmi, proficiency])


def predict(x):

   model: Model = load_model("chest_model.h5")
   y = model.predict(x)
   y = np.around(y.flatten(), 3)
   return y


def get_excercise_list():
   return np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]])


def recommend(user_input):
   exercise_list = get_excercise_list()

   user_input[1] = scalered_height(user_input[1])
   user_input[2] = scalered_weight(user_input[2])
   user_input[3] = scalered_sex(user_input[3])
   user_input[4] = scalered_age(user_input[4])
   user_input[5] = scalered_bmi(user_input[5])
   user_input[6] = scalered_proficiency(user_input[6])

   return predict([np.array([input_data(user_input[1], user_input[2], user_input[3],
                                        user_input[4], user_input[5], user_input[6])]), exercise_list])


if __name__ == "__main__":
   from pymongo.mongo_client import MongoClient
   from config import MONGO_URL

   client = MongoClient(MONGO_URL)
   KWIX = client.KWIX

   id = input("id:")
   user_input = mongo.get_user(KWIX, id)[0]
   result = recommend(user_input)
   print(result)
