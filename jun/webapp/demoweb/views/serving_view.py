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
    image_input = image_input.resize((128,128))
    image_array = tf_keras.utils.img_to_array(image_input)
    image_array = image_array/255
    image_array = np.expand_dims(image_array, 0)


    parts = request.form.getlist('part')

    if not parts:
        return jsonify({
            "result": "fail",
            "message": "No areas selected"
        })


    model_paths = {
        # "forehead": "serving_model/model76-1.h5",
        "cheeks" : "serving_model/볼모공_분류모델.h5",
        "glabella": "serving_model/미간주름_분류모델.h5",
        "chin" : "serving_model/턱쳐짐_분류모델.h5",
        "lips" : "serving_model/입술건조_분류모델.h5",
        "eye wrinkles" : "serving_model/눈가주름_분류모델.h5",
        "acne" : "serving_model/여드름_분류모델.h5"

    }

    predictions = {}


    for area in parts:
        if area in model_paths:
            try:
                model_path = model_paths[area]
                rpath = serving_bp.root_path
                root_path = Path(rpath).parent
                model = tf_keras.models.load_model(os.path.join(root_path, model_path))
                print(model)

                area_prediction = model.predict(image_array)
                predicted_class = (area_prediction >= 0.5).astype(int)[0][0]
                confidence = np.max(area_prediction)

                predictions[area] = {
                    "predicted_class": str(predicted_class),
                    "confidence": str(confidence)
                }

            except Exception as e:
                predictions[area] = {
                    "error": str(e)
                }



    return jsonify({
        "result": "success",
        "predictions": predictions
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