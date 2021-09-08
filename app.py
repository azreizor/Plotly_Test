import json
from flask import Flask, render_template
import pandas as pd
import plotly
import plotly.express as px
from datetime import date, datetime, time

from werkzeug.wrappers import request

app = Flask(__name__)
@app.route("/") # el nombre de la url de solicitud
def index():
    return render_template("index.html")





@app.route("/post", methods = ["POST"])
def post():
    calendar1 = request.form["calendar1"]
    print(calendar1)
    calendar2 = request.form["calendar2"]
    return render_template("post.html", calendar1=calendar1, calendar2=calendar2)









@app.route("/fechas")
def fechas():
    return render_template("fechas.html")

@app.route("/pandas")
def pandasdf():
    df = pd.read_excel('BASE_AGROSPARE_COMPLETA.xlsx', engine='openpyxl', sheet_name="VENTAS_MENSUALES")
    #df = pd.read_csv("VENTAS_SEMANALES_AGROSPARE2.csv", sep=";")
    #print(df.loc[0]["FECHA"])              #muestra la fecha del primer registro[0]
    #print("imprimir como dataframe", df)   #imprime el dataframe completo
    #print(df.head(10))                     #imprime los primeros 10 registros del dataframe
    #print(df.info())                       #imprime los tipos de datos en el dataframe
    #print(df.head(10)["FECHA"])            #imprime los primeros 10 registros de la columna FECHA
    #print(df.head()["TOTAL_SEMANAL"])      #imprime los primeros 5 registros de la columna TOTAL_SEMANAL
    #print(df["FECHA"])                     #imprime todos los registros de la columna FECHA
    #print(df["FECHA"].size)                #imprime la cantidad de registros existentes en la comuna FECHA
    #print(df.columns)                      #imprime los nombres de las columnas del dataframe
    #print(df.index)                        #imprime el total de registros del dataframe
    #print(df.rename(columns= 
    #{"FECHA":"fecha", "TOTAL_SEMANAL":"total"} #imprime el dataframe con el renombramiento de las columnas
    #))
    #print(pd.to_datetime(df["FECHA"]))     #imprime la columna FECHA en formato datetime
    #df["FECHA"] = pd.to_datetime(df["FECHA"]) #modifica la columna FECHA en formato datetime
    df["FECHA"] = pd.to_datetime(df["FECHA"])
    df = df.head(10)
    df = df.sort_values(by="FECHA")
    df = df.rename(columns={"FECHA":"Fecha", "TOTAL_MENSUAL":"Total Mensual"})
    figura = px.bar(
    data_frame= df,
    x = "Fecha", y = "Total Mensual"
    , color="Total Mensual"
    #, color_continuous_scale='Bluered_r' #escala de colores mixto rojo azul
    #, color_continuous_scale=["#ff0000", "green", "blue"] #escala de colores definidos
    #, color_continuous_scale=[  (0.00, "red"),   (0.33, "red"), #escala de colores por intervalos
    #                            (0.33, "green"), (0.66, "green"),
    #                            (0.66, "blue"),  (1.00, "blue")]
    #, range_color=[1,100] #calor de la barra lateral del color (nomenclatura de valores)
    #, pattern_shape = df["Total Mensual"] #patrones de diseño en grafico
    , title = "Total Mensuall" #titulo del grafico
    )
    print(figura)
    graficoJSON = json.dumps(figura, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("pandas.html", grafico = graficoJSON)


@app.route("/crear_json_ventas")
def crear_json_ventas():
    df = pd.read_csv("VENTAS_SEMANALES_AGROSPARE.csv", sep=";")
    df.to_json("ventas2.json")
    return render_template("crear_json_ventas.html")

@app.route("/leer_json_ventas")
def leer_json_ventas():
    json = pd.read_json("ventas2.json")
    return render_template("leer_json_ventas.html", json = json)

@app.route('/plotly1')
def plotly_1():
    df = pd.DataFrame({
        "Frutas": ["Manzana", "Naranja", "Platano", "Manzana", "Naranja", "Platano"],
        "Cantidad": [4, 1, 2, 2, 4, 5],
        "Ciudad": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})
    print(df)
    fig = px.bar(df, x="Frutas", y="Cantidad", color="Ciudad", barmode="group")
    print(fig)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Fruit in North America"
    description = """
    A academic study of the number of apples, oranges and bananas in the cities of
    San Francisco and Montreal would probably not come up with this chart.
    """
    return render_template('plotly.html', graphJSON=graphJSON, graphJSON2=graphJSON, header=header,description=description)





app.run(port=5000)
if __name__ == "__main__":
    app.run(debug=True)
    app.debug(debug=True)