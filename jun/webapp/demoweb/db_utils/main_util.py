import pymysql

import pymysql

import pymysql

def member_count():
    """멤버 수 조회 함수 (Activate가 1인 경우)"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM member WHERE active = 1")
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def test_count():
    """멤버 수 조회 함수 (Activate가 1인 경우)"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_table")
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def weekly_member_count():
    """최근 7일 이내 가입한 활성 멤버 수 조회 함수"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM member
            WHERE active = 1
            AND regdate >= DATE_SUB(NOW(), INTERVAL 7 DAY);
        """)
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def weekly_test_count():
    """최근 7일 수행된 테스트 수 조회"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM test_table
            WHERE testdate >= DATE_SUB(NOW(), INTERVAL 7 DAY); 
        """)
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def product_count():
    """제품 수 조회"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(product_no) FROM product")
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def ingredient_count():
    """성분 수 조회"""
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ingredient")
        return [cursor.fetchone()[0]]
    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def product_table_list(result_type = "list"):
    """최근 5개 제품 조회"""
    conn = pymysql.connect(host="192.168.0.31", port=3306, db="skin", user="humanda", passwd="humanda")

    cursor = conn.cursor()
    
    sql = """select product_no, category, product_name, created_at
             from product
             order by created_at desc
             limit 5"""
    
    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if not rows:
        return None
    
    elif result_type =='list':
        return rows
    
    else:
        return result_as_dict(rows, ["product_no", "category", "product_name", "created_at"])
    

def result_as_dict(rows, columns):
    dict_list = []
    for row in rows:
        d = {c:v for c,v in zip(columns, row)}
        dict_list.append(d)
    return dict_list

                  