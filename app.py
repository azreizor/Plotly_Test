import json
from flask import Flask, render_template
import pandas as pd
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route("/") # el nombre de la url de solicitud
def index():
    return render_template("index.html")

@app.route("/pandas")
def pandasdf():
    df = pd.read_csv("VENTAS_SEMANALES_AGROSPARE.csv", sep=";")
    #print(df.loc[0]["FECHA"])
    #print("imprimir como dataframe", df)
    #print(df.head(10))
    #print(df.info())
    #print(df.head(10)["FECHA"])
    #print(df.head()["TOTAL_SEMANAL"])
    #print(df["FECHA"])
    #print(total)
    return render_template("pandas.html")


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