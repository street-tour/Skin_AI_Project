from flask import Blueprint, request, jsonify, session
from ..db_utils import chatbot_util
from openai import OpenAI

# Flask Blueprint 설정
chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# OpenAI API 클라이언트 초기화 (환경변수에서 API 키 사용)
client = OpenAI()

# ---------------------------------------
# ✅ 현재 사용하는 요청 처리: 사용자 맞춤형 정보 반영 (info2)
# ---------------------------------------
@chatbot_bp.route("/chat-text/", methods=['POST'])
def handle_chat_text_with_custom_info2():
    """
    사용자 맞춤 정보를 반영한 프롬프트 기반 챗봇
    """
    loginuser = session.get('loginuser')
    if not loginuser or 'memberid' not in loginuser:
        return jsonify({'message':'로그인이 필요합니다.'})
    
    memberid = session['loginuser'].get('memberid')
    memberinfo = chatbot_util.memberinfo(memberid=memberid)
    model_list = ['eyewrinkles', 'lips', 'chin', 'forehead_1', 'forehead_2', 'cheeks', 'glabella']

    bad_conditions = chatbot_util.get_bad_skin_conditions(memberid)

    if bad_conditions is None:
        bad_conditions_text = "검사 결과가 없습니다."
    elif not bad_conditions:
        bad_conditions_text = "피부 상태가 양호합니다."
    else:
        bad_conditions_text = ", ".join(bad_conditions)

    selected_ingredients = chatbot_util.get_ingredients_for_conditions(bad_conditions)

    recommended_products = chatbot_util.recommended_best_products(selected_ingredients)

    if recommended_products:
        recommended_text = "\n".join([f"- {p['product_name']}" for p in recommended_products])
    else:
        recommended_text = "추천할 제품이 없습니다."

    json_data = request.get_json()
    message = json_data.get('message')
    
    recent_result = {}
    for mo in model_list:
        v = chatbot_util.select_result_by_memberid_and_model(memberid, mo)
        recent_result.update({mo:v})
    json_data = request.get_json()
    message = json_data.get('message')
    # print(memberinfo[0][0])
    # print(recent_result)
    prompt = f"""
        아래 **고려사항**과 **피부고민**을 반영하여 **지시사항**에 따라 질문에 대한 답변을 생성하세요.

        [지시사항]
        화장품 추천에 대한 질문인 경우 **추천제품** 내용을 기반으로 답변을 생성하세요
        화장품 추천이 아닌 경우 다른 정보와 당신의 기존 학습 내용을 기반으로 답변을 생성하세요
        
        [고려사항]
        1. 사용자의 성별은 {memberinfo[0][0]}  입니다.
        2. 사용자의 피부타입은 {memberinfo[0][1]} 입니다.
        3. 사용자의 나이는 {memberinfo[0][2]} 입니다.
        4. 사용자의 피부 상태는 {recent_result} 입니다.

        [피부고민]
        - 최근 피부 진단 결과에서 미흡한 부분: {bad_conditions_text}

        [해결성분]
        - {', '.join(selected_ingredients)}

        [추천제품]
        {recommended_text}

        질문: {message}
        답변: 
    """

    # 대화 이력 불러오기 (없으면 초기화)
    chat_history = session.get('chat-history', [])
    if not chat_history:
        chat_history.append({"role": "system", "content": "당신은 모든 정보를 잘 알고 있는 친절한 안내자입니다. 질문에 대해 가능한 간결하게 답변해야 합니다."})

    # 사용자 메시지 추가
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)
    # chat_history.append({"role": "user", "content": prompt})

    # OpenAI API 요청
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history,
        n=1,
        temperature=1
    )

    # chat_history = chat_history[:-1]
    # chat_history.append({"role": "user", "content": message})
    user_message['content'] = message

    # 챗봇 응답 추가
    chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})
    session['chat-history'] = chat_history  # 세션에 저장

    return jsonify({'message': completion.choices[0].message.content})

# ---------------------------------------
# ✅ 대화 이력 복원 기능 (세션 유지)
# ---------------------------------------
@chatbot_bp.route("/reload-chat-history/")
def reload_chat_history():
    """
    대화 이력을 불러오는 엔드포인트
    """
    chat_history = session.get("chat-history", [])
    if not chat_history:
        chat_history.append({"role": "system", "content": "당신은 모든 정보를 잘 알고 있는 친절한 안내자입니다. 질문에 대해 가능한 간결하게 답변해야 합니다."})

    session['chat-history'] = chat_history  # 세션 저장

    return jsonify(chat_history[1:] if len(chat_history) > 1 else [])
