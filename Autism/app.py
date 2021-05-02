from flask import Flask, render_template, request
import tensorflow as tf
from werkzeug.utils import secure_filename
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import os
app = Flask(__name__)


def predict(image):
    model = load_model("autism_fin.h5")
    img = tf.keras.preprocessing.image.load_img(image, target_size = (180, 180))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    score = predictions[0]
    print("This image is %.2f percent autistic and %.2f percent non-autistic." % (100 * (1 - score), 100 * score) )
    result = "This image is %.2f percent autistic and %.2f percent non-autistic." % (100 * (1 - score), 100 * score)
    return result

@app.route("/")
def home():
    return render_template("upload.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      result = predict(f.filename)
      filepath = os.path.normpath(f.filename)
      print(filepath)
      return render_template("result.html",result = result, filepath = filepath )

if __name__ == "__main__":
    app.run(debug=True)
