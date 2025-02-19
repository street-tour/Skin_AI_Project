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
            AND regdate >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
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
        cursor.execute("SELECT COUNT(*) FROM product")
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
