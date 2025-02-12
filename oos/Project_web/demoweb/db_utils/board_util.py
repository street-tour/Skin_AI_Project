import pymysql

def insert_board(title, writer, content):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """insert into board(title, writer, content)
             values(%s,%s,%s)"""

    cursor.execute(sql, [title, writer, content])

    conn.commit()

    sql = 'select last_insert_id()'
    cursor.execute(sql)
    last_insert_id_row = cursor.fetchone()

    cursor.close()
    conn.close()

    return last_insert_id_row[0]

def select_board_list(result_type = 'list'):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = 'skin',
                           user = "humanda", passwd = 'humanda')
    
    cursor = conn.cursor()

    sql = """select boardno, title, writer, writedate, modifydate, deleted
             from board
             order by boardno desc"""
    
    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) == 0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["boardno", "title", "writer", "writedate", "modifydate", "deleted"])
                                     

def result_as_dict(rows, columns):
    dict_list = []
    for row in rows:
        d = {c:v for c,v in zip(columns, row)}
        dict_list.append(d)
    return dict_list

    
def select_member_by_id(member_id):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select memberid, passwd, email
            from member
            where memberid = %s"""

    cursor.execute(sql, [member_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def select_board_by_boardno(boardno, result_type='list'):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = 'skin',
                           user = "humanda", passwd = 'humanda')
    
    cursor = conn.cursor()

    sql = """select boardno, title, writer, content, writedate, modifydate, deleted
             from board
             where boardno = %s and deleted = FALSE"""
    
    cursor.execute(sql, [boardno])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) ==0:
        return None
    elif result_type =='list':
        return rows[0]
    else:
        cols = "boardno,title,writer,content,writedate,modifydate,deleted".split(",")
        results = result_as_dict(rows, cols)
        return results[0]
    
def delete_board(boardno):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    
    cursor = conn.cursor()

    # sql = """delete board where boardno =%s"""
    sql = """update board set deleted = TRUE where boardno =%s"""

    cursor.execute(sql, boardno)

    conn.commit()

    cursor.close()
    conn.close()

def update_board(boardno, title, content):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    
    cursor = conn.cursor()

    # sql = """delete board where boardno =%s"""
    sql = """update board set title = %s, content = %s where boardno = %s"""
    cursor.execute(sql, [title, content, boardno])

    conn.commit()

    cursor.close()
    conn.close()

def select_board_list_with_paging(start, page_size, result_type="list"):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select boardno, title, writer, writedate, modifydate, deleted
             from board
             order by boardno desc
             limit %s,%s"""
    
    cursor.execute(sql, [start, page_size])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(rows) ==0:
        return None
    elif result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ['boardno', 'title', 'writer','writedate','modifydate','deleted'])
    
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

def insert_attachment(boardno, userfilename, savedfilename):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """insert into attachment (boardno, userfilename, savedfilename)
             values(%s,%s,%s)"""

    cursor.execute(sql, [boardno, userfilename, savedfilename])

    conn.commit()


    cursor.close()
    conn.close()

def select_attachments_by_boardno(boardno, result_type='dict'):
    conn = pymysql.connect(host = "192.168.0.51", port = 3306, db = "skin",
                           user ='humanda', passwd='humanda')
    cursor = conn.cursor()

    sql = """select attachno, boardno, userfilename, savedfilename, downloadcnt
             from attachment
             where boardno = %s"""
    cursor.execute(sql,[boardno])

    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if result_type =='list':
        return rows
    else:
        return result_as_dict(rows, ["attachno", "boardno", "userfilename", "savedfilename", "downloadcnt"])


def increase_download_count(savedfilename):
    conn = pymysql.conncet(host="192.168.0.51", port=3306, db='skin',
                           user="humanda", passwd="humanda")
    
    cursor = conn.cursor()

    sql = """update attachment
             set downloadcnt = downloadcnt + 1
             where savedfilename = %s"""
    cursor.execute(sql, [savedfilename])

    conn.commit()

    cursor.close()
    conn.close()

def delete_attachment(attachno):
    conn = pymysql.conncet(host="192.168.0.51", port=3306, db="skin",
                           user='humanda', passwd="humanda")
    
    cursor = conn.cursor()

    sql = """delete from attachment
             where attachno = %s"""
    cursor.execute(sql, [attachno])

    conn.commit()

    cursor.close()
    conn.close()