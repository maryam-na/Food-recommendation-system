# importing libraries
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import scipy
import psycopg2
from tensorflow import keras
from flask import Flask, jsonify, request

app = Flask(__name__)

test_df = pd.read_csv('./data/test_df.csv')
train_df = pd.read_csv('./data/train_df.csv')
# generating more images to fix our low number of images
# mobilenet_v2 is used to generate more images. a convolutional neural network which includes 53 layers. mobilenet_v2 is a pretrained model on more than a million images from the ImageNet database
generate_train = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=keras.applications.mobilenet_v2.preprocess_input)
generate_test = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=keras.applications.mobilenet_v2.preprocess_input)

# now fitting training, validation and test sets with it

train_images = generate_train.flow_from_dataframe(
    dataframe=train_df,
    x_col='imagepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=0,
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
)
test_images = generate_test.flow_from_dataframe(
    dataframe=test_df,
    x_col='imagepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=False
)


def img_store(imagepath):
    labels = []

    for i in range(len(imagepath)):
        labels.append(str(imagepath[i]).split("\\")[-2])

    imagepath = pd.Series(imagepath, name='imagepath').astype(str)
    labels = pd.Series(labels, name='Label')

    # Concatenate imagepaths and labels in a dataframe
    df = pd.concat([imagepath, labels], axis=1)
    df = df.sample(frac=1).reset_index(drop=True)
    return df


def picture_detection(imagepath):
    model = keras.models.load_model('./model/resnet_model_200.h5')
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    path_dir = Path(imagepath)
    pic_paths = list(path_dir.glob(r'**/*.jpg'))
    image = img_store(pic_paths)
    generate_image = tf.keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=keras.applications.mobilenet_v2.preprocess_input)

    images = generate_image.flow_from_dataframe(
        dataframe=image,
        x_col='imagepath',
        y_col='Label',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=32,
        shuffle=True,
        seed=0,
        rotation_range=30,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    prediction = model.predict(images)
    prediction = np.argmax(prediction, axis=1)
    labels = (train_images.class_indices)
    # labels = ["potato","grapes","onion","sweetcorn","soy beans","ginger","chilli pepper","spinach","pineapple","cucumber","apple","pear","lemon","corn","bell pepper","jalepeno","pomegranate","lettuce","capsicum","cauliflower","paprika","cabbage","peas","carrot","tomato","watermelon","orange","raddish","banana","eggplant","sweetpotato","kiwi","garlic","turnip","mango"]
    # labels = {'apple': 0, 'banana': 1, 'beetroot': 2, 'bell pepper': 3, 'cabbage': 4, 'capsicum': 5, 'carrot': 6, 'cauliflower': 7, 'chilli pepper': 8, 'corn': 9, 'cucumber': 10, 'eggplant': 11, 'garlic': 12, 'ginger': 13, 'grapes': 14, 'jalepeno': 15, 'kiwi': 16, 'lemon': 17, 'lettuce': 18, 'mango': 19, 'onion': 20, 'orange': 21, 'paprika': 22, 'pear': 23, 'peas': 24, 'pineapple': 25, 'pomegranate': 26, 'potato': 27, 'raddish': 28, 'soy beans': 29, 'spinach': 30, 'sweetcorn': 31, 'sweetpotato': 32, 'tomato': 33, 'turnip': 34, 'watermelon': 35}
    labels = dict((a, b) for b, a in labels.items())
    prediction = [labels[b] for b in prediction]
    return prediction


red_meat = ['beef', 'pork', 'goat', 'lamb', 'rabbit']
polutry = ['chicken', 'turkey']
sea_food = ['fish', 'crab', 'lobster', 'prawn', 'clam', 'oyster', 'scallop',
            'mussel']


def run_db_query(predictedPhotos, requestData):
    try:
        connection = psycopg2.connect(user="user",
                                      password="password",
                                      host="localhost",
                                      port="8432",
                                      database="recipe_db")
        cursor = connection.cursor()

        main_query = "select t.id, ingredients from ("
        sub_query_1 = "select recipe.id, string_agg(ingredient.name, ' ') ingredients from recipe join ingredient on recipe.id = ingredient.recipe_id where recipe.id in ("
        sub_query_2 = "select recipe_id from recipe join ingredient on recipe.id = ingredient.recipe_id where ingredient.name similar to '%"
        for photo in predictedPhotos:
            sub_query_2 += photo + "%|"

        sub_query_1 += sub_query_2 + "') group by recipe.id) t "

        main_query += sub_query_1

        if not requestData['vegetarian']:
            meat_query = "where t.ingredients similar to '%"
            if len(requestData['meatTypes']) > 0:
                if 'Red meat' in requestData['meatTypes']:
                    for item in red_meat:
                        meat_query += item + "%|"
                if 'Poultry' in requestData['meatTypes']:
                    for item in polutry:
                        meat_query += item + "%|"
                if 'Sea food' in requestData['meatTypes']:
                    for item in sea_food:
                        meat_query += item + "%|"
            main_query += meat_query + "'"
        else:
            meat_query = "where t.ingredients "
            for item in red_meat:
                meat_query += "not like '%" + item + "%' and t.ingredients "

            for item in polutry:
                meat_query += "not like '%" + item + "%' and t.ingredients "

            for item in sea_food:
                meat_query += "not like '%" + item + "%' and t.ingredients "

            meat_query = meat_query[:-18]
            main_query += meat_query

        main_query += " limit 10"

        cursor.execute(main_query)
        result = cursor.fetchall()
        return result

    except psycopg2.OperationalError as e:
        print("error happened!")
        print("Error while fetching data from PostgreSQL", e)

    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/getRecipes', methods=['POST'])
def add_income():
    data = request.get_json()
    folderPath = "./data/uploads/" + data['folderName']
    prediction = picture_detection(folderPath)
    db_result = run_db_query(prediction, data)
    ids = []
    for item in db_result:
        ids.append(item[0])

    idSet = set(ids)

    ids = list(idSet)

    return jsonify(ids)


app.run()
