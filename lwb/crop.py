import os
import json
import cv2
import numpy as np

# 데이터가 저장된 최상위 경로
base_dir = r"D:\final_project_backup\FINAL_DATA\한국인 피부상태 측정 데이터\Training"
image_base_dir_camera = os.path.join(base_dir, "images", "camera")
label_base_dir_camera = os.path.join(base_dir, "labels", "camera")
image_base_dir_pad = os.path.join(base_dir, "images", "pad")
label_base_dir_pad = os.path.join(base_dir, "labels", "pad")
image_base_dir_phone = os.path.join(base_dir, "images", "phone")
label_base_dir_phone = os.path.join(base_dir, "labels", "phone")

# 리사이즈 크기 설정
target_size = (128, 128)

def process_files(label_key, annotion_key):
    """
    :param label_key : JSON파일에서 처리할 키
    :param annotation_key : 타겟 데이터에서 사용할 키
    """
    # 딕셔너리에 결과 저장
    image_data = {}  # {파일명: 이미지 배열}
    target_data = {}  # {파일명: 타겟 값}

    def find_image_path(base_dirs, id_folder, image_filename):
        for base_dir in base_dirs:
            image_path = os.path.join(base_dir, id_folder, image_filename)
            if os.path.exists(image_path):
                return image_path  # 이미지 경로를 찾으면 반환
        return None  # 모든 경로에서 이미지 파일을 찾지 못하면 None 반환

    label_dirs = [label_base_dir_camera, label_base_dir_pad, label_base_dir_phone]
    base_dirs = [image_base_dir_camera, image_base_dir_pad, image_base_dir_phone]

    for label_dir in label_dirs:
        for root, _, files in os.walk(label_dir):
            for file in files:
                if file.endswith(label_key):
                    label_path = os.path.join(root, file)
                    
                    try:
                        # JSON 파일 로드
                        with open(label_path, 'r', encoding='utf-8') as f:
                            label_data = json.load(f)
                        
                        # JSON 데이터에서 이미지 파일명 및 id_folder 추출
                        image_filename = label_data['info']['filename']
                        id_folder = label_data['info']['id']
                        
                        # 이미지 경로 찾기
                        image_path = find_image_path(base_dirs, id_folder, image_filename)
                        if image_path is None:
                            print(f"Image file not found for {label_path}: {image_filename}")
                            continue
                        
                        # 이미지 파일 읽기
                        with open(image_path, 'rb') as img_file:
                            file_data = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
                            image = cv2.imdecode(file_data, cv2.IMREAD_COLOR)
                        
                        if image is None:
                            print(f"Failed to decode image: {image_path}")
                            continue
                        
                        # bbox 유효성 검사
                        bbox = label_data['images']['bbox']
                        x_min, y_min, x_max, y_max = map(int, bbox)
                        if x_min >= x_max or y_min >= y_max:
                            print(f"Invalid bbox in file {label_path}: {bbox}")
                            continue
                        
                        # 이미지 크롭 및 리사이즈
                        cropped_image = image[y_min:y_max, x_min:x_max]
                        resized_image = cv2.resize(cropped_image, target_size)
                        
                        # 데이터 저장
                        key = os.path.splitext(file)[0]  # 파일명에서 확장자 제거
                        image_data[key] = resized_image
                        target_data[key] = label_data['annotations'][annotion_key]
                    
                    except Exception as e:
                        print(f"Error processing file {label_path}: {e}")

    return image_data, target_data