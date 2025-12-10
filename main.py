#TP1
#Tenemos 4 tablas:

import pandas as pd    
import duckdb as db
import matplotlib.pyplot as plt
import seaborn as sns

#Abrimos todas las tablas y las guardamos en dataframes

educacion_original = pd.read_excel('Tablas_Originales/2022_padron_oficial_establecimientos_educativos.xlsx', skiprows=6)
produccion_original = pd.read_csv('Tablas_Originales/Datos_por_departamento_actividad_y_sexo.csv')
actividades_original = pd.read_csv('Tablas_Originales/actividades_establecimientos.csv')
padron_original = pd.read_excel('Tablas_Originales/padron_poblacion.xlsx', skiprows = 12)

#Pasamos todos los datos a la tabla normalizada departamentos_info

padron_original = padron_original.iloc[:, 1:5] #Nos quedamos solo con las columnas que queremos

padron_original.dropna(axis=0, how="all", inplace=True) #Eliminamos filas nulas de padron

departamentos_info = pd.DataFrame(columns=["Departamento_Id", "Departamento_Nombre", "Provincia_Nombre", "Poblacion_Jardin", "Poblacion_Primario", "Poblacion_Secundario", "Poblacion_Total"])
#Pasamos los datos
i = 0
while i < len(padron_original):
    valor_columna1 = str(padron_original.iloc[i, 0]).strip()
    valor_columna2 = str(padron_original.iloc[i,1]).strip()
    if valor_columna1.startswith("AREA"):
        Departamento_Id = valor_columna1[-5:]
        Departamento_Nombre = valor_columna2
        Poblacion_Jardin = 0
        Poblacion_Primario = 0
        Poblacion_Secundario = 0
        Poblacion_Total = 0
        i += 2 #Nos salteamos la fila de nombres de las columnas
        while not str(padron_original.iloc[i, 0]).strip().startswith("Total"):
            edad = int(padron_original.iloc[i,0])
            cant_habitantes = int(padron_original.iloc[i,1])
            if 3 <= edad <= 5:
                Poblacion_Jardin += cant_habitantes
            elif 6 <= edad <= 12:
                Poblacion_Primario += cant_habitantes
            elif 13 <= edad <= 17:
                Poblacion_Secundario += cant_habitantes
            i += 1
        Poblacion_Total = int(padron_original.iloc[i,1])
        departamentos_info.loc[len(departamentos_info)] = [Departamento_Id, Departamento_Nombre, None, Poblacion_Jardin, Poblacion_Primario, Poblacion_Secundario, Poblacion_Total]
        i += 1
    else:
        i += 1

#Modificamos valores a mano que están mal.
departamentos_info["Departamento_Id"] = departamentos_info["Departamento_Id"].replace({"94015": "94014","94008": "94007"})

#Falta agregar las provincias que sacaremos de la tabla de produccion
#Creamos una tabla provisoria de produccion para relacionar las provincias
produccion_provisoria = produccion_original.copy()

#Modificamos los id de los departamentos que estan mal en la tabla original
produccion_provisoria["in_departamentos"] = produccion_provisoria["in_departamentos"].astype(str).str.zfill(5)

#Eliminamos los ids repetidos
produccion_provisoria = produccion_provisoria.drop_duplicates(subset="in_departamentos", keep="first")

#Reemplazamos datos que están mal en la tabla
produccion_provisoria["in_departamentos"] = produccion_provisoria["in_departamentos"].replace("06217", "06218")

#Definimos el id del departamento como indice sabiendo que no se repiten
produccion_provisoria = produccion_provisoria.set_index("in_departamentos")

#Completamos el nombre de las provincias
i = 0
while i < len(departamentos_info):
    id_departamento = departamentos_info.loc[i, "Departamento_Id"]
    provincia = produccion_provisoria.loc[id_departamento, "provincia"] #Usamos el indice de la tabla
    if provincia == "CABA":
        provincia = "Buenos Aires"
    departamentos_info.loc[i, "Provincia_Nombre"] = provincia
    i += 1
