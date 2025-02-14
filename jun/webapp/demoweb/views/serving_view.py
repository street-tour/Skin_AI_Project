from flask import Blueprint, render_template
from flask import request, jsonify

from PIL import Image
from tensorflow import keras as tf_keras
import torch
import numpy as np
from pathlib import Path
import os
import torch.nn as nn
import torch.nn.functional as F
import warnings
import oos_model_binary
import sys

serving_bp = Blueprint("serving", __name__, url_prefix = "/serving")

@serving_bp.route("/index/")
def index():
    return render_template("serving/index.html")

@serving_bp.route("/predict/", methods=["POST"])
def predict():



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
    


    parts = request.form.getlist('part')

    if not parts:
        return jsonify({
            "result": "fail",
            "message": "No areas selected"
        })


    model_paths = {

        "이마-주름": "serving_model/model70.h5",
        "이마-색소침착":"serving_model/ForeheadPigmentation_BinaryClassification_Cam_3F_4190.pth",
        "볼" : "serving_model/볼모공_분류모델.h5",
        "미간": "serving_model/미간주름_분류모델.h5",
        "턱" : "serving_model/턱쳐짐_분류모델.h5",
        "입술" : "serving_model/입술건조_분류모델.h5",
        "눈가주름" : "serving_model/눈가주름_분류모델.h5",
        "여드름" : "serving_model/여드름_분류모델.h5"

    }

    predictions = {}

    expanded_parts = []
    for part in parts:
        expanded_parts.extend(part.split(","))  # 쉼표로 구분된 값을 분리

    print('--------------------> 1.', expanded_parts)
    # pythorch_model = SkinNet()
    # weight_path = 'serving_model/FP_5084.pth'
    # pythorch_model = torch.load(os.path.join(root_path, weight_path), map_location=torch.device('cpu'))

    for area in expanded_parts:
        if area in model_paths:
            try:
                model_path = model_paths[area]
                rpath = serving_bp.root_path
                root_path = Path(rpath).parent
                if area == "이마-색소침착":

                    # 모듈 경로를 추가 (예: 모듈이 "D:/Work/modules/oos_model_binary"에 있을 경우)
                    module_path = r"D:\project\jun\final\jun\webapp\demoweb\serving_model"
                    if module_path not in sys.path:
                        sys.path.append(module_path)

                    # 모듈 불러오기
                    import oos_model_binary

                    image = Image.open(file).convert("RGB")
                    image_array = np.array(image)
                    image = image_array / 255  # 0~1로 정규화 (이미지가 numpy 배열인 경우

                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=FutureWarning)
                        # 모델 로드 (구조와 가중치 동시 로드)
                        model_path = os.path.join(root_path, "serving_model/FP_3687(softmax_normalization).pth")
                        model = torch.load(model_path, map_location="cpu",weights_only=False)
                        model.to("cpu")
                        model.eval()

                    # 모델 예측
                    result, confidence = oos_model_binary.predict(image=image, model=model)

                    # 결과 및 신뢰도 출력
                    if result == 0:
                        result_text = "색소침착 없음"
                    else:
                        result_text = "색소침착 심함"


                    predictions[area] = {
                        "model_name":str(area),
                        "predicted_class": str(result_text),
                        "confidence": str(confidence)
                    }

                else:

                    image_input = Image.open(file)
                    image_input = image_input.resize((128,128))
                    image_array = tf_keras.utils.img_to_array(image_input)
                    image_array = image_array/255
                    image_array = np.expand_dims(image_array, 0)

                    model = tf_keras.models.load_model(os.path.join(root_path, model_path))

                    area_prediction = model.predict(image_array)
                    # predicted_class = (area_prediction >= 0.5).astype(int)[0][0]
                    # confidence = np.max(area_prediction)
                    
                    # softmax처럼 확률을 계산 (두 클래스에 대한 확률로 변환)
                    prob_class_1 = area_prediction[0][0]   # 클래스 1의 확률 (sigmoid)
                    prob_class_0 = 1 - prob_class_1       # 클래스 0의 확률 (1 - sigmoid)

                    # 예측 클래스 결정 (더 높은 확률을 가진 클래스로 예측)
                    predicted_class = np.argmax([prob_class_0, prob_class_1])  # 0 또는 1
                
                    if area == "이마-주름":
                        if predicted_class ==0:
                            result_text = "주름이 없습니다."
                        else:
                            result_text = "주름이 많습니다."
                    elif area =='볼':
                        if predicted_class ==0:
                            result_text = "0"
                        else:
                            result_text = "1"
                    elif area =='미간':
                        if predicted_class ==0:
                            result_text = "2"
                        else:
                            result_text = "3"
                    elif area =='턱':
                        if predicted_class ==0:
                            result_text = "4"
                        else:
                            result_text = "5"
                    elif area =='입술':
                        if predicted_class ==0:
                            result_text = "6"
                        else:
                            result_text = "7"
                    elif area =='눈가주름':
                        if predicted_class ==0:
                            result_text = "8"
                        else:
                            result_text = "9"
                    else:
                        if predicted_class ==0:
                            result_text = "10"
                        else:
                            result_text = "11"

                    
                    # confidence는 예측된 클래스의 확률
                    confidence = max(prob_class_0, prob_class_1)
                    confidence = confidence * 100
                    predictions[area] = {
                        "model_name":str(area),
                        "predicted_class": str(result_text),
                        "confidence": str(confidence)
                    }


            except Exception as e:
                print("--------------------------> e", e)
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