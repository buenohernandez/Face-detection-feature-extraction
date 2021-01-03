from keras.models import model_from_json
from keras.optimizers import Adam
import pandas as pd
from tensorflow.keras.metrics import BinaryAccuracy, Precision, Recall
import cv2

HEIGHT = 128
WIDTH = 128

df=pd.read_csv("celeba.csv")

columns= df.columns[1:]

def load_model():
    json_file = open('features_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("features_best_model.h5")
    opt = Adam(lr = 0.0001)
    loaded_model.compile(loss='binary_crossentropy', optimizer=opt, metrics=[BinaryAccuracy(), Precision(), Recall()])

    json_file = open('hair_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model2 = model_from_json(loaded_model_json)
    loaded_model2.load_weights("hair_best_model.h5")
    opt = Adam(lr = 0.0001)
    loaded_model2.compile(loss='categorical_crossentropy', optimizer=opt, metrics=[BinaryAccuracy(), Precision(), Recall()])

    return loaded_model, loaded_model2

features_pred, hair_pred = load_model()


def predict(face):

    if face[0][0][0] > 1:    face = face / 255.
    if face.shape[0] != WIDTH or face.shape[1] != HEIGHT:   face = cv2.resize(face, (WIDTH, HEIGHT))

    prediction = list(features_pred.predict(face.reshape(1, HEIGHT, WIDTH, -1))[0])
    prediction = [round(v,2) for v in prediction]

    columns_features = columns[5:]
    output = [(columns_features[i]  if i !=3 else "Beard", str(prediction[i]) if i !=3  else str(round(1 - prediction[i],2))) for i in list(range(len(prediction)))]

    m_f = output[1]; del output[1]
    m_f = ('M:'+str(m_f[1]),'F:'+str(round(1-float(m_f[1]),2)))
    output.insert(0,m_f)

    prediction = list(hair_pred.predict(face.reshape(1, HEIGHT, WIDTH, -1))[0])
    prediction = [round(v,2) for v in prediction]

    columns_hair = columns[:5]
    output2 = [(columns_hair[i], str(prediction[i])) for i in list(range(len(prediction)))]

    return output + output2


