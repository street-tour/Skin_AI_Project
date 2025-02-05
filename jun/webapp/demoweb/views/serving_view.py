from flask import Blueprint, render_template
from flask import request, jsonify

serving_bp = Blueprint("serving", __name__, url_prefix = "/serving")

@serving_bp.route("/index/")
def index():
    return render_template("serving/index.html")

@serving_bp.route("/predict/", methods=["POST"])
def predict():

    from PIL import Image
    from tensorflow import keras as tf_keras
    import numpy as np
    from pathlib import Path
    import os

    files = request.files
    if 'img_input' not in files:
        return jsonify({
            "result" : "fail",
            "message" : "No file part"
        })
    
    file = files['img_input']
    if len(file.filename) == 0:
        return jsonify({
            "result": "fail",
            "message" : "File not selected"
        })

    image_input = Image.open(file)
    image_input = image_input.resize((256,256))
    image_array = tf_keras.utils.img_to_array(image_input)
    image_array = image_array/255
    image_array = np.expand_dims(image_array, 0)

    try:
        rpath = serving_bp.root_path
        root_path = Path(rpath).parent
        sub_path = 'serving_model/model76-1.h5'
        mnist_model = tf_keras.models.load_model(os.path.join(root_path, sub_path))
    except Exception as e:
        print(e)
        raise e

    predictions = mnist_model.predict(image_array)
    # predicted_class = np.argmax(predictions, axis=1)
    print("---------------------------", predictions)
    predicted_class = (predictions >= 0.5).astype(int)[0][0]
    confidence = np.max(predictions)

    return jsonify({
        "result": "success",
        "message": "",
        "predicted_class" : str(predicted_class),
        "confidence" : str(confidence)
    })





@serving_bp.route("/disease/")
def disease():
    return render_template("serving/disease.html")

@serving_bp.route("/predict2/", methods=["POST"])
def predict2():

    from PIL import Image
    from tensorflow import keras as tf_keras
    import numpy as np
    from pathlib import Path
    import os

    files = request.files
    if 'img_input' not in files:
        return jsonify({
            "result" : "fail",
            "message" : "No file part"
        })
    
    file = files['img_input']
    if len(file.filename) == 0:
        return jsonify({
            "result": "fail",
            "message" : "File not selected"
        })

    image_input = Image.open(file)
    image_input = image_input.resize((256,256))
    image_array = tf_keras.utils.img_to_array(image_input)
    image_array = image_array/255
    image_array = np.expand_dims(image_array, 0)

    try:
        rpath = serving_bp.root_path
        root_path = Path(rpath).parent
        sub_path = 'serving_model/test.model.h5'
        mnist_model = tf_keras.models.load_model(os.path.join(root_path, sub_path))
    except Exception as e:
        print(e)
        raise e

    predictions = mnist_model.predict(image_array)
    predicted_class = np.argmax(predictions, axis=1)
    #predicted_class = (predictions >= 0.5).astype(int)[0][0]
    confidence = np.max(predictions)

    return jsonify({
        "result": "success",
        "message": "",
        "predicted_class" : str(predicted_class),
        "confidence" : str(confidence)
    })