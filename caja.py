import datetime
import random
import bcrypt

'''
Unidad 3: Programación Orientada a objetos
Tema: 1.1 Clases y objetos
Fecha: 28 de septiembre del 2022
Autor: Leonardo Martínez González

Clases y objetos en Python : https://www.youtube.com/watch?v=aj4PEXq0zuc
'''


'''
Sumar y restar dias a la fecha: https://j2logo.com/operaciones-con-fechas-en-python/
Generar numeros aleatorios: https://j2logo.com/python/generar-numeros-aleatorios-en-python/
Código ASCII:  https://elcodigoascii.com.ar/
Convertir un INT a ASCII: https://www.delftstack.com/es/howto/python/python-int-to-ascii/
Descargue la libreria bcrypt con el comando: "pip install bcrypt"

Realizar una clase llamada Password que siga las siguientes condiciones:
▪ Que tenga los atributos longitud, contraseña y fecha_expiracion. Por defecto, la longitud sera de 8, la contraseña
  será los números del 1 al 8 y la fecha_expiración será de UN día.
  
▪ Un constructor con la contraseña y fecha_expiracion que nosotros le pasemos, se calculará la longitud de la contrasena

Generará una contraseña aleatoria con esa longitud.

▪ Los métodos que implementa serán:
▪ esFuerte(): devuelve un booleano si es fuerte o no, para que sea fuerte debe tener mas de 2 mayúsculas, al menos una
minúscula y al menos  1 caracter.

▪ generarPassword(): genera la contraseña del objeto con la longitud que tenga.

▪ cifraPassword(): cifra la contraseña del objeto.

▪ verificarClave: regresará verdadero si la contrasena es correcta.

▪ Método get para contraseña y longitud.

▪ Método set para longitud.

Ahora, crea una clase clase ejecutable(main):
▪ Crea un array de Passwords con el tamaño que tu le indiques por teclado.
▪ Crea un bucle que cree un objeto para cada posición del array.
▪ Indica también por teclado la longitud de los Passwords (antes de bucle).
▪ Crea otro array de booleanos donde se almacene si el password del array de Password es o no fuerte (usa el bucle anterior).
▪ Al final, muestra la contraseña y si es o no fuerte (usa el bucle anterior). Usa este simple formato:
contraseña1 valor_booleano1
contraseña2 valor_bololeano2
'''
from datetime import datetime

class Password:
  # Constructor longitud,contraseña y fecha de expiracion
  def __init__(self,longitud=8,contrasena='123456789'):
    self.longitud = longitud
    self.contrasena = contrasena
    self.fechaexpiracion = datetime.today()
    self.contrasena_cifrada = self.cifrar_contra()

  def __str__(self):
    return f"Contraseña:{self.contrasena} contraseña cifrada: {self.contrasena_cifrada}"

  #Metodo generar contraseña
  def generar_password(self,contra):
    clave = ""
    for i in range(self.longitud):
      #Generar aleatoriamente numero del 1 al 4
      numero = random.randint(1,4)
      if numero ==1: #Letras Mayusculas
        clave += self.generar_mayusculas()
      elif numero==2: #Letras minusculas
        clave += self.generar_minusculas()
      elif numero==3: #Numeros
        clave += str(self.generar_numeros())
      elif numero==4: #Caracteres aleatorios
         clave += self.generar_caractes()
    self.contrasena = clave
    self.cifrar_contra()

  def generar_mayusculas(self):
    return chr(random.randint(65,90))

  def generar_minusculas(self):
    return chr(random.randint(97,122))

  def generar_numeros(self):
    return random.randint(0,9)

  def generar_caractes(self):
    listaCa=['?','*','$','&','#','.','¡','%','!']
    return listaCa[random.randint(0,7)]

  def cifrar_contra(self):
    sal = bcrypt.gensalt()
    contra_cifrada = bcrypt.hashpw(self.contrasena.encode('utf-8'),sal)
    return contra_cifrada


  def validar(self):
                                                #self.contrasena_cifrada
    return(bcrypt.checkpw((self.contrasena).decode('utf-8'),(self.contrasena_cifrada).decode('utf-8')))

  def es_fuerte(self):
    contador_mayusculas=0;
    contador_minusculas=0;
    contador_caracteres=0;
    contador_numeros=0;
    for car in self.contrasena:
      if ord(car)>=65 and ord(car)<=90: #Letra mayuscula
        contador_mayusculas+=1;
      elif ord(car)>=97 and ord(car)<=122: #Letra minuscula
        contador_minusculas+=1;
      elif ord(car) >= 48 and ord(car)<=57: #Numeros
        contador_numeros+=1;
      else: #Caracter especial
        contador_caracteres+=1;

    if contador_mayusculas >= 2 and contador_minusculas >=1 and contador_caracteres >=1:
      return True
    return False
    
def  app():
  pws=[]
  arr_fuertes=[]
  numero_elementos = int(input("Dame cuantos elementos quieres: "))
  longitud =int(input("Dame la longitud: "))
  for i in range(numero_elementos):
    objPassword= Password(longitud=longitud)
    objPassword.generar_password()
    pws.append(objPassword)
    arr_fuertes.append(objPassword.es_fuerte())
  for i in range(numero_elementos):
    print(pws[i].contrasena,arr_fuertes[i])
#app()
#objPass = Password()
#print(objPass)


#print(objPass.fechaexpiracion)
#if(bcrypt.checkpw((contra).encode('utf-8'),(us[2]).encode('utf-8'))):
""" mycontra=objPass.generar_password()
mycontracif=objPass.cifrar_contra(mycontra)
print("Mi contraseña")
print(mycontra)
print("Mi contraseña encriptada")
print(mycontracif) """
#print("Son validas")
#objPass.validar(mycontracif,mycontra)

