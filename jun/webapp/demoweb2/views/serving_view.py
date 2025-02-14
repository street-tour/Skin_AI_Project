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
from serving_model2 import oos_model_binary

print("======================>", oos_model_binary)

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

        "forehead-wrinkle": "serving_model/model70.h5",
        "forehead-hyperpigmentation":"serving_model/ForeheadPigmentation_BinaryClassification_Cam_3F_4190.pth",
        "cheeks" : "serving_model/볼모공_분류모델.h5",
        "glabella": "serving_model/미간주름_분류모델.h5",
        "chin" : "serving_model/턱쳐짐_분류모델.h5",
        "lips" : "serving_model/입술건조_분류모델.h5",
        "eye wrinkles" : "serving_model/눈가주름_분류모델.h5",
        "acne" : "serving_model/여드름_분류모델.h5"

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
        print('--------------------> 2.', area)
        if area in model_paths:
            try:
                model_path = model_paths[area]
                rpath = serving_bp.root_path
                root_path = Path(rpath).parent
                if area == "forehead-hyperpigmentation":

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
                    print("========================> 3.")

                    # 모델 예측
                    result, confidence = oos_model_binary.predict(image=image, model=model)

                    # 결과 및 신뢰도 출력
                    if result == 0:
                        result_text = "색소침착 없음"
                    else:
                        result_text = "색소침착 심함"

                    print("=" * 30)
                    print(f"분석 결과: {result_text}")
                    print(f"신뢰도: {confidence :.2f}%")
                    print("=" * 30)

                else:

                    image_input = Image.open(file)
                    image_input = image_input.resize((128,128))
                    image_array = tf_keras.utils.img_to_array(image_input)
                    image_array = image_array/255
                    image_array = np.expand_dims(image_array, 0)

                    model = tf_keras.models.load_model(os.path.join(root_path, model_path))

                    print(model)

                    area_prediction = model.predict(image_array)
                    predicted_class = (area_prediction >= 0.5).astype(int)[0][0]
                    confidence = np.max(area_prediction)

                    predictions[area] = {
                        "predicted_class": str(predicted_class),
                        "confidence": str(confidence)
                    }

                # if area == "forehead-hyperpigmentation":
                #     # 모델 예측 수행
                #     pythorch_model = torch.load(os.path.join(root_path, weight_path), map_location=torch.device('cpu'), weights_only=False)
                #     pythorch_model.eval()  # 평가 모드
                #     with torch.no_grad():
                #         logits = model(image_input)  # 모델의 출력 (로짓 값)

                #     # 1) 확률 계산 (Softmax)
                #     probabilities = F.softmax(logits, dim=1)

                #     # 2) 예측 클래스
                #     predicted_class = torch.argmax(probabilities, dim=1).item()  # 가장 높은 확률의 클래스

                #     # 출력
                #     print("클래스별 확률:", probabilities)
                #     print("예측된 클래스:", predicted_class)
                # else:
                #     predictions[area] = {
                #         "predicted_class": str(predicted_class),
                #         "confidence": str(confidence)
                #     }

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