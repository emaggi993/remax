from core import config
from mysql.connector import connect

class Conexion:
    def __init__(self):
        self.__db = connect(
            host = config.HOST,
            port = config.PUERTO,
            user = config.USER,
            password = config.PASS,
            database = config.BASE_DATOS
        )
        self.__cursor = self.__db.cursor()
        self.__cursos_dic = self.__db.cursor(dictionary=True)

    def get_db(self):
        return self.__db

    def get_cursor(self):
        return self.__cursor
    
    def get_cursor_dic(self):
        return self.__cursos_dic

    def close(self):
        self.__db.close()
        self.__cursor.close()
        self.__cursos_dic.close()

    def commit(self):
        self.__db.commit()
    
    def rollback(self):
        self.__db.rollback()

    def get_columnas(self, tabla):
        query = "SHOW COLUMNS FROM {}".format(tabla)
        self.__cursor.execute(query)

        return self.__cursor.fetchall()
    def get_columnas_nombres(self, tabla):
        query = "SHOW COLUMNS FROM {}".format(tabla)
        self.__cursor.execute(query)
        columnas = self.__cursor.fetchall()
        nombres = []
        for columna in columnas:
            nombres.append(columna[0])
        return nombres
    
    def crear_campo(self, propiedad):
        query= "ALTER TABLE inmuebles ADD {} TEXT NULL AFTER observacion_inmueble".format(propiedad)
        self.__cursor.execute(query)
        self.__db.commit()

    def insertar(self, sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return self.__cursor.lastrowid