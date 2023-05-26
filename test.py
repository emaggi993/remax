from core.conexion import Conexion

con = Conexion()
columnas = con.get_columnas_nombres('inmuebles')
con.close()
print(columnas)