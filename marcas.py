from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

marca=Blueprint("marcas",__name__)

@marca.route('/api/v1/users')
def list_users():
    return "user example"

@marca.route('/api/v1/marcas/get_all',methods=['GET'])
def listar_marca():
    data=mongo.db.Marcas.find({})
    r=[]
    for marcas in data:
        if '_id' in marcas:
         marcas['_id'] = str(marcas['_id'])
        r.append(marcas)
    return jsonify(r)  

@marca.route('/marcas/nuevo', methods=['POST'])
def add_proveedor():
    try:
        data = request.json
        
        proveedor = {
            "nom_marca": data["nom_marca"],
            "logo": data["logo"],
            "cantidad": int(data["cantidad"])
        }
        resultado = mongo.db.Marcas.insert_one(proveedor)
        if resultado:
            return jsonify({"mensaje": "Proveedor insertado"})
        else:
            return jsonify({"mensaje": "Proveedor no insertado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@marca.route('/api/v1/marca/porID/<string:_id>', methods=['GET'])
def obtener_PorID(_id):
    query = {'_id': ObjectId(_id)}
    project = {"_id": 0}
    try:
        resultado = mongo.db.Marcas.find_one(query, project)
        if resultado:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return dumps(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return dumps({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        # Manejo de la excepción
        return dumps({"error": str(e)}), 500

@marca.route('/api/v1/marca/actualizar/<string:id>', methods=['PUT'])
def actualizar_proveedor(id):
    try:
        data = request.get_json()
        if '_id' in data:
            del data['_id']

        required_fields = ['nom_marca', 'logo', 'cantidad']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        marca_actualizado = {
            "nom_marca": data["nom_marca"],
            "logo": data["logo"],
            "cantidad": int(data['cantidad'])
        }
        resultado = mongo.db.Marcas.update_one({'_id': ObjectId(id)}, {"$set": marca_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Proveedor actualizado"})
        else:
            return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# @marca.route('/marca/actualizar/<string:id>', methods=['PUT'])
# def actualizar(id):
#     nuevo_marca=request.json[ "nom_marca"]
#     nuevo_logo=request.json[ "logo"]
#     nuevo_cantidad=request.json[ "cantidad"]
#     try:
#         resultado =mongo.db.Marcas.update_one({'_id':ObjectId(id)},{'$set': {"nom_marca":nuevo_marca, "logo":nuevo_logo, "cantidad":nuevo_cantidad}})
#         if resultado.modified_count > 0:
#              return jsonify({"mensaje": "Documento actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#  # Manejo de la excepción, puedes personalizar el mensaje de error
#         return jsonify({"error": str(e)}), 500
    
@marca.route('/marca/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Marcas.delete_one({'_id':ObjectId(id)})
        if resultado.deleted_count > 0:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    

# @marca.route('/marcas/insertar', methods=['POST'])
# def insertar_marca():
#     idMarca=request.json["idMarca"]
#     nom_marca=request.json[ "nom_marca"]
#     logo=request.json[ "logo"]
#     cantidad=request.json[ "cantidad"]
#     try:
#         # Inserta el nuevo usuario en la base de datos
#         resultado = mongo.db.Marcas.insert_one({
#             "idMarca": idMarca,
#             "nom_marca": nom_marca,
#             "logo": logo,
#             "cantidad": cantidad
#         })
#         # Verifica si la inserción fue exitosa
#         if resultado.inserted_id:
#             return jsonify({"mensaje": "marca insertada correctamente", "id": str(resultado.inserted_id)})
#         else:
#             return jsonify({"mensaje": "Error al insertar el usuario"}), 500
#     except Exception as e:
#         # Manejo de la excepción
        #return jsonify({"error": str(e)}), 500