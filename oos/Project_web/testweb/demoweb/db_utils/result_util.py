import pymysql

import pymysql

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

def select_result_list_with_tryno(result_type='list', tryno=None):
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

        # 트라이넘버가 없을 경우 None 반환
        if tryno is None:
            return None
        
        # 트라이넘버가 리스트라면 IN 절로 변환
        if isinstance(tryno, (list, tuple)):
            placeholders = ', '.join(['%s'] * len(tryno))
            sql = f"""
                SELECT t.testno, t.model, t.result, t.tryno
                FROM skin_test t
                INNER JOIN (
                    SELECT model, MAX(testno) AS max_testno
                    FROM skin_test
                    WHERE tryno IN ({placeholders})
                    GROUP BY model
                ) subquery
                ON t.model = subquery.model AND t.testno = subquery.max_testno
                ORDER BY t.testno DESC
            """
            cursor.execute(sql, tuple(tryno))  # 리스트를 튜플로 변환하여 실행
        else:
            sql = """
                SELECT t.testno, t.model, t.result, t.tryno
                FROM skin_test t
                INNER JOIN (
                    SELECT model, MAX(testno) AS max_testno
                    FROM skin_test
                    WHERE tryno = %s
                    GROUP BY model
                ) subquery
                ON t.model = subquery.model AND t.testno = subquery.max_testno
                ORDER BY t.testno DESC
            """
            cursor.execute(sql, (tryno,))

        rows = cursor.fetchall()

        if not rows:
            return None

        return rows if result_type == 'list' else {row[1]: row[2] for row in rows}

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

def select_skin_test_count():
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select count(*) from test_table"""
    cursor.execute(sql)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0]

def select_skin_test_with_paging(memberid, start, page_size, result_type="list"):
    memberid = memberid
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select tryno, memberid, testdate
             from test_table
             where memberid = %s
             order by tryno desc
             limit %s,%s"""
    
    cursor.execute(sql, [memberid, start, page_size])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) ==0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["tryno", "memberid", "testdate"])
    
def select_disease_test(memberid, result_type='list'):
    memberid = memberid
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                        user ='humanda', passwd='humanda')
    cursor = conn.cursor()
    sql = """SELECT result, testdate
            FROM disease_test
            WHERE memberid = %s
            ORDER BY testno DESC
            LIMIT 1
        """
    
    cursor.execute(sql, [memberid])

    rows = cursor.fetchone()

    cursor.close()
    conn.close()
    if len(rows) ==0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["result", "testdate"])
    
import pymysql

def select_skin_test(tryno_list, result_type='list'):
    """트라이넘버 리스트에 해당하는 데이터를 조회"""
    conn = None
    try:
        conn = pymysql.connect(
            host="192.168.0.31",
            port=3306,
            db="skin",
            user="humanda",
            passwd="humanda"
        )

        # 리스트가 아니면 리스트로 변환
        if not isinstance(tryno_list, (list, tuple)):
            tryno_list = [tryno_list]

        # 빈 리스트면 즉시 반환
        if not tryno_list:
            return None

        # IN 절을 동적으로 생성
        placeholders = ', '.join(['%s'] * len(tryno_list))
        sql = f"""
            SELECT testno, model, result, tryno
            FROM skin_test
            WHERE tryno IN ({placeholders})
            ORDER BY testno DESC
        """

        with conn.cursor() as cursor:  # 자동으로 커서 닫힘
            cursor.execute(sql, tuple(tryno_list))  # 리스트를 튜플로 변환하여 전달
            rows = cursor.fetchall()

        if not rows:
            return None

        return rows if result_type == 'list' else [
            {"testno": row[0], "model": row[1], "result": row[2], "tryno": row[3]}
            for row in rows
        ]

    except pymysql.MySQLError as e:
        print(f"DB 오류 발생: {e}")
        return None

    finally:
        if conn:
            conn.close()