#Guardamos la tabla como archivo de excel 
departamentos_info.to_excel('Tablas_Finales/departamentos_info.xlsx', index=False)

#Pasamos todos los datos a la tabla normalizada establecimientos_productivos
establecimientos_productivos = produccion_original.iloc[:, [5, 1, 8, 9, 10, 11]].copy()

#Renombramos las columnas para que coincida con nuestro modelo relacional
establecimientos_productivos.columns = ["Clae6", "Departamento_Id", "Genero", "Cant_Empleados", "Cant_Establecimientos", "Cant_Empresas_Exportadoras"]

#Pasamos todos los id de los departamentos a string
establecimientos_productivos["Departamento_Id"] = establecimientos_productivos["Departamento_Id"].astype(str)

#A todos los Id de departamentos que tienen longitud 4 les agregamos un 0 a la izquierda
establecimientos_productivos["Departamento_Id"] = establecimientos_productivos["Departamento_Id"].str.zfill(5)

#Reemplazamos datos que están mal
establecimientos_productivos["Departamento_Id"] = establecimientos_productivos["Departamento_Id"].replace("06217", "06218")

#Guardamos la tabla como archivo de excel
establecimientos_productivos.to_excel('Tablas_Finales/establecimientos_productivos.xlsx', index=False)


#Pasamos todos los datos a la tabla normalizada establecimientos_educativos
establecimientos_educativos = educacion_original.iloc[:, [1, 9, 2, 3]].copy()

#Renombramos las columnas para que coincidan con nuestro modelo relacional
establecimientos_educativos.columns = ["Cueanexo", "Departamento_Id", "Establecimiento_Nombre", "Sector"]

#Pasamos los id de los departamentos a string
establecimientos_educativos["Departamento_Id"] = establecimientos_educativos["Departamento_Id"].astype(str)

#A todos los id de departamentos que tienen longitud 7 les agregamos un 0 a la izquierda
establecimientos_educativos["Departamento_Id"] = establecimientos_educativos["Departamento_Id"].astype(str).str.zfill(8)

#Ahora de los codigos de localidades que teniamos nos quedamos solo con los primeros 5 digitos que son los del id del departamento
establecimientos_educativos["Departamento_Id"] = establecimientos_educativos["Departamento_Id"].str[:5]

datos_a_cambiar = {"02101": "02007",
                   "02102": "02014",
                   "02103": "02021",
                   "02104": "02028",
                   "02105": "02035",
                   "02106": "02042",
                   "02107": "02049",
                   "02108": "02056",
                   "02109": "02063",
                   "02110": "02070",
                   "02111": "02077",
                   "02112": "02084",
                   "02113": "02091",
                   "02114": "02098",
                   "02115": "02105"}

#Reemplazamos los valores ques están mal
establecimientos_educativos["Departamento_Id"] = establecimientos_educativos["Departamento_Id"].replace(datos_a_cambiar)

#Guardamos la tabla como archivo de excel
establecimientos_educativos.to_excel('Tablas_Finales/establecimientos_educativos.xlsx', index=False)


#Ahora pasamos los datos a la tabla de niveles educativos

#Creamos una tabla provisoria para limpiar los datos
educacion_provisoria = educacion_original.copy()

#A las columnas que nos interesan les eliminamos los espacios al principio y al final
educacion_provisoria[["Común", "Nivel inicial - Jardín de infantes", "Primario", "Secundario"]] = educacion_provisoria[["Común", "Nivel inicial - Jardín de infantes", "Primario", "Secundario"]].astype(str).apply(lambda fila: fila.str.strip())

#Nos quedamos solo con los establecimientos comunes
educacion_provisoria = educacion_provisoria[educacion_provisoria["Común"] == "1"]

#Creamos la tabla final normalizada
niveles_educativos = pd.DataFrame(columns=["Cueanexo", "Nivel"])

#Pasamos todos los datos a la tabla
i = 0
while i < len(educacion_provisoria):
    Cueanexo = educacion_provisoria.iloc[i, 1]  
    nivel_jardin = educacion_provisoria.iloc[i, 21]
    nivel_primaria = educacion_provisoria.iloc[i, 22]
    nivel_secundaria = educacion_provisoria.iloc[i, 23]
    if nivel_jardin == "1":
        niveles_educativos.loc[len(niveles_educativos)] = [Cueanexo, "Jardin"]
    if nivel_primaria == "1":
        niveles_educativos.loc[len(niveles_educativos)] = [Cueanexo, "Primaria"]
    if nivel_secundaria == "1":
        niveles_educativos.loc[len(niveles_educativos)] = [Cueanexo, "Secundaria"]
    i += 1
    
#Guardamos la tabla como archivo de excel
niveles_educativos.to_excel('Tablas_Finales/niveles_educativos.xlsx', index=False)

#La tabla actividades economicas queda como estaba originalmente
actividades_economicas = actividades_original.copy() 

#Guardamos la tabla como archivo de excel
actividades_economicas.to_excel('Tablas_Finales/actividades_economicas.xlsx', index=False)


#Ejercicio de consultas i)

consulta_ee = """SELECT d.Provincia_Nombre AS Provincia,
d.Departamento_Nombre AS Departamento,
SUM(CASE WHEN n.Nivel = 'Jardin' THEN 1 ELSE 0 END) AS Jardines,
d.Poblacion_Jardin AS "Población Jardin",
SUM(CASE WHEN n.Nivel = 'Primaria' THEN 1 ELSE 0 END) AS Primarias,
d.Poblacion_Primario AS "Población Primaria",
SUM(CASE WHEN n.Nivel = 'Secundaria' THEN 1 ELSE 0 END) AS Secundarias,
d.Poblacion_Secundario AS "Población Secundaria"
FROM departamentos_info d
LEFT JOIN establecimientos_educativos e ON d.Departamento_Id = e.Departamento_Id
LEFT JOIN niveles_educativos n ON e.Cueanexo = n.Cueanexo
GROUP BY d.Provincia_Nombre, d.Departamento_Nombre, d.Poblacion_Jardin, 
d.Poblacion_Primario, d.Poblacion_Secundario
ORDER BY Provincia ASC, Primarias DESC"""
reporte_i = db.query(consulta_ee).to_df()
reporte_i.to_excel("Reportes_TP/reporte_i.xlsx", index=False)



#Ejercicio de consultas ii)
consulta_empleados = """
SELECT d.Provincia_Nombre AS Provincia, d.Departamento_Nombre AS Departamento,
SUM(p.Cant_Empleados) AS "Cantidad total de empleados en 2022"
FROM departamentos_info d
LEFT JOIN establecimientos_productivos p
ON d.Departamento_Id = p.Departamento_Id
GROUP BY d.Provincia_Nombre, d.Departamento_Nombre
ORDER BY Provincia ASC, "Cantidad total de empleados en 2022" DESC
"""
reporte_ii = db.query(consulta_empleados).to_df()
reporte_ii.to_excel("Reportes_TP/reporte_ii.xlsx", index=False)


#Ejercicio de consultas iii)

consulta_exportadoras = """SELECT e.Departamento_Id,
d.Provincia_Nombre AS Provincia,
d.Departamento_Nombre AS Departamento,
p."Cantidad de empresas exportadoras con mujeres",
COUNT(e.Cueanexo) AS "Cantidad de EE",
d.Poblacion_Total AS "Población Total"
FROM establecimientos_educativos e
LEFT JOIN departamentos_info d
ON e.Departamento_Id = d.Departamento_Id
LEFT JOIN (SELECT p.Departamento_Id,
SUM(p.Cant_Empresas_Exportadoras) AS "Cantidad de empresas exportadoras con mujeres"
FROM establecimientos_productivos p
WHERE p.Genero = 'Mujeres'
GROUP BY p.Departamento_Id) p
ON e.Departamento_Id = p.Departamento_Id
GROUP BY e.Departamento_Id, d.Provincia_Nombre, d.Departamento_Nombre, 
d.Poblacion_Total, p."Cantidad de empresas exportadoras con mujeres"
ORDER BY "Cantidad de EE" DESC, "Cantidad de empresas exportadoras con mujeres" DESC,
Provincia ASC, Departamento ASC"""
reporte_iii = db.query(consulta_exportadoras).to_df()
reporte_iii.to_excel("Reportes_TP/reporte_iii.xlsx", index=False)




#Ejercicio de consultas iv)    
empleos_departamento_query = """
SELECT a.Departamento_Id, SUM(a.Cant_Empleados) AS Total_Empleados, b.Provincia_Nombre
FROM establecimientos_productivos AS a
JOIN departamentos_info AS b
ON a.Departamento_Id = b.Departamento_Id
GROUP BY a.Departamento_Id, b.Provincia_Nombre
ORDER BY b.Provincia_Nombre
"""
empleos_departamento = db.query(empleos_departamento_query).to_df()

departamentos_por_provincia_query = """
SELECT Provincia_Nombre, COUNT(DISTINCT Departamento_Id) AS Cantidad_Departamentos
FROM departamentos_info
GROUP BY Provincia_Nombre
"""
departamentos_por_provincia = db.query(departamentos_por_provincia_query).to_df()

empleados_por_provincia_query = """
SELECT Provincia_Nombre, SUM(Total_Empleados) AS Empleados_Provincia
FROM empleos_departamento
GROUP BY Provincia_Nombre
"""
empleados_por_provincia = db.query(empleados_por_provincia_query).to_df()

promedio_empleados_query = """
SELECT p.Provincia_Nombre, p.Empleados_Provincia, d.Cantidad_Departamentos,
p.Empleados_Provincia * 1.0 / d.Cantidad_Departamentos AS Promedio_Provincial
FROM empleados_por_provincia p
JOIN departamentos_por_provincia d
ON p.Provincia_Nombre = d.Provincia_Nombre
"""
promedio_empleados = db.query(promedio_empleados_query).to_df()

clae6_departamento_query = """ 
SELECT b.Provincia_Nombre, b.Departamento_Nombre, b.Departamento_Id, a.CLAE6, SUM(a.Cant_Empleados) AS Empleados_Rubro 
FROM establecimientos_productivos AS a 
JOIN departamentos_info AS b 
ON a.Departamento_Id = b.Departamento_Id 
GROUP BY b.Provincia_Nombre, b.Departamento_Nombre, a.CLAE6, b.Departamento_Id 
ORDER BY b.Provincia_Nombre, b.Departamento_Nombre, Empleados_Rubro DESC 
""" 
clae6_departamento = db.query(clae6_departamento_query).to_df()

departamentos_arriba_promedio_query = """
SELECT a.Departamento_Id, a.Total_Empleados, a.Provincia_Nombre
FROM empleos_departamento AS a
JOIN promedio_empleados AS b
ON a.Provincia_Nombre = b.Provincia_Nombre
WHERE a.Total_Empleados > b.Promedio_Provincial
"""
departamentos_arriba_promedio = db.query(departamentos_arriba_promedio_query).to_df()

clae6_filtrado_query = """
SELECT a.*
FROM clae6_departamento AS a
INNER JOIN departamentos_arriba_promedio AS b
ON a.Departamento_Id = b.Departamento_Id
"""
clae6_filtrado = db.query(clae6_filtrado_query).to_df()

max_por_departamento_query = """
SELECT Departamento_Id, MAX(Empleados_Rubro) AS Max_Empleados_Rubro
FROM clae6_filtrado
GROUP BY Departamento_Id
"""
max_por_departamento = db.query(max_por_departamento_query).to_df()

clae6_final_query = """
SELECT a.Provincia_Nombre, a.Departamento_Nombre, a.Departamento_Id, a.CLAE6, a.Empleados_Rubro
FROM clae6_filtrado AS a
INNER JOIN max_por_departamento AS b
ON a.Departamento_Id = b.Departamento_Id
AND a.Empleados_Rubro = b.Max_Empleados_Rubro
"""
clae6_final = db.query(clae6_final_query).to_df()

clae6_final["Clae6"] = clae6_final["Clae6"].astype(str)
clae6_final["Clae3"] = clae6_final["Clae6"].str.zfill(6).str[:3]

resultado_final_query = """
SELECT Provincia_Nombre AS Nombre,
       Departamento_Nombre AS Departamento,
       Clae3 AS CLAE3,
       Empleados_Rubro AS Cant_Empleados
FROM clae6_final
"""
reporte_iv = db.query(resultado_final_query).to_df()

reporte_iv.to_excel('Reportes_TP/reporte_iv.xlsx', index=False)

     
#GRAFICOS:
#i)
empleados_x_provincia = db.query("""SELECT d.provincia_nombre AS Provincia, 
SUM(p.cant_empleados) AS "Cantidad de Empleados"
FROM establecimientos_productivos p LEFT JOIN departamentos_info d ON
p.Departamento_Id = d.Departamento_Id GROUP BY d.provincia_nombre
ORDER BY "Cantidad de Empleados" DESC
                                 """).to_df()
empleados_x_provincia.plot(
    kind="bar",
    x="Provincia",
    y="Cantidad de Empleados",
    title="Empleados por Provincia",
    legend = False,
    width = 0.8, #Ensanchamos las barras
    ylabel = "Cantidad de Empleados")
plt.title("Empleados por Provincia", weight = "bold")
plt.xticks(rotation=45, ha="right")  #Rotamos los nombres para que se lean mejor
plt.tight_layout()  #Hace que no se superpongan los nombres
plt.savefig("Graficos_TP/Empleados_por_Provincia.png", dpi=300, bbox_inches="tight")

#ii) 
#Creamos el grafico con un tamaño mayor ya que son muchos puntos a graficar
plt.figure(figsize=(9,6)) 
plt.scatter(
    reporte_departamentos["Población Jardin"],
    reporte_departamentos["Jardines"],
    color="orange",
    label="Nivel Inicial",
    alpha=0.7, #Hacemos los puntos mas transparentes porque se superponen muchos
    edgecolors="Black", #Colocamos contorno negro en cada punto
    s=70) #Agrandamos el tamaño de los puntos)
plt.scatter(
    reporte_departamentos["Población Primaria"],
    reporte_departamentos["Primarias"],
    color="dodgerblue",
    label="Nivel Primario",
    alpha=0.7,
    edgecolors="Black",
    s=70)
plt.scatter(
    reporte_departamentos["Población Secundaria"],
    reporte_departamentos["Secundarias"],
    color="green",  # verde
    label="Nivel Secundario",
    alpha=0.7,
    edgecolors="Black",
    s=70)
plt.title("Relación entre Población y Cantidad de Escuelas por Nivel Educativo", fontsize=13, weight="bold")
plt.xlabel("Población del grupo etario")
plt.ylabel("Cantidad de establecimientos educativos (EE)")
plt.legend(fontsize=12)
plt.grid(visible=True, alpha=0.5)
plt.tight_layout()
plt.savefig("Graficos_TP/Relación_entre_Población_y_Cantidad_de_Escuelas_por_Nivel_Educativo.png", dpi=300, bbox_inches="tight")

# iii) Boxplot: cantidad de EE por departamento de cada provincia
ee_por_departamento = db.query("""SELECT r.Provincia, r.Departamento,
(r.Jardines + r.Primarias + r.Secundarias) AS cant_ee FROM reporte_departamentos r""").to_df()

mediana_por_provincia = db.query("""SELECT Provincia, MEDIAN(e.cant_ee) AS mediana
FROM ee_por_departamento e
GROUP BY Provincia ORDER BY mediana ASC""").to_df()
#Nos quedamos con la lista de las provincias ordenadas por mediana
provincias_ordenadas = mediana_por_provincia["Provincia"].tolist()

plt.figure(figsize=(14,6))
sns.boxplot(
    data=ee_por_departamento,
    x="Provincia",
    y="cant_ee",
    order=provincias_ordenadas,
    palette="tab20",  #Usamos una paleta de colores para diferenciar cada provincia
    flierprops=dict(markerfacecolor='red'))  # Personalización de outliers

plt.xticks(rotation=45, ha="right")
plt.xlabel("Provincia")
plt.ylabel("Cantidad de Establecimientos Educativos por Departamento")
plt.title("Distribución de Establecimientos Educativos por Departamento en cada Provincia", weight="bold")
plt.grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Graficos_TP/Distribución_de_Establecimientos_Educativos_por_Departamento_en_cada_Provincia.png", dpi=300, bbox_inches="tight")

#iv)
relacion_empleados_ee = db.query("""
SELECT 
    d.Departamento_Id,
    d.Poblacion_Total,
    SUM(p.Cant_Empleados) AS total_empleados,
    (SUM(p.Cant_Empleados) / d.Poblacion_Total) * 1000 AS empleados_cada_mil,
    (COUNT(e.Cueanexo) / d.Poblacion_Total) * 1000 AS ee_cada_mil
FROM departamentos_info d
LEFT JOIN establecimientos_productivos p
    ON d.Departamento_Id = p.Departamento_Id
LEFT JOIN establecimientos_educativos e
    ON d.Departamento_Id = e.Departamento_Id
GROUP BY d.Departamento_Id, d.Poblacion_Total
""").to_df()

plt.figure(figsize=(10,6))
plt.scatter(
    relacion_empleados_ee["ee_cada_mil"], 
    relacion_empleados_ee["empleados_cada_mil"],
    color="dodgerblue",
    edgecolor="black",
    s=70,
    alpha=0.7
)

plt.xlabel("Cantidad de EE por 1000 habitantes")
plt.ylabel("Cantidad de empleados por 1000 habitantes")
plt.title("Relación entre empleados y EE cada mil habitantes", weight="bold")
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig("Graficos_TP/Relación_entre_empleados_y_EE_cada_mil_habitantes.png", dpi=300, bbox_inches="tight")


#v)
proporcion_mujeres = db.query("""
SELECT
    Clae6,
    SUM(CASE WHEN Genero = 'Mujeres' THEN Cant_Empleados ELSE 0 END) / SUM(Cant_Empleados) AS prop_mujeres
FROM establecimientos_productivos
GROUP BY Clae6
ORDER BY prop_mujeres DESC
""").to_df()

# Top 5 y Bottom 5
top5 = proporcion_mujeres.head(5)
bottom5 = proporcion_mujeres.tail(5)
top_bottom = pd.concat([top5, bottom5])

# Convertir Clae6 a string
top_bottom["Clae6"] = top_bottom["Clae6"].astype(str)

# Promedio de proporción de empleadas
promedio = proporcion_mujeres["prop_mujeres"].mean()

# Graficar
plt.figure(figsize=(12,6))
plt.bar(
    top_bottom["Clae6"], 
    top_bottom["prop_mujeres"], 
    color="dodgerblue", 
    edgecolor="black",
    width=0.9)
plt.axhline(promedio, color="red", linestyle="--", label="Promedio")
plt.xlabel("Actividad (CLAE6)")
plt.ylabel("Proporción de empleadas mujeres")
plt.title("Proporción de empleadas mujeres por actividad", weight="bold")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig("Graficos_TP/Proporción_de_empleadas_mujeres_por_actividad.png", dpi=300, bbox_inches="tight")







