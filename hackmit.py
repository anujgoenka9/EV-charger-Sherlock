import numpy as np
from fastapi import FastAPI, Form
import pandas as pd
import tensorflow as tf
import csv
from starlette.responses import HTMLResponse
app = FastAPI()


def getArray():
    results = []
    with open("TEST_corrected.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            results.append(row)
    b = np.array(results)
    return b


def getAccuracy(array):
    COORDINATES_corrected = pd.read_csv("COORDINATES_corrected.csv")
    final = pd.DataFrame(columns=['Accuracy', 'Latitude', 'Longitude'])
    for num in range(0, 26909):
        final = final.append(pd.Series([array[num][0], COORDINATES_corrected['Latitude'][num], COORDINATES_corrected['Longitude'][num]], index=[
            'Accuracy', 'Latitude', 'Longitude']), ignore_index=True)
    final = final.sort_values(by=['Accuracy'], ascending=False)
    return final


def give_output(input_value, final):
    arr = []
    for i in range(0, input_value):
        arr.append([final['Latitude'][i], final['Longitude'][i]])
    return arr


@app.post('/api')  # prediction on data
def predict(noOfEvs: int = Form(...)):  # input is from forms
    get_array = getArray()
    loaded_model = tf.keras.models.load_model(
        'hackmit.h5')  # loading the saved model
    predictions_array = loaded_model.predict(get_array)  # making predictions
    accuracy = getAccuracy(predictions_array)
    output = give_output(noOfEvs, accuracy)
    return {
        "Output": output  # returning a dictionary as endpoint
    }

@app.get('/api', response_class=HTMLResponse)  # data input by forms
def take_inp():
    return '''<form method="post"> 
    <input type="number" name="noOfEvs" value="20"/>  
    <input type="submit"/> 
    </form>'''