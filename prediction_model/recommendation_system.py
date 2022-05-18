# importing libraries
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import scipy
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


# x = picture_detection('./data/test/test3')
# print(x)
print(1)

red_meat = ['beef', 'pork', ' goat', 'lamb', 'rabbit']
polutry = ['chicken', 'turkey']
sea_food = ['fish', 'crab', 'lobster', 'prawn', 'clam', 'oyster', 'scallop',
            'mussel']


def next_input(h):
    inpt = input('your desired food must be vegeterian? ')
    inpt = inpt.lower()
    if (inpt == 'yes'):
        res = h
    else:
        inpt_meat = input('what kind of meat your food should include? ')
        if (inpt_meat == 'red meat'):
            res = h.extend(red_meat)
        elif (inpt_meat == 'sea food'):
            res = h.extend(sea_food)
        elif (inpt_meat == 'polutry'):
            res = h.extend(polutry)
        elif (
            inpt_meat == 'red meat' and inpt_meat == 'polutry' and inpt_meat == 'sea food'):
            res = h.extend(red_meat, polutry, sea_food)
        else:
            res = h
    return res


recipes = [
    {'id': 123, 'title': 'random food 1', 'picture_link': 'fghjhjgdhgdgdgdgd'},
    {'id': 243, 'title': 'random food 2', 'picture_link': 'fghjhjgshgdgdgdgd'},
    {'id': 567, 'title': 'random food 3', 'picture_link': 'fghjhjghgadgdgdgd'},
]


@app.route('/getRecipes')
def get_incomes():
    return jsonify(recipes)


@app.route('/getRecipes', methods=['POST'])
def add_income():
    data = request.get_json()
    folderPath = "./data/uploads/" + data['folderName']
    prediction = picture_detection(folderPath)
    return jsonify(recipes)


app.run()
