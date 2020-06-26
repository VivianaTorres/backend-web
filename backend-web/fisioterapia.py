from flask import Flask, request, jsonify  
from bson.json_util import dumps
from bson.objectid import ObjectId
import db
from pymongo import TEXT

app = Flask(__name__)

# ------------------ INSERCIÓN ------------------
@app.route("/paciente", methods=['POST'])
def create():
    data = request.get_json()
    con = db.get_connection() 
    Rehabilitacion = con.Rehabilitacion 
    try:
        pacientes = Rehabilitacion.pacientes # pacientes es una coleccion de la base de datos
        pacientes.insert(data)
        return jsonify({"mensaje":"OK"})
    finally:
        con.close()
        print("Conexion cerrada")

# ------------------ BORRADO ------------------
@app.route("/paciente/<codigo>", methods=['DELETE'])
def delete(codigo):
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    try:
        pacientes = Rehabilitacion.pacientes
        pacientes.delete_one({'_id': ObjectId(codigo)}) 
        return jsonify({"mensaje":"OK"})
    finally:
        con.close()
        print("Conexion cerrada")

# ------------------ CONSULTA ------------------
 
# Consulta de toda la informacion 
@app.route("/paciente", methods=['GET'])
def get_pacientes():
    con = db.get_connection() 
    Rehabilitacion = con.Rehabilitacion 
    try:
        pacientes = Rehabilitacion.pacientes 
        retorno = dumps(pacientes.find()) 
        return jsonify(retorno)
    finally:
        con.close()
        print("Conexion cerrada")

# Consulta especifica por codigo del paciente
@app.route("/paciente/<codigo>", methods=['GET']) 
def get_paciente(codigo):
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    try:
        pacientes = Rehabilitacion.pacientes
        retorno = dumps(pacientes.find_one({'_id': ObjectId(codigo)}))
        return jsonify(retorno)
    finally:
        con.close()
        print("Conexion cerrada")

# Endpoint--Consulta por nombre del paciente en la ruta  
@app.route("/paciente/nombre/<codigo>", methods=['GET']) 
def get_nombreRuta(codigo):
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    try:
        pacientes = Rehabilitacion.pacientes
        retorno = dumps(pacientes.find({'nombre':codigo}))
        return jsonify(retorno)
    finally:
        con.close()
        print("Conexion cerrada")

# Endpoint--Consulta por nombre del paciente enviado por el body 
@app.route("/paciente/consultanombre", methods=['GET']) 
def get_parametro():
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    nombre = request.form['nombre']
    
    try:
        pacientes = Rehabilitacion.pacientes
        retorno = dumps(pacientes.find_one({"nombre":nombre}))
        return jsonify(retorno)
    finally:
        con.close()
        print("Conexion cerrada")

# Endpoint--Consulta para ver pacientes con determinada artroplastia 
@app.route("/paciente/categoria", methods=['GET']) 
def get_categoria():
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    tratamiento = request.form['tratamiento']
    try:
        pacientes = Rehabilitacion.pacientes
        #pacientes.create_index([('tratamiento', 'text')])
        pacientes.create_index([('tratamiento', TEXT)])
        print(tratamiento)
        #retorno = dumps(pacientes.find({"tratamiento":tratamiento}))
        retorno = dumps(pacientes.find({'$text': {'$search': tratamiento}}))
        #retorno = dumps(pacientes.find({"tratamiento":{"$exists":tratamiento}}))
        return jsonify(retorno)
    finally:
        con.close()
        print("Conexion cerrada")


# ------------------ ACTUALIZACION ------------------
@app.route("/paciente/<codigo>", methods=['PUT'])
def update(codigo):
    data = request.get_json()
    con = db.get_connection()
    Rehabilitacion = con.Rehabilitacion
    try:
        pacientes = Rehabilitacion.pacientes
        pacientes.update(
            {'_id': ObjectId(codigo)},
            data
        ) 
        return jsonify({"mensaje":"OK"})
    finally:
        con.close()
        print("Conexion cerrada")

