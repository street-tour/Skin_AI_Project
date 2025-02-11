import pymysql

def insert_member(memberid, passwd, email, age, gender, skintype, address):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """insert into member (memberid, passwd, email, age, gender, skintype, address)
             values(%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(sql, [memberid, passwd, email, age, gender, skintype, address])

    conn.commit()

    cursor.close()
    conn.close()
    
def select_member_by_id(memberid):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select memberid, passwd, email, age, gender, skintype, address
            from member
            where memberid = %s"""

    cursor.execute(sql, [memberid])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row