import pymysql

def memberinfo(memberid, result_type = 'list'):
    memberid = memberid
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select gender, skintype, age
             from member
             where memberid = %s
            """
    
    cursor.execute(sql, [memberid])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) ==0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["gender", "skintype", "age"])
    



def select_result_by_memberid_and_model(memberid, model):
    """트라이넘버(tryno)에 해당하는 가장 최근 testno 결과 조회"""
    conn = None
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()


        sql = """select tryno, model, result from skin_test 
                 where 
                    tryno in (select tryno from test_table where memberid = %s)
                    and 
                    model = %s
                 order by tryno desc
                 limit 1"""
       
        cursor.execute(sql, (memberid, model))

        row = cursor.fetchone()

        if not row:
            return None
        
        return row[-1]

    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def result_as_dict(rows, columns):
    dict_list = []
    for row in rows:
        d = {c:v for c,v in zip(columns, row)}
        dict_list.append(d)
    return dict_list


def get_bad_skin_conditions(memberid):
    """
    test_table에서 memberid와 tryno를 찾고,
    skin_test에서 해당 tryno의 result가 미흡인 것을 가져오는 함수
    """
    conn = pymysql.connect(
        host="192.168.0.31",
        port=3306,
        db="skin",
        user="humanda",
        passwd="humanda"
    )
    cursor = conn.cursor()

    query = """
        SELECT st.model, st.result
        FROM test_table tt
        JOIN skin_test st ON tt.tryno = st.tryno
        WHERE tt.memberid = %s
    """

    cursor.execute(query, [memberid])
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        return None

    bad_conditions = [model for model, result in results if result == "미흡"]

    return bad_conditions

# 추천 성분 매핑
Skin_Concerns = {
    "눈가주름": ["Anti-Aging", "Brightening"],
    "이마색소침착": ["Brightening", "UV Protection"],
    "이마주름" : ["Anti-Aging", "UV Protection"],
    "입술건조": ["Promotes Wound Healing"],
    "턱주름": ["Anti-Aging"],
    "미간주름": ["Anti-Aging", "UV Protection"],
    "볼모공": ["Brightening", "Acne-Fighting"],
    "여드름": ["Acne-Fighting", "Promotes Wound Healing"]
}

def get_ingredients_for_conditions(conditions):
    "bad skin 리스트에 대한 추천 성분 반환"
    selected_ingredients = []
    for condition in conditions:
        if condition in Skin_Concerns:
            selected_ingredients.extend(Skin_Concerns[condition])

    return list(set(selected_ingredients))

def recommended_best_products(ingredients):
    "해당 성분을 많이 포함하는 제품 추천"
    if not ingredients:
        return None
    
    placeholders = ', '.join(['%s'] * len(ingredients))

    query = f"""
    SELECT p.product_no, p.category, p.product_name, p.url, COUNT(i.ingredient) as match_count
    FROM product p
    JOIN ingredient i ON p.product_no = i.product_no
    WHERE i.ingredient IN ({placeholders})
    GROUP BY p.product_no
    ORDER BY match_count DESC
    LIMIT 5; 
    """

    conn = pymysql.connect(host="192.168.0.31", port=3306, db="skin",
                           user='humanda', passwd='humanda')
    cursor = conn.cursor()
    cursor.execute(query, ingredients)
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    if not products:
        return None

    return [
        {"product_no": pid, "category": cat, "product_name": name, "url": url}
        for pid, cat, name, url, _ in products
    ]