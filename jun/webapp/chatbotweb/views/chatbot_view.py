from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# os.environ['OPENAI_API_KEY'] =''
client =OpenAI() # 환경변수에 저장된 api_key를 사용


# @chatbot_bp.route("/chat-text/", methods=['POST'])
# def handle_chat_text():
#     # 요청 데이터 읽기 1 : form데이터 형식 
#     # message = request.form.get('message')

#     # 요청 데이터 읽기 2 : JSON 데이터 형식
#     json_data = request.get_json()
#     message = json_data.get('message')

#     print(message)

#     # 데이터 응답 1 : plain text
#     # return 'echo message :' + message 
    
#     # 데이터 응답 2 : json
#     return jsonify({'response_message' : f'echo message :  + {message}' })
    
# 요청 처리 1 : 폼데이터 + plain text 반환
# @chatbot_bp.route("/chat-text/", methods=['POST'])
# def handle_chat_text():
#     message = request.form.get('message')
#     print(message)

#     return 'echo message :' + message 

# 요청 처리 2 : JSON 읽기 + JSON반환
# @chatbot_bp.route("/chat-text/", methods=['POST'])
# def handle_chat_text():
#     json_data = request.get_json()
#     message = json_data.get('message')

#     print(message)
#     return jsonify({'message' : f'echo message :  + {message}' })

# 요청 처리 3 : open api service 사용 (simple)
@chatbot_bp.route("/chat-text/", methods=['POST'])
def handle_chat_text():
    json_data = request.get_json()
    message = json_data.get('message')

    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": 'system', 'content': "당신은 모든 정보를 잘 알고 있는 친절한 안내자입니다. 질문에 대해 가능한 간결하게 답변해야 합니다."},
            {"role":"user", "content": message}
        ],
        n=1,
        temperature=1
    )

    return jsonify({'message' : completion.choices[0].message.content })