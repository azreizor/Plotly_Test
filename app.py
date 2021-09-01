from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route("/") # el nombre de la url de solicitud
def index():
    return render_template("index.html")

#@app.route("/crear_json_ventas")
#def crear_json_ventas():
#    col_names = ['fecha','valor']
#    df = pandas.read_csv("VENTAS_SEMANALES_AGROSPARE.csv", sep=";")
#    df.to_json("ventas2.json")
#    return render_template("crear_json_ventas.html")


@app.route("/leer_json_ventas")
def leer_json_ventas():
    json = pd.read_json("ventas.json")
    return render_template("leer_json_ventas.html", json = json)

#@app.route("/plotly")
#def plotly():
#    json = pandas.read_json("ventas.json")
#    df = pandas.DataFrame(json)
#    fig = plotly_express.bar(df, x = "FECHA", y = "TOTAL_SEMANAL", barmode= "group")
#    graphJSON = json.dumps(fig)
#    return render_template("plotly.html", graphJSON = graphJSON)

@app.route('/plotlyoriginal')
def chart1():
    df = pd.DataFrame({
        "Frutas": ["Manzana", "Naranja", "Platano", "Manzana", "Naranja", "Platano"],
        "Cantidad": [4, 1, 2, 2, 4, 5],
        "Ciudad": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Frutas", y="Cantidad", color="Ciudad", barmode="group")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Fruit in North America"
    description = """
    A academic study of the number of apples, oranges and bananas in the cities of
    San Francisco and Montreal would probably not come up with this chart.
    """
    return render_template('plotly.html', graphJSON=graphJSON, header=header,description=description)





#@app.route("/importar") # el nombre de la url de solicitud
#def importar_datos():
#    dir = os.getcwd()
#    f= open("VENTAS_SEMANALES_AGROSPARE2.csv")
#    datos = csv.reader(f)
#    return render_template("importar_datos.html", dir = dir, datos = datos)
#
##---------------------------------------------------------------------------------------------------------
#@app.route("/plantilla") # el nombre de la url de solicitud
#def plantilla():
#    return render_template("plantilla.html")
#
#@app.route("/tabla") # el nombre de la url de solicitud
#def tabla():
#    return render_template("hijo1.html")
#
#@app.route("/muestra_paises")
#def muestra_paises():
#    #paises = paises_datos()
#    #return render_template("paises.html", paises = paises)
#    paises_datos()
#    return render_template("paises.html")




app.run(port=5000)
if __name__ == "__main__":
    app.run(debug=True)
    app.debug(debug=True)