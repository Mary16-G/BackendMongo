from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request


prove=Blueprint("provee",__name__)

@prove.route('/api/v1/users')
def list_users():
    return "user example"

@prove.route('/api/v1/provedores/get_all',methods=['GET'])
def listar_prove():
    data=mongo.db.Proveedores.find({})
    r=[]
    for producto in data:
        if '_id' in producto:
         producto['_id'] = str(producto['_id'])
        r.append(producto)
    return jsonify(r)    


@prove.route('/proveedores/nuevo', methods=['POST'])
def add_proveedor():
    try:
        data = request.json
        
        proveedor = {
            "Nombre": data["Nombre"],
            "DescuentoPor": data["DescuentoPor"],
            "correo": data["correo"]
        }

        resultado = mongo.db.Proveedores.insert_one(proveedor)
        if resultado:
            return jsonify({"mensaje": "Proveedor insertado"})
        else:
            return jsonify({"mensaje": "Proveedor no insertado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@prove.route('/provedores/pornombre/<string:nombre>',methods=['GET'])
def obtener_PorNombre(nombre):
    query={'Nombre':nombre}
    project={"_id":0,"Nombre":1,"DescuentoPor":1}
    try:
        resultado = mongo.db.Proveedores.find(query, project)
        if resultado:
            return dumps(resultado)
        else:
            return dumps({"mensaje": "Proveedor no encontrado"}),404
    except Exception as e:
        return dumps({"error": str(e)}),500

@prove.route('/api/v1/proveedores/porID/<string:id>',methods=['GET'])
def obtener_PorID(_id):
    query={'_id':ObjectId(_id)}
    project = {"_id": 0}
    try:
        resultado = mongo.db.Proveedores.find(query, project)
        if resultado:
            #si la consulta es exitosa,devuelve los datos en formato JSON
            return dumps(resultado)
        else:
            #"si no se encuentra el documento,devuelve un mensaje adecuado"
            return dumps({"mensaje": "Documento no encontrado"}),404
    except Exception as e:
        #manejo de la excepcion
        return dumps({"error": str(e)}),500

@prove.route('/api/v1/proveedores/actualizar/<string:id>', methods=['PUT'])
def actualizar_proveedor(id):
    try:
        data = request.get_json()
        if '_id' in data:
            del data['_id']

        required_fields = ['Nombre', 'DescuentoPor', 'correo']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        proveedor_actualizado = {
            "Nombre": data["Nombre"],
            "DescuentoPor": data["DescuentoPor"],
            "correo": data["correo"]
        }
        resultado = mongo.db.Proveedores.update_one({'_id': ObjectId(id)}, {"$set": proveedor_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Proveedor actualizado"})
        else:
            return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@prove.route('/provedores/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Proveedores.delete_one({'_id':ObjectId(id)})
        if resultado.deleted_count > 0:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"documento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
# @prove.route('/provedores/insertar', methods=['POST'])
# def insertar_provedor():
#     provId=request.json["provId"]
#     Nombre=request.json[ "Nombre"]
#     DescuentoPor=request.json[ "DescuentoPor"]
#     correo=request.json[ "correo"]
#     try:
#         # Inserta el nuevo usuario en la base de datos
#         resultado = mongo.db.Proveedores.insert_one({
#             "provId": provId,
#             "Nombre": Nombre,
#             "DescuentoPor": DescuentoPor,
#             "correo": correo
#         })
#         # Verifica si la inserción fue exitosa
#         if resultado.inserted_id:
#             return jsonify({"mensaje": "proveedor insertado correctamente", "id": str(resultado.inserted_id)})
#         else:
#             return jsonify({"mensaje": "Error al insertar el usuario"}), 500
#     except Exception as e:
#         # Manejo de la excepción
#         return jsonify({"error": str(e)}), 500

# @prove.route('/api/v1/proveedores/actualizar/<string:id>', methods=['PUT'])
# def actualizar_nombre(id):

#     nuevo_Nombre=request.json[ "Nombre"]
#     nuevo_Des=request.json[ "DescuentoPor"]
#     nuevo_correo=request.json[ "correo"]
#     try:
#         resultado = mongo.db.Proveedores.update_one({'_id': ObjectId(id)}, {'$set': {"Nombre": nuevo_Nombre, "DescuentoPor": nuevo_Des, "correo": nuevo_correo}})
#         if resultado.modified_count > 0:
#              return jsonify({"mensaje": "Documento actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#  # Manejo de la excepción, puedes personalizar el mensaje de error
#         return jsonify({"error": str(e)}), 500
