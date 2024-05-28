from app import create_app
from mongo import mongo
from flask_cors import CORS
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

carrito=Blueprint("Carrito", __name__)
app = create_app()
CORS(app)

@carrito.route('/Carrito/get_all',methods=['GET'])
def listar_empleado():
    data=mongo.db.Carrito.find({})
    r=dumps(data)
    return r 

#inner join
@carrito.route('/Carrito/cliente', methods=['GET'])
def obtener_client_carrito():
    
    query = [
        {
        '$lookup': {
            'from': "Cliente",
            'localField': "Cliente_id",
            'foreignField': "id",
            'as': "client"
        }
        },
        {
             '$unwind': "$client" #deshacer el array creado por $lookup
        },
        {
            '$project':{
                "_id":0,
                "ListaProductos":1,
                "Costo":1,
                "FechaCompra":1,
                "client.Nombre": 1  # Cambia a "client" en lugar de "client.Nombre"
            }
        }
    ]
    
    try:
        resultado = mongo.db.Carrito.aggregate(query)
        if resultado:
            return list(resultado)
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}),500

@carrito.route('/Carrito/insertar', methods=['POST'])
def insertar_cliente():
    ListaProductos = request.json["ListaProductos"]
    Cliente_id = request.json["Cliente_id"]
    FechaCompra = request.json["FechaCompra"]
    try:
        # Inserta el nuevo usuario en la base de datos
        resultado = mongo.db.Carrito.insert_one({
            "ListaProductos": ListaProductos,
            "Cliente_id": Cliente_id,
            "FechaCompra": FechaCompra
        })
        # Verifica si la inserción fue exitosa
        if resultado.inserted_id:
            return jsonify({"mensaje": "Usuario insertado correctamente", "id": str(resultado.inserted_id)})
        else:
            return jsonify({"mensaje": "Error al insertar el usuario"}), 500
    except Exception as e:
        # Manejo de la excepción
        return jsonify({"error": str(e)}), 500
    
@carrito.route('/Carrito/actualizar/<string:id>', methods=['PUT'])
def actualizar_campos(id):
    nuevosProduc = request.json["ListaProductos"]
    nuevoCliente = request.json["Cliente_id"]
    nuevaFecha = request.json["FechaCompra"]

    try:
        resultado = mongo.db.Carrito.update_one({'_id': ObjectId(id)}, {'$set': {"ListaProductos": nuevosProduc, "Cliente_id": nuevoCliente, "FechaCompra": nuevaFecha}})
        if resultado.modified_count > 0:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carrito.route('/Carrito/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Carrito.delete_one({'_id':ObjectId(id)})
        if resultado:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500