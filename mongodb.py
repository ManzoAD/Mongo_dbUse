
from urllib import response
import pymongo
from varmongo import variables
#from env import variables as varsmysql
from crudmysql import MySQL
#Conexion para mongo db
class PyMongo():
    def __init__(self,variables):
        self.MONGO_DATABASE = variables["db"]
        self.MONGO_URI = 'mongodb://'+variables["host"]+':'+str(variables["port"])
        self.MONGO_CLIENT =None
        self.MONGO_RESPUESTA= None
        self.MONGO_TIMEOUT=variables["timeout"]


    def conectar_mongo(self):

        try:
            self.MONGO_CLIENT =pymongo.MongoClient(self.MONGO_URI,serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
        except Exception as error:
            print("Error:",error)
        else:
            pass
            #print("Conexion al servidor realizada")

    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def colsulta_mongodb(self,tabla,filtro,atributos={"_id":0}):
        response ={"status":False,"resultado":[]}
        self.MONGO_RESPUESTA= self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find(filtro,atributos)
        if self.MONGO_RESPUESTA:
            response["status"]=True
            for reg in self.MONGO_RESPUESTA:
                response['resultado'].append(reg)
        return response

    def insertar(self,tabla,documento):
        self.MONGO_RESPUESTA= self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(documento)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
            #for reg in self.MONGO_RESPUESTA:
                #print(reg)
        else:
            return None

    def inserta_estudiante(self,tabla,estu):
        self.MONGO_RESPUESTA= self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(estu)
        if self.MONGO_RESPUESTA:
            return True
        else:
            return False


        #Actualizar documentos en las colecciones
    def ActualizarDocuments(self,tabla,filtro,nuevos_valores):
        response={"status":False}
        self.MONGO_RESPUESTA= self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_one(filtro,nuevos_valores)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            #return self.MONGO_RESPUESTA
        return response

    def deleteDocuments(self,tabla,filtro,val):
        response={"status":False}
        if val==1:
            self.MONGO_RESPUESTA=self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_one(filtro)
        elif val==2:
            self.MONGO_RESPUESTA=self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_many(filtro)
            
        if self.MONGO_RESPUESTA:
            response["status"]=True
        return response



alumno = {

    "control":200,
    "nombre":"Michael Jhordan"
}
#Lo creamos de nuevo en manejo_mongodb
def insert_student():
    """ obj_Mysql =MySQL(varsMysql)
    slq="SELECT * From estudiantes;"
    obj_Mysql.conectar_mysql()
    lista_estudiantes =obj_Mysql.consulta_sql(sql)
    obj_Mysql.desconectar_mysql()

    for est in lista_estudiantes:
        e = {
            "control": est[0],
            "nombre":est[1]
        }
        obj_Mongo.insertar_estudiante(e)
    obj_Mongo.desconectar_mongobd()
     """


#obj_Mongo=PyMongo(variables)
#obj_Mongo.conectar_mongo()
#obj_Mongo.inserta_estudiante('estudiantes',alumno)
#obj_Mongo.desconectar_mongodb()