from mtcnn.mtcnn import MTCNN
import os
import numpy as np
from PIL import Image
import cv2
import sys
from model import predict

font = cv2.FONT_HERSHEY_SIMPLEX
path = os.getcwd()
detector = MTCNN()

class MTC:
    def extract_face(self, filepath):
        print(filepath)
        image = Image.open(filepath)

        if image.size[0] * image.size[1] > 1024 * 768:    image = image.resize((int(image.size[0]*0.5),int(image.size[1]*0.5)),Image.LANCZOS)

        image = np.asarray(image)[:,:,:3]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(image)
        fcs = len(results)
        data_h = 350

        if image.shape[0] > data_h:
            dt_h = image.shape[0]
            frame_bool = False
        else:
            dt_h = data_h
            frame = np.ones((data_h - image.shape[0], image.shape[1], 3)) * 255
            frame_bool = True

        data = np.ones((dt_h, 160 * fcs, 3)) * 255

        for i in list(range(fcs)):
            try:
                x1, y1, width, height = results[i]['box']
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                x1 -= int(width * (18/85))
                y1 -= int(height * (30/120))
                x2 += int(width * (18/85))
                y2 += int(height * (10/120))
                face = image[y1:y2, x1:x2]
                face = Image.fromarray(face)
                face = np.asarray(face.resize((128,128), Image.LANCZOS)) #OpenCV resize has a bug with big images
                cv2.rectangle(image, (x1,y1),(x2,y2), (0,0,255), 1)
                cv2.putText(image, str(i),(x1,y1), font, 0.5, (255,255,255),5)
                cv2.putText(image, str(i),(x1,y1), font, 0.5, (0,0,0), 2)
                cv2.putText(data, str(i),((10+i*160),25), font, 0.5, (0,0,0), 2)
                predictions = predict(face)

                for j in list(range(len(predictions))):
                    cv2.putText(data, "{} {}".format(predictions[j][0], predictions[j][1]),((10+i*160),50+j*25), font, 0.5,(0,0,0), 1)

            except Exception as e:
                print(e)

        if frame_bool:    image = np.concatenate((image, frame), 0)

        output = np.concatenate((image, data), 1)

        return output

if __name__ == '__main__':
    mtc = MTC()
    filepath = sys.argv[1]
    image = mtc.extract_face(filepath)
    filepath = filepath.replace('./uploads/', './uploads/out')
    cv2.imwrite(filepath, image)
