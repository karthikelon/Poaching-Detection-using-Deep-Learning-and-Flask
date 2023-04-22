import os
from flask import Flask, render_template, request
import os
import cv2
import math
import matplotlib.pyplot
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import os
import imghdr
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from twilio.rest import Client
import requests


app = Flask(__name__)
target_folder = "E:\combinationofboth\images"

def is_target_folder(folder_path, target_folder):
    folder_path = os.path.abspath(folder_path)
    target_folder = os.path.abspath(target_folder)
    return folder_path == target_folder


@app.route('/', methods=['GET', 'POST'])
def upload_folder():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        if os.path.exists(folder_path):
            if is_target_folder(folder_path, target_folder):
                # Run machine learning model to detect poaching on images in the folder
                # Replace the code below with your actual machine learning model code
                new_model1 = load_model(os.path.join('models', 'poachingdetectionVER7.h5'))
                poacher = False
                person = int(0)
                noperson = int(0)
                solution = 0
                cwd = os.getcwd()
                print(cwd)
                os.chdir(r"E:\combinationofboth\images")
                # SMS INTEGRATION
                response = requests.get("http://ip-api.com/json/").json()
                message1 = " "
                message1 = "The region of poaching is " + \
                    response['region']+" "+response['city'] + " latitude is " + \
                    str(response['lat']) + " logitude is "+str(response['lon'])
                cwd = os.getcwd
                print(cwd)
                for picture in os.listdir():
                    if picture.endswith(".jpg"):
                        testingimg = cv2.imread(picture)
                        pic1 = tf.image.resize(testingimg, (256, 256))
                        solution = new_model1.predict(np.expand_dims(pic1, 0))
                    if solution > 0.5:
                        print(f'poacher is present warning')
                        print(picture)
                        poacher = True
                        person = person+1

                    else:
                        print(f'No poacher is present')
                        print(picture)
                        noperson = noperson+1
                print(person)
                print(noperson)
                finalmessage = True
                if (person > (person+noperson)*.10):
                    finalmessage = True
                else:
                    finalmessage = False
                print(finalmessage)
                outputinscreen = "Poaching is present and SMS REGARDING POACHING is sent to concerned authorities"
                if(finalmessage == True):
                    SID = ""
                    auth_token = ""

                    my_phone_number = ''
                    target_phone_number = ''

                    cl = Client(SID, auth_token)
                    if(poacher):
                        cl.messages.create(
                            body=message1, from_=my_phone_number, to=target_phone_number)

                    outputinscreen = "Poaching is present and SMS REGARDING POACHING is sent to concerned authorities"
                else:
                    outputinscreen = "Poaching is not present and animals are safe"
                return render_template('index.html', prediction=outputinscreen)
            #prediction = "Machine learning model detected poaching in the images in the selected folder."
            #return render_template('index.html', prediction=prediction)
        else:
            error = "Invalid folder path. Please try again."
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
