import pymysql

def insert_test_table(memberid):
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """insert into test_table (memberid)
             values(%s)"""
    
    cursor.execute(sql, [memberid])

    conn.commit()

    cursor.close()
    conn.close()


    
def select_tryno(memberid):
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select tryno from test_table
             where memberid = %s
             order by tryno desc
             limit 1"""
    
    cursor.execute(sql, [memberid])

    conn.commit()

    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row



def insert_skin_test(model, result, confidence, tryno):
    conn = pymysql.connect(host = "192.168.0.31", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """insert into skin_test (model, result, confidence, tryno)
             values(%s,%s,%s,%s)"""
    
    cursor.execute(sql, [model, result, confidence, tryno])

    conn.commit()

    cursor.close()
    conn.close()

# def insert_disease_test(memberid, result, confidence):
#     conn = pymysql.connect(host="192.168.0.31", port=3306, db ='skin',
#                            user='humanda', passwd='humanda')
#     cursor = conn.cursor()

#     sql = """insert into disease_test(memberid, result, confidence)
#              values(%s, %s,%s)"""
    
#     cursor.execute(sql, [memberid, result, confidence])

#     conn.commit()

#     cursor.close()
#     conn.close()