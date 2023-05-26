from core import config
from datetime import date
import json

def get_data(anuncio, link):
    from utils.funciones import obtener_pais_departamento_ciudad, convertir_float, limpiar_cadena, calcular_total, calular_precio_por_metro
    from bs4 import BeautifulSoup
    import requests
    import re
    from core.conexion import Conexion
    conexion = Conexion()

    columns_table= conexion.get_columnas_nombres('inmuebles')


    ATRIBUTOS= {}
    into=""
    value=""
    datos_dic= {}
    #se obtienen los datos
    box= anuncio.find('div', class_='key-data')
    # encabezados = box.find_element(By.CLASS_NAME,'row')
    titulo= box.find('h1', itemprop='name').get_text().replace("'","")
    
    aux= titulo.split(' - ')
    id_anuncio = box.find('span', itemprop='productID').get_text().strip()
    datos_dic['id_inmueble'] = id_anuncio
    into += 'id_inmueble'+ ","
    value += "'"+datos_dic['id_inmueble']+ "',"

    datos_dic['tipo_inmueble']= aux[0]
    into += 'tipo_inmueble'+ ","
    value += "'"+datos_dic['tipo_inmueble']+ "',"

    datos_dic['operacion_inmueble'] = aux[1]
    into += 'operacion_inmueble'+ ","
    value += "'"+datos_dic['operacion_inmueble']+ "',"

    resul = obtener_pais_departamento_ciudad(aux[2])

    datos_dic['pais_inmueble']= resul['pais']
    into += 'pais_inmueble'+ ","
    value += "'"+datos_dic['pais_inmueble']+ "',"

    datos_dic['departamento_inmueble']= resul['departamento']
    into += 'departamento_inmueble'+ ","
    value += "'"+datos_dic['departamento_inmueble']+ "',"

    datos_dic['ciudad_inmueble'] = resul['ciudad']
    into += 'ciudad_inmueble'+ ","
    value += "'"+datos_dic['ciudad_inmueble']+ "',"

    if datos_dic['departamento_inmueble'].lower()== 'asuncion':
      datos_dic['barrio_inmueble']= resul['barrio'].replace("'","-").encode('utf8').decode('utf8')
      into += 'barrio_inmueble'+ ","
      value += "'"+datos_dic['barrio_inmueble']+ "',"
    
    if box.find('div', class_='key-status') != None:
      datos_dic['estado_inmueble']= box.find('div', class_='key-status').get_text().strip()
      into += 'estado_inmueble'+ ","
      value += "'"+ datos_dic['estado_inmueble']+ "',"
    precio_a = box.find('a', itemprop='price')
    if precio_a != None:
      precio = precio_a['content']
      datos_dic['precio_actual_inmueble'] = str(convertir_float(precio))
      into += 'precio_actual_inmueble'+ ","
      value += "'"+datos_dic['precio_actual_inmueble']+ "',"  

      datos_dic['hist_precio_inmueble']= json.dumps({str(date.today()) : datos_dic['precio_actual_inmueble'] })
      into += 'hist_precio_inmueble'+ ","
      value += "'"+datos_dic['hist_precio_inmueble']+ "',"

      datos_dic['moneda_inmueble'] = box.find('span', itemprop='priceCurrency')['content']
      into += 'moneda_inmueble'+ ","
      value += "'"+datos_dic['moneda_inmueble']+ "',"
      if datos_dic['moneda_inmueble'] == "PYG":
        datos_dic['precio_pyg_inmueble'] = str(convertir_float(box.find('a', itemprop='price')['content']))
        into += 'precio_pyg_inmueble'+ ","
        value += "'"+datos_dic['precio_pyg_inmueble']+ "',"
        url_moneda= config.URL_CALCULO_PRECIO.format(datos_dic['precio_pyg_inmueble'], "PYG")
        r = requests.get(url_moneda)
        anuncio_precio = BeautifulSoup(r.content, 'html.parser')
        otro_precio = str(convertir_float(anuncio_precio.find("td", class_="currency-value").get_text()))
        datos_dic["precio_usd_inmueble"]= otro_precio
        into += 'precio_usd_inmueble'+ ","
        value += "'"+datos_dic['precio_usd_inmueble']+ "',"
      elif datos_dic['moneda_inmueble'] == "USD" :
        datos_dic['precio_usd_inmueble'] = str(convertir_float(box.find('a', itemprop='price')['content']))
        into += 'precio_usd_inmueble'+ ","
        value += "'"+datos_dic['precio_usd_inmueble']+ "',"
        url_moneda= config.URL_CALCULO_PRECIO.format(datos_dic['precio_usd_inmueble'], "USD")
        r = requests.get(url_moneda)
        anuncio_precio = BeautifulSoup(r.content, 'html.parser')
        otro_precio = str(convertir_float(anuncio_precio.find("td", class_="currency-value").get_text()))
        datos_dic["precio_pyg_inmueble"]= otro_precio
        into += 'precio_pyg_inmueble'+ ","
        value += "'"+datos_dic['precio_pyg_inmueble']+ "',"
    else:
        datos_dic['precio_actual_inmueble']='0'
        into += 'precio_actual_inmueble'+ ","
        value += "'"+datos_dic['precio_actual_inmueble']+ "',"
        datos_dic["precio_usd_inmueble"]= str(0)
        into += 'precio_usd_inmueble'+ ","
        value += "'"+datos_dic['precio_usd_inmueble']+ "',"
        datos_dic["precio_pyg_inmueble"]= str(0)
        into += 'precio_pyg_inmueble'+ ","
        value += "'"+datos_dic['precio_pyg_inmueble']+ "',"
    
    temp_area= None
    lote = None
    #direccion es lo que sigue de lo que esta en el titulo
    direccion= limpiar_cadena(aux[2]).encode('utf8').decode('utf8')
    dir_aux= box.find('div', class_='key-address').get_text().replace("'", "")
    datos_dic['direccion_inmueble']= dir_aux.replace(direccion, '').strip()
    into += 'direccion_inmueble'+ ","
    value += "'"+datos_dic['direccion_inmueble']+ "',"
    items = box.findAll('div', class_='data-item-row')
    for item in items:
      atributo = item.find('div', class_='data-item-label')
      valor= item.find('div', class_='data-item-value')
      if atributo.find('span').get_text().strip() == 'Sup. Lote:':
        propiedad= 'dimensiones_inmueble'
      else:
        propiedad=  limpiar_cadena( atributo.find('span').get_text() )+'_inmueble' 
        if propiedad not in columns_table:
          print()
          print("Se agregró ",propiedad)
          print()
          conexion.crear_campo(propiedad)
        
          
      v=  valor.find('span').get_text().replace("'","-") 
      ATRIBUTOS[propiedad]= v
      datos_dic[propiedad]= v
      if propiedad == "area_de_construccion_inmueble":
        temp_area= v
      if propiedad == "sup_lote_inmueble":
        lote= v
      if propiedad == "total_inmueble":
        total_atributo= v
      into += propiedad+ ","
      value += "'"+datos_dic[propiedad]+ "',"
    datos_dic['total_calculado_inmueble']= calcular_total(construido= temp_area, lote= lote, total= total_atributo)
    into += 'total_calculado_inmueble'+ ","
    value += "'"+datos_dic['total_calculado_inmueble']+ "',"
    datos_dic['precio_mts_cuadrados_pyg_inmueble']= calular_precio_por_metro(datos_dic['total_calculado_inmueble'], datos_dic['precio_pyg_inmueble'])
    into += 'precio_mts_cuadrados_pyg_inmueble'+ ","
    value += "'"+datos_dic['precio_mts_cuadrados_pyg_inmueble']+ "',"
    datos_dic['precio_mts_cuadrados_usd_inmueble']= calular_precio_por_metro(datos_dic['total_calculado_inmueble'], datos_dic['precio_usd_inmueble'])
    into += 'precio_mts_cuadrados_usd_inmueble'+ ","
    value += "'"+datos_dic['precio_mts_cuadrados_usd_inmueble']+ "',"
    ubicacion= anuncio.find('input', id='listingfull-map-toggler')
    if ubicacion != None:
      datos_dic['latitud_inmueble']= ubicacion['data-lat']
      into += 'latitud_inmueble'+ ","
      value += "'"+datos_dic['latitud_inmueble']+ "',"

      datos_dic['longitud_inmueble']= ubicacion['data-lng']
      into += 'longitud_inmueble'+ ","
      value += "'"+datos_dic['longitud_inmueble']+ "',"

    else:
      datos_dic['latitud_inmueble']= 0
      datos_dic['longitud_inmueble']= 0

    datos_dic['atributos_inmueble']= json.dumps(ATRIBUTOS)
    into += 'atributos_inmueble'+ ","
    value += "'"+datos_dic['atributos_inmueble']+ "',"
    observacion= anuncio.find('div', itemprop='description')
    if observacion != None:
      observacion = observacion.get_text().encode('utf8').decode('utf8')
      datos_dic['observacion_inmueble'] = re.sub(r"[^a-zA-Z0-9 ./!\|@#$%^&*();,?><+=-_ñáÁéÉíÍóÓúÚñÑ]","",observacion) 
      into += 'observacion_inmueble'+ ","
      value += "'"+datos_dic['observacion_inmueble']+ "',"

    datos_dic['link_inmueble']= link+ "?Lang=es-PY"
    into += 'link_inmueble'
    value += "'"+datos_dic['link_inmueble']+"'"
    sql = "INSERT INTO inmuebles ("+into+") VALUES ("+value+") ON DUPLICATE KEY update id_inmueble = id_inmueble, precio_anterior_inmueble = precio_actual_inmueble, moneda_anterior_inmueble= moneda_inmueble, total_calculado_inmueble= values(total_calculado_inmueble), precio_mts_cuadrados_pyg_inmueble = values(precio_mts_cuadrados_pyg_inmueble), precio_mts_cuadrados_usd_inmueble = values(precio_mts_cuadrados_usd_inmueble), precio_actual_inmueble= values(precio_actual_inmueble), moneda_inmueble= values(moneda_inmueble)"
    conexion.insertar(sql)
    print("Se insertó el inmueble: ", titulo)
    print()