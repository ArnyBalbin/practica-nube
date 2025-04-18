from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'dpg-d01bpp6uk2gs73ditvmg-a.virginia-postgres.render.com'
DB_NAME = 'practica_lc4v'
DB_USER = 'arnybalbin'
DB_PASSWORD = 'nqZO8vmr1ZbHTVPWXvyyPvUqvbHN1GNe'


def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)


def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                   (dni, nombre, apellido, direccion, telefono))
    conn.commit()
    conn.close()

def obtener_registros():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM personas order by apellido")
    registros = cursor.fetchall()
    conn.close()
    return registros

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    mensaje_confirmacion = "Registro Exitoso"
    return redirect(url_for('index', mensaje_confirmacion=mensaje_confirmacion))

@app.route('/administrar')
def administrar():
    registros=obtener_registros()
    return render_template('administrar.html',registros=registros)

@app.route('/eliminar', methods=['POST'])
def eliminar_registros():
    ids = request.form.getlist('seleccion')
    conn = conectar_db()
    cursor = conn.cursor()
    for id in ids:
        cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('administrar'))

if __name__ == '__main__':
    #Esto es nuevo
    port = int(os.environ.get('PORT',5000))    
    app.run(host='0.0.0.0', port=port, debug=True)
