import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='MEET',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
