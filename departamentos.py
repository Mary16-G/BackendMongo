from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

depa=Blueprint("departamentos", __name__)
app = create_app()

@depa.route('/Departamentos/get_all',methods=['GET'])
def listar_empleado():
    data=mongo.db.Departamentos.find({})
    r=dumps(data)
    return r 

@depa.route('/Departamentos/insertar', methods=['POST'])
def insertar_cliente():
    Nombre = request.json["Nombre"]
    Cargo = request.json["CargoSuperior"]
    Plazas = request.json["Plazas"]
    try:
        # Inserta el nuevo usuario en la base de datos
        resultado = mongo.db.Departamentos.insert_one({
            "Nombre": Nombre,
            "CargoSuperior": Cargo,
            "Plazas": Plazas
        })
        # Verifica si la inserción fue exitosa
        if resultado.inserted_id:
            return jsonify({"mensaje": "Usuario insertado correctamente", "id": str(resultado.inserted_id)})
        else:
            return jsonify({"mensaje": "Error al insertar el usuario"}), 500
    except Exception as e:
        # Manejo de la excepción
        return jsonify({"error": str(e)}), 500
    
@depa.route('/Departamentos/actualizar/<string:id>', methods=['PUT'])
def actualizar_campos(id):
    nuevoNombre = request.json["Nombre"]
    nuevoCargo = request.json["CargoSuperior"]
    nuevoPlazas = request.json["Plazas"]

    try:
        resultado = mongo.db.Departamentos.update_one({'_id': ObjectId(id)}, {'$set': {"Nombre": nuevoNombre, "CargoSuperior": nuevoCargo, "Plazas": nuevoPlazas}})
        if resultado.modified_count > 0:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@depa.route('/Departamentos/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Departamentos.delete_one({'_id':ObjectId(id)})
        if resultado:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500