import os
from keras.models import model_from_json
from keras.optimizers import Adam
import pandas as pd

HEIGHT = 128
WIDTH = 128

path_val = os.getcwd() + "\\dataset\\"

df=pd.read_csv("celeb.csv")
columns= [att for att in df.columns[1:]]


def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("best_model.h5")
    opt = Adam(lr = 0.0001)
    loaded_model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    return loaded_model

md_pred = load_model()


def predict(face):

    if face[0][0][0] > 1:    face = face / 255.

    prediction = list(md_pred.predict(face.reshape(1, HEIGHT, WIDTH, -1))[0])
    prediction = [round(v,2) for v in prediction]
    output = [(columns[i]  if i !=8 else "Beard", str(prediction[i]) if i !=8  else str(round(1 - prediction[i],2))) for i in list(range(len(prediction)))]
    m_f = output[6]; del output[6]
    m_f = ('M:'+str(m_f[1]),'F:'+str(round(1-float(m_f[1]),2)))
    output.insert(0,m_f)
    return output
