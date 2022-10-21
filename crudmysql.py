'''
Tema: Clases y Objetos en Python
Fecha: 29 de septiembre del 2022
Autor: Leonardo Martínez González
'''

'''
Crear una clase de nombre MySQL que tenga las siguientes propiedades:
    MYSQL_HOST
    MYSQL_USER
    MYSQL_PASSWORD
    MYSQL_DATABASE
    MYSQL_CONNECTION
    MYSQL_CURSOR
    
y los siguientes métodos:
    constructor (host="localhost",user="root", pwd="", bd="opensource") que recibe parámetros
    con valores por defecto
    
    conectar_mysql(). se conecta a la Base de datos, 
    
    desconectar_mysql(). Cerrar la conexion a la Base de Datos
    
    consulta_sql(sql). Recibe la consulta SQL que ejecutará, desde este método se conectará a la
    Base de Datos y terminando de ejecutar la consulta se deconectará de la BD.

Utilizando la clase MySQL, cargue los datos a la Base de datos de:
    Estudiantes.txt
    Kardex.txt 

Genere las constraseñas a los estudiantes en una tabla llamada Usuarios, utilice la clase Password.

Para ello, cree la Base de Datos y las tablas: Estudiantes, Usuarios y Kardex con los campos que tienen
los archivos mencionados, considere integridad referencial.
Realice el CRUD a la tabla Kardex

Realice algo SIMILAR para MongoDB, considere solo consultas de una tabla.

para instalar mysql: pip install mysql-conector-python
para instalar pymongo: pip install pymongo
'''
from typing import List
import mysql.connector
class MySQL:
    def __init__ (self,vars_config):
        self.MYSQL_HOST=vars_config['host']
        self.MYSQL_USER=vars_config['user']
        self.MYSQL_PASSWORD=vars_config['pws']
        self.MYSQL_DATABASE=vars_config['db']
        self.MYSQL_CONNECTION= None
        self.MYSQL_CURSOR = None

    def myConexionSQL(self):
        if self.MYSQL_CONNECTION== None:
            try:
                    self.MYSQL_CONNECTION = mysql.connector.connect(host=self.MYSQL_HOST,user=self.MYSQL_USER,password=self.MYSQL_PASSWORD, database=self.MYSQL_DATABASE)
            except Exception as error:
                print("ERROR: ", error)
            else:
                return self.MYSQL_CONNECTION
    def desconectar_mysql(self):
        if self.MYSQL_CONNECTION is None:
            self.MYSQL_CONNECTION.close()

    def consulta(self,sql):
        self.MYSQL_CURSOR = self.MYSQL_CONNECTION.cursor()
        try:
            self.MYSQL_CURSOR.execute(sql)
        except mysql.connector.errors.ProgrammingError as e:
            print("Error en la consulta ", e)
        except Exception as error:
            print("ERROR: ", error)
        else:
            if (sql.upper().startswith("SELECT")):
                #for reg in self.MYSQL_CURSOR:
                    #print(reg)
                resultado = self.MYSQL_CURSOR.fetchall()
                return resultado
            else:
                self.MYSQL_CONNECTION.commit()
            self.MYSQL_CURSOR.close()
            self.desconectar_mysql()
            

            #self.MYSQL_CURSOR.close()
        #self.MYSQL_CONNECTION.close()  # Checar





#objMysql= MySQL()
#objMysql.myConexionSQL()
#objMysql.consulta("Select * from alumno")
#print("===========================")
#objMysql.myConexionSQL()
#objMysql.consulta("Select nombre carrera from alumno")

