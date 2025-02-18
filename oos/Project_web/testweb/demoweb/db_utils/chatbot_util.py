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