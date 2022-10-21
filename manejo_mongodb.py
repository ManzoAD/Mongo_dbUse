from ast import Try
from env import variables as varsql
from varmongo import variables as varmong
from crudmysql import MySQL
from mongodb import PyMongo
from caja import Password

def menu():
    while True:
        print('============== Menu Principal ==============')
        print('1. Insertar Estudiante')
        print('2. Actualizar Calificacion')
        print('3. Consultar Materias por estudiante')
        print('4. Consuta general de estudiante')
        print('5. Eliminar estudiante')
        print('6. Salir')
        print('Ingresa la opcion:')
        try:
            opcion= int(input(""))
        except Exception as error:
            print(f'ha ocurrido el siguiente error {error}')
        else:
            if opcion==1:
               insert_student()
            elif opcion==2:
                update_subject()
            elif opcion==3:
                search_subject()
            elif opcion==4:
                general_query()
            elif opcion==5:
                delete_student()
            elif opcion==6:
                break
            else:
                print('Opciones valida (1-6)')



def cargar_datos():
    print("----> Cargondo los datos ---->")
    obj_MySQL = MySQL(varsql)
    obj_PyMongo= PyMongo(varmong)
    #crear consultas
    sql_estudiante="Select * from estudiantes;"
    sql_kardex = "Select * From Kardex;"
    sql_usuario="Select * from usuarios"
    obj_MySQL.myConexionSQL()
    lista_estudiantes =obj_MySQL.consulta(sql_estudiante)
    lista_kardex=obj_MySQL.consulta(sql_kardex)
    lista_usuarios=obj_MySQL.consulta(sql_usuario)
    obj_MySQL.desconectar_mysql()

    #Insertar datos en mongo db
    obj_PyMongo.conectar_mongo()

    for est in lista_estudiantes:
        e = {
            'control':est[0],
            'nombre':est[1]
        }
        obj_PyMongo.insertar('estudiantes',e)

    for mat in lista_kardex:
        m= {
            'idKardex':mat[0],
            'control':mat[1],
            'materia':mat[2],
            'calificacion':float(mat[3])
        }
        obj_PyMongo.insertar('kardex',m)

    for usr in lista_usuarios:
        u={
            'idusuario':usr[0],
            'control':usr[1],
            'clave':usr[2],
            'clave_cifrada':usr[3]
        }
        obj_PyMongo.insertar('usuarios',u)
    obj_PyMongo.desconectar_mongodb()
    print("---> Carga Finalizada")

def insert_student():
    obj_PyMongo = PyMongo(varmong)
    print('=== Insertar Estudiantes ===')
    ctrl= input('Ingresa el N°: ')
    nomb=input('Ingresa el nombre: ')
    clav=input('Clave Acceso: ')
    obj_estudiante=Password(longitud=len(clav),contrasena=clav)
    json_estudiante={'control':ctrl,'nombre':nomb}
    json_usuarios={'idUsuario':100,'control':ctrl,'clave':clav,'clave_cifrada':obj_estudiante.contrasena_cifrada}
    obj_PyMongo.conectar_mongo()
    obj_PyMongo.colsulta_mongodb('estudiantes','')
    obj_PyMongo.insertar('estudiantes',json_estudiante)
    obj_PyMongo.insertar('usuarios',json_usuarios)
    obj_PyMongo.desconectar_mongodb()
    print("---> Insercion exitosa <---")

def update_subject():
    obj_PyMongo = PyMongo(varmong)
    print('==== Actualizar promedio ====')
    ctrl=input('Ingresa NC: ')
    materia= input('Ingresa materia: ')
    filtro_buscar_materia = {'control':ctrl , 'materia':materia}
    obj_PyMongo.conectar_mongo()
    respuesta= obj_PyMongo.colsulta_mongodb('kardex',filtro_buscar_materia)
    print(respuesta)
    if respuesta:
        prom=int(input('Dame el nuevo promedio: '))
        json_actuali_prom ={'$set':{'calificacion':prom}}
        rsp=obj_PyMongo.ActualizarDocuments('kardex',filtro_buscar_materia,json_actuali_prom)
        print(rsp)
        if rsp['status']:
            print("==== Promedio Actualizado ====\n")
        else:
            print('Ha ocurrido un error al actualizar')
    else:
        print(f'El estudiante con numero de control {ctrl} o la materia {materia} no ha sido encontrado\n')
    obj_PyMongo.desconectar_mongodb()

def search_subject():
    obj_PyMongo =PyMongo(varmong)
    print('==== Consultar materias por estudiante ====')
    ctrl= input("Dame el numero de control: ")

    filtro_general={'control':ctrl}
    atributos_estudiante={"_id":0,"nombre":1}
    atributos_kardex = {"_id":0,"materia":1,"calificacion":1}

    obj_PyMongo.conectar_mongo()
    respuesta1= obj_PyMongo.colsulta_mongodb('estudiantes',filtro_general,atributos_estudiante)
    respuesta2 =obj_PyMongo.colsulta_mongodb('kardex',filtro_general,atributos_kardex)

    if respuesta1['status'] and respuesta2['status']:
        print("Estudiante:",respuesta1['resultado'][0]["nombre"])
        for mat in respuesta2["resultado"]:
            print(mat["materia"],mat["calificacion"])
    obj_PyMongo.desconectar_mongodb()

def general_query():
    obj_PyMongo= PyMongo(varmong)
    obj_PyMongo.conectar_mongo()
    filtro={}
    dat=[]
    acu=0
    prom=0.0
    respuestaestudiante=obj_PyMongo.colsulta_mongodb('estudiantes',filtro)
    for i in respuestaestudiante['resultado']:
        respuestakardex=obj_PyMongo.colsulta_mongodb('kardex',{'control':i['control']})
        for j in respuestakardex['resultado']:
            acu+=j['calificacion']
        try:
            prom=acu/len(respuestakardex['resultado'])
        except ZeroDivisionError:
            print(f"El usuario {i['nombre']} no tiene materias por mostrar")
        else:
            dat.append({'control':i['control'],'nombre':i['nombre'],'promedio':prom})
            acu=0
            prom=0.0
    if dat != None:
        for a in dat:
            print(a)

    obj_PyMongo.desconectar_mongodb()

def delete_student():
    obj_PyMongo= PyMongo(varmong)
    ctrl=input('Ingresa numero control:')
    filtro_general={'control':ctrl}
    obj_PyMongo.conectar_mongo()

    respueststudiante=obj_PyMongo.colsulta_mongodb('estudiantes',filtro_general)
    respuestaKardex=obj_PyMongo.colsulta_mongodb('kardex',filtro_general)
    respuestausuario=obj_PyMongo.colsulta_mongodb('usuarios',filtro_general)
    
    if respueststudiante:
        print("¿Deseas eliminar al estudiante?")
        print(respueststudiante)
        valor=input('S / N: ')
        if valor=='S' or valor=='s':
            obj_PyMongo.deleteDocuments('estudiantes',filtro_general,1)
            if respuestaKardex:
                if len(respuestaKardex['resultado'][0])>1:
                    obj_PyMongo.deleteDocuments('kardex',filtro_general,2)
                else:
                    obj_PyMongo.deleteDocuments('kardex',filtro_general,1)
            if respuestausuario:
                obj_PyMongo.deleteDocuments('usuarios',filtro_general,1)
            print('=== Eliminacion Exitosa ===\n')
        else:
            print('=== Eliminacion Cancelada!!!! ===\n')

    else:
        print("Estudiante no encontrado")
    obj_PyMongo.desconectar_mongodb()
menu()