from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

client=Blueprint("cliente", __name__)
app = create_app()

@client.route('/api/v1/users')
def list_users():
    return "user example"

@client.route('/api/v1/Cliente/get_all',methods=['GET'])
def listar_cliente():
    data=mongo.db.Cliente.find({})
    r=[]
    for cliente in data:
        if '_id' in cliente:
         cliente['_id'] = str(cliente['_id'])
        r.append(cliente)
    return jsonify(r) 


@client.route('/api/v1/clientes', methods=['POST'])
def agregar_cliente():
    try:
        data = request.json
        cliente = {
            "Nombre": data["Nombre"],
            "Telefono": data["Telefono"],
            "Direccion": data["Direccion"]
        }
        resultado = mongo.db.Cliente.insert_one(cliente)
        if resultado:
            return jsonify({"mensaje": "Cliente insertado correctamente"}), 201
        else:
            return jsonify({"mensaje": "Error al insertar cliente"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client.route('/Cliente/actualizar/<string:id>', methods=['PUT'])
def actualizar_campos(id):
    nuevoNombre = request.json["Nombre"]
    nuevoTelefono = request.json["Telefono"]
    nuevaDireccion = request.json["Direccion"]

    try:
        resultado = mongo.db.Cliente.update_one({'_id': ObjectId(id)}, {'$set': {"Nombre": nuevoNombre, "Telefono": nuevoTelefono, "Direccion": nuevaDireccion}})
        if resultado.modified_count > 0:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client.route('/api/v1/Cliente/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Cliente.delete_one({'_id':ObjectId(id)})
        if resultado.deleted_count > 0:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
