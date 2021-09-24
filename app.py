import json, math
import types
from flask import Flask, render_template, request, redirect, url_for
from numpy import mod
import pandas as pd
import plotly
import plotly.express as px, plotly.graph_objects as go
from datetime import date, datetime, time

app = Flask(__name__)
@app.route("/") # el nombre de la url de solicitud
#-------------------------------------------------------------------------------
def index():
    return render_template("index.html")
#-------------------------------------------------------------------------------
@app.route("/diario")
def diario():
    df = pd.read_excel('BASE_AGROSPARE_COMPLETA.xlsx', engine='openpyxl', sheet_name="VENTAS_DIARIAS")
    df["FECHA"] = pd.to_datetime(df["FECHA"]).dt.date
    sumatoria_dia = df.groupby("DIA_SEMANA").sum()
    dia_top3 = sumatoria_dia.nlargest(3,"TOTAL_DIARIO")
    separados = []
    dias = []
    
    colores = ["success", "warning", "danger"]
    for numero in range(dia_top3["TOTAL_DIARIO"].size):
        dias.append(dia_top3.index[numero])
        separados.append(format(dia_top3["TOTAL_DIARIO"][numero], ',d'))
    dia_top3["DIA"] = dias
    dia_top3["COLORES"] = colores
    dia_top3["SEPARADOS"] = separados
    print(dia_top3)
    print(dia_top3.dtypes)
    lista_dias = dia_top3.values.tolist()
    fig = px.pie(
        data_frame = df,
        names = 'DIA_SEMANA' ,
        values = 'TOTAL_DIARIO',
        title="Ventas Diarias",
        color_discrete_sequence=px.colors.sequential.Emrld)
    fig.update_traces(
        textinfo="percent+label")
    graficoJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------------------------------------------
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df["FECHA"],
            y=df["TOTAL_DIARIO"],
                mode='lines',
                name='lines'))
    grafico2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------------------------------------------
    fig3 = go.Figure(
        go.Scatter(
            x = df['FECHA'],
            y = df['TOTAL_DIARIO'],
            mode='lines'))
    grafico3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------------------------------------------
    fig4 = go.Figure()
    fig4.add_trace(
        go.Scatter(
            x=list(df["FECHA"]),
            y=list(df["TOTAL_DIARIO"])))
    grafico4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------------------------------------------
    lista_datos = df.values.tolist()
    #print(df.head(1))

    return render_template("diario.html", grafico = graficoJSON, top3=lista_dias, plot2 = grafico2JSON, lista_datos=lista_datos)



#-------------------------------------------------------------------------------
@app.route("/post_filtro_fecha", methods = ['POST'])
def post_filtro_fecha():
    if request.method == "POST":
        fecha_inicio = request.form["calendar1"]
        fecha_fin = request.form["calendar2"]
        df = pd.read_excel('BASE_AGROSPARE_COMPLETA.xlsx', engine='openpyxl', sheet_name="VENTAS_MENSUALES")
        df["FECHA"] = pd.to_datetime(df["FECHA"])
        df = df.head(10)
        mascara = (df["FECHA"] >= fecha_inicio) & (df["FECHA"] <= fecha_fin)
        datos = []
        mascara = pd.DataFrame(mascara)
        indice = mascara["FECHA"].size
        for numero in range(indice):
            if mascara["FECHA"].loc[numero] == True:
                datos.append(df.loc[numero])
                print(df["FECHA"].loc[numero])
        df_filtrado = pd.DataFrame(datos)
        print(df_filtrado)

        return render_template("post_filtro_fecha.html")
    else:
        return redirect(url_for('pre_filtro_fecha'))


#-------------------------------------------------------------------------------
@app.route("/pre_filtro_fecha")
def pre_filtro_fecha():
    return render_template("pre_filtro_fecha.html")
#-------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
@app.route("/crear_json_ventas")
def crear_json_ventas():
    df = pd.read_csv("VENTAS_SEMANALES_AGROSPARE.csv", sep=";")
    df.to_json("ventas2.json")
    return render_template("crear_json_ventas.html")
#-------------------------------------------------------------------------------
@app.route("/leer_json_ventas")
def leer_json_ventas():
    json = pd.read_json("ventas2.json")
    return render_template("leer_json_ventas.html", json = json)
#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------




app.run(port=5000)
if __name__ == "__main__":
    app.run(debug=True)
    app.debug(debug=True)