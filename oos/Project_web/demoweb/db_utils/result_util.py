import pymysql

def select_result_list(result_type = 'list', memberid = None):
    memberid = memberid
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = 'skin',
                           user = "humanda", passwd = 'humanda')
    
    cursor = conn.cursor()

    sql = """select testno, model, result, modeldate, memberid
             from skin_test
             where memberid = %s
             order by testno desc"""
    
    cursor.execute(sql, (memberid,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) == 0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["testno", "model", "result", "modeldate", "memberid"])
                                     

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

    sql = """select count(*) from skin_test"""
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

    sql = """select testno, model, result, modeldate, memberid
             from skin_test
             where memberid = %s
             order by testno desc
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
        return result_as_dict(rows, ["testno", "model", "result", "modeldate", "memberid"])