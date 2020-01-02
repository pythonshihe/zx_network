import pymysql


# 1.连接到mysql数据库
def get_keyword():
    # 本地链接
    conn = pymysql.connect(host='********', port=3306, user='root', password='*******',
                           db='******', charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    sql = 'select city from city_keyword ORDER BY id LIMIT 0,100'
    cursor.execute(sql)
    all_key = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_key


if __name__ == '__main__':
    all_key = get_keyword()
    for key_word in all_key:
        if len(key_word[0]) == 2:
            print(key_word[0])
