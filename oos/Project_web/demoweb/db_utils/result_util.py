import pymysql

def select_result_list_with_tryno(result_type='list', tryno=None):
    tryno = tryno
    conn = pymysql.connect(host="192.168.0.51", port=3306, db='skin',
                           user="humanda", passwd='humanda')
    
    cursor = conn.cursor()

    # SQL 수정: 모델별로 가장 큰 testno를 가진 행 가져오기
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
    
    cursor.execute(sql, [tryno])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(rows) == 0:
        return None
    elif result_type == 'list':
        return rows
    else:  # result_type == 'dict'
        # model을 키로, result를 값으로 하는 딕셔너리 생성
        return {row[1]: row[2] for row in rows}  # row[1] = model, row[2] = result


                                     

def result_as_dict(rows, columns):
    dict_list = []
    for row in rows:
        d = {c:v for c,v in zip(columns, row)}
        dict_list.append(d)
    return dict_list

def select_skin_test_count():
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
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
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
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
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
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