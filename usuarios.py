from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

usuari=Blueprint("usuarios", __name__)
app = create_app()

@usuari.route('/api/v1/users')
def list_users():
    return "user example"

@usuari.route('/api/v1/Usuario/get_all',methods=['GET'])
def listar_usuario():
    data=mongo.db.Usuarios.find({})
    r=[]
    for usuario in data:
        if '_id' in usuario:
         usuario['_id'] = str(usuario['_id'])
        r.append(usuario)
    return jsonify(r) 

@usuari.route('/usuarios/<clave>/<correo>', methods=['GET'])
def obtener_Correo(clave, correo):
    try:
        resultado = mongo.db.Usuarios.find_one({"correo": correo, "clave": clave}, {"_id": 0, "clave": 1, "correo": 1})
        if resultado:
            return jsonify({"mensaje": "True"})
        else:
            return jsonify({"mensaje": "false"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuari.route('/api/v1/usuarios/nuevo', methods=['POST'])
def agregar_usuario():
    try:
        data = request.json
        
        usuario = {
            "Nombre": data["Nombre"],
            "ApellidoP": data["ApellidoP"],
            "Password": data["Password"],
            "Rol": data["Rol"],
            "email": data["email"],
            "foto": data["foto"]
        }
        resultado = mongo.db.Usuarios.insert_one(usuario)
        if resultado:
            return jsonify({"mensaje": "Usuario insertado"})
        else:
            return jsonify({"mensaje": "Usuario no insertado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuari.route('/api/v1/usuarios/porID/<string:id>', methods=['GET'])
def obtener_usuario_por_id(id):
    query = {'_id': ObjectId(id)}
    project = {"_id": 1, "Password": 1, "Nombre": 1, "email": 1, "Rol": 1}
    try:
        resultado = mongo.db.Usuarios.find_one(query, project)
        if resultado:
            return dumps(resultado)
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuari.route('/api/v1/usuarios/actualizar/<string:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        data = request.get_json()

        usuario_actualizado = {
            "Password": data["Password"],
            "Nombre": data["Nombre"],
            "email": data["email"],
            "Rol": data["Rol"]
        }
        
        resultado = mongo.db.Usuarios.update_one({'_id': ObjectId(id)}, {"$set": usuario_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Usuario actualizado"})
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@usuari.route('/Usuario/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Usuarios.delete_one({'_id':ObjectId(id)})
        if resultado.deleted_count > 0:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    