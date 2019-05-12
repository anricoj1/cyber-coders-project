import pymysql

class db_connector:
    def __init__(self):
        self.__connection = pymysql.connect(host='35.226.170.182',
                             user='root',
                             password='P@$$word12',
                             db='MEET',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        self.__c = self.__connection.cursor()

    def fetchall(self, query):

        self.__c.execute(query)

        result = self.__c.fetchall()

        self.__c.close()
        return result

    def db_mod(self, query):
        self.__c.execute(query)

        self.__c.commit()

        self.__c.close()

    def fetchone(self, query, one):
        self.__c.execute(query)

        self.__c.execute(query)

        result = self.__c.fetchone()

        self.__c.close()
        return result

    def __del__(self):
        return 'Done!!'

