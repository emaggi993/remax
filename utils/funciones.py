import json
from core import conexion as cn


def limpiar_cadena(cadena):
  return cadena.lower().replace("'",'-').replace('²','2').replace(' (m2)','_area').replace('mts2','').replace('(', '').replace(')', '').replace('/','_').replace('º', 'ro').replace(':', '').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('.','').replace('ñ','nh').strip().replace(' ','_').replace('_area','')

def crear_campo(propiedad):
  cursor = cn.Conexion().get_cursor_dic()
  query= "ALTER TABLE inmuebles ADD {} TEXT NULL AFTER observacion_inmueble".format(propiedad)
  cursor.execute(query)
  cursor.commit()
  cursor.close()

def convertir_float(cadena):
  if cadena == None:
    return float(0)
  return round(float(cadena.replace(",","")),2)

def eliminar_acentos(cadena):
  return cadena.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U")

def calular_precio_por_metro(total_calculado_inmueble, precio_actual_inmueble):
  t= convertir_float(total_calculado_inmueble)
  p= convertir_float(precio_actual_inmueble)
  if t != float(0):
    return str(round(float(p/t),2))
  else:
    return str(round(float(0),2))

def calcular_total(construido= None, lote= None, total= None):
  total_superficie = str(0)
  if construido == None and lote == None and total == None:
    total_superficie= str(0)
  elif construido == None and lote == None and total != None:
    total_superficie= total
  elif construido == None and lote != None:
    total_superficie= lote
  elif construido != None and lote == None:
    total_superficie= construido
  elif construido != None and lote != None:
    total_superficie= convertir_float(construido) + convertir_float(lote)
    if total_superficie < convertir_float(total):
      total_superficie= convertir_float(total)
    total_superficie = str(total_superficie)
  return total_superficie

def obtener_pais_departamento_ciudad(cadena):
  cadena= eliminar_acentos(cadena.upper())
  jsonFile = 'config.json'
  # jsonFile= 'H:\\core\\config.json'
# Open a json file for writing json data
  with open(jsonFile, encoding='utf8') as file:
    parametros = json.load(file)
  resul= {}
  resul['pais']= cadena.split(" ")[0]
  # print('pais ', resul['pais'])
  cadena= cadena.replace(resul['pais']+" ", "")
  depto_temp= cadena.split(" ",2)
  departamentos = parametros['DEPARTAMENTOS'].keys()
  depto =  eliminar_acentos( depto_temp[0]).upper().strip()
  # depto= depto_array[0]
  if depto not in departamentos:
    depto= depto_temp[0]+" "+ depto_temp[1]
  resul['departamento']= depto
  if depto == "ASUNCION":
    resul['ciudad']= "ASUNCION"
    cadena= cadena.replace(resul['departamento'],"")
    resul['barrio']= cadena.strip()
  else:
    cadena= cadena.replace(resul['departamento'],"")
    resul['ciudad']= cadena.strip()
  return resul