from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson import ObjectId
from flask import request

empleado=Blueprint("empleado",__name__)

@empleado.route('/api/v1/users')
def list_users():
    return "user example"

@empleado.route('/api/v1/Empleado/get_all',methods=['GET'])
def listar_empleado():
    data=mongo.db.Empleados.find({})
    r=[]
    for empleado in data:
        if '_id' in empleado:
         empleado['_id'] = str(empleado['_id'])
        r.append(empleado)
    return jsonify(r)  

@empleado.route('/Empleado/nuevo', methods=['POST'])
def add_proveedor():
    try:
        data = request.json
        
        proveedor = {
            "Nombre": data["Nombre"],
            "ApellidoP": data["ApellidoP"],
            "ApellidoM": data["ApellidoM"],
            "Salario": int(data["Salario"]),
            "Cargo": data["Cargo"]
        }
        resultado = mongo.db.Empleados.insert_one(proveedor)
        if resultado:
            return jsonify({"mensaje": "empleado insertado"})
        else:
            return jsonify({"mensaje": "empleado no insertado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@empleado.route('/Empleado/eliminar/<string:id>',methods=['DELETE'])
def eliminar(id):
    try:
        resultado= mongo.db.Empleados.delete_one({'_id':ObjectId(id)})
        if resultado.deleted_count > 0:
            #si la consulta es exitosa devuelve datos 
            return jsonify({"mensaje":"doumento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@empleado.route('/api/v1/Empleado/porID/<string:id>',methods=['GET'])
def obtener_PorID(_id):
    query={'_id':ObjectId(_id)}
    project = {"_id": 0}
    try:
        resultado = mongo.db.Empleados.find(query, project)
        if resultado:
            #si la consulta es exitosa,devuelve los datos en formato JSON
            return dumps(resultado)
        else:
            #"si no se encuentra el documento,devuelve un mensaje adecuado"
            return dumps({"mensaje": "Documento no encontrado"}),404
    except Exception as e:
        #manejo de la excepcion
        return dumps({"error": str(e)}),500

@empleado.route('/api/v1/Empleado/actualizar/<string:id>', methods=['PUT'])
def actualizar_proveedor(id):
    try:
        data = request.get_json()
        if '_id' in data:
            del data['_id']

        required_fields = ['Nombre', 'ApellidoP', 'ApellidoM']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        proveedor_actualizado = {
            "Nombre": data["Nombre"],
            "ApellidoP": data["ApellidoP"],
            "ApellidoM": data["ApellidoM"]
        }
        resultado = mongo.db.Empleados.update_one({'_id': ObjectId(id)}, {"$set": proveedor_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "empleado actualizado"})
        else:
            return jsonify({"mensaje": "empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#@empleado.route('/Empleado/actualizar/<string:id>', methods=['PUT'])
# def actualizar_nombre(id):
#     nuevo_empleado=request.json[ "Nombre"]
#     nuevo_apeP=request.json[ "ApellidoP"]
#     nuevo_apeM=request.json[ "ApellidoM"]

#     try:
#         resultado =mongo.db.Empleados.update_one({'_id':ObjectId(id)},{'$set': {"Nombre":nuevo_empleado, "ApellidoP":nuevo_apeP, "ApellidoM":nuevo_apeM}})
#         if resultado.modified_count > 0:
#              return jsonify({"mensaje": "Documento actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#  # Manejo de la excepción, puedes personalizar el mensaje de error
#         return jsonify({"error": str(e)}), 500