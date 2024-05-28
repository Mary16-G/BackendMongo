import datetime
from bson import ObjectId
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps
from datetime import datetime
from flask import request

prod=Blueprint("products", __name__)
app = create_app()

@prod.route('/api/v1/users')
def list_users():
    return "user example"

@prod.route('/api/v1/Productos/get_all', methods=['GET'])
def listar_prod():
    data = mongo.db.Productos.find({})
    r=[]
    for producto in data:
        if '_id' in producto:
         producto['_id'] = str(producto['_id'])
        r.append(producto)
    return jsonify(r)    

@prod.route('/productos/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
    try:
        resultado = mongo.db.Productos.delete_one({'_id': ObjectId(id)})
        if resultado.deleted_count > 0:
            return jsonify({"mensaje": "Documento eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prod.route('/api/v1/productos/actualizar/<string:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        data = request.get_json()
        if '_id' in data:
            del data['_id']

        required_fields = ['Costo', 'cantidad_existente', 'Uso']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        nuevo_precio = float(data['Costo']) * 1.2

        producto_actualizado = {
            "Costo": int(data['Costo']),
            "Precio": nuevo_precio,
            "cantidad_existente": int(data['cantidad_existente']),
            "Uso": str(data['Uso'])
        }
        resultado = mongo.db.Productos.update_one({'_id': ObjectId(id)}, {"$set": producto_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@prod.route('/api/v1/productos/porID/<string:id>', methods=['GET'])
def obtener_PorId(id):
    query = {'_id': ObjectId(id)}
    project = {"_id": 0, "Nombre": 1, "Precio": 1, 'Categoria': 1}
    try:
        resultado = mongo.db.Productos.find_one(query, project)
        if resultado:
            return dumps(resultado)
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@prod.route('/productos/nuevoprod', methods=['POST'])
def add_producto():
    try:
        data = request.json

        precio = float(data["Costo"]) * 1.2

        fechaAdq_str = data["fechaAdq"]
        # Convertir la cadena de fecha a un objeto date
        fechaAdq = datetime.strptime(fechaAdq_str, "%Y-%m-%d")

        producto = {
            "idProducto": data["idProducto"],
            "Nombre": data["Nombre"],
            "Costo": data["Costo"],
            "Precio": precio,
            "Color": data["Color"],
            "Marca": data["Marca"],
            "Categoria": {
                "idCategoria": data["Categoria"]["IdCategoria"],
                "nombre": data["Categoria"]["Nombre"]
            },
           "Forma": data["Forma"],
            "Tipo": data["Tipo"],
            "Uso": data["Uso"],
            "Porcentaje_agua": data["Porcentaje_agua"],
            "Material": data["Material"],
            "Afeccion": data["Afeccion"],
            "Estilo": data["Estilo"],
            "Medida": data["Medida"],
            "TipodeArmazon": data["TipodeArmazon"],
            "fechaAdqn": fechaAdq,
            "fechaRegistro": datetime.now(),
            "Origen": data["Origen"],
            "Foto": data["Foto"],
            "Descripcion": data["Descripcion"],
            "cantidad_existente": data["cantidad_existente"],
            "Status": data["Status"]
        }

        resultado = mongo.db.Productos.insert_one(producto)

        if resultado.inserted_id:
            return jsonify({"mensaje": "Producto insertado correctamente", "id": str(resultado.inserted_id)})
        else:
            return jsonify({"mensaje": "Error al insertar el producto"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# @prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
# def actualizar_costo(id):

#     nuevo_costo=request.json[ "Costo"]
#     precio=request.json["Precio"]
#     color=request.json["Color"]
#     try:
#         resultado =mongo.db.Productos.update_one({'_id':ObjectId(id)},{'$set': {"Costo":nuevo_costo, "Precio": precio, "Color": color}})
#         if resultado.modified_count > 0:
#              return jsonify({"mensaje": "Documento actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#  # Manejo de la excepción, puedes personalizar el mensaje de error
#         return jsonify({"error": str(e)}), 500
    
# @prod.route('/productos/eliminar/<string:id>',methods=['DELETE'])
# def eliminar(id):
#     try:
#         resultado= mongo.db.productos.delete_one({'_id':ObjectId(id)})
#         if resultado:
#             #si la consulta es exitosa devuelve datos 
#             return jsonify({"mensaje":"doumento eliminado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"})
#     except Exception as e:
#         return jsonify({"error": str(e)}),500


# @prod.route('/productos/porColor/<string:Color>',methods=['GET'])
# def obtener_PorColor(Color):
#     query={'Color':{'$eq':Color}}
#     sort = [("Color",1)]
#     project= {"_id":0,"Nombre":1,"Precio":1, 'Descripcion':1}
#     try:
#         resultado = mongo.db.Productos.find(query, project).sort(sort)
#         if resultado:
#             #si la consulta es exitosa,devuelve los datos en formato JSON
#             return dumps(resultado)
#         else:
#             #"si no se encuentra el documento,devuelve un mensaje adecuado"
#             return dumps({"mensaje": "Documento no encontrado"}),404
#     except Exception as e:
#         #manejo de la excepcion
#         return dumps({"error": str(e)}),500
    
# @prod.route('/productos/porID/<string:_id>',methods=['GET'])
# def obtener_PorID(_id):
#     query={'_id':ObjectId(_id)}
#     project={"_id":0,"Nombre":1,"Precio":1,'Descripcion':1}
#     try:
#         resultado = mongo.db.Productos.find(query, project)
#         if resultado:
#             #si la consulta es exitosa,devuelve los datos en formato JSON
#             return dumps(resultado)
#         else:
#             #"si no se encuentra el documento,devuelve un mensaje adecuado"
#             return dumps({"mensaje": "Documento no encontrado"}),404
#     except Exception as e:
#         #manejo de la excepcion
#         return dumps({"error": str(e)}),500
    
# #inner join
# @prod.route('/productos/prod_prov', methods=['GET'])
# def obtener_prod_prov():
    
#     query = [
#         {
#         '$lookup': {
#             'from': "Proveedores",
#             'localField': "provId",
#             'foreignField': "provId",
#             'as': "proveedor"
#         }
#         },
#         {
#              '$unwind': "$proveedor" #deshacer el array creado por $lookup
#         },
#         {
#             '$project':{
#                 "_id":0,
#                 "Nombre":1,
#                 "Costo":1,
#                 "Color":1,
#                 "proveedor.Nombre":1,
#                 "proveedor.DescuentoPor":1
#             }
#         }
#     ]
    
#     try:
#         resultado = mongo.db.Productos.aggregate(query)
#         if resultado:
#             return list(resultado)
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#         return jsonify({"error":str(e)}),500
      
# def actualizar_precio(id,nuevo_costo):
#     try:
#         resultado = mongo.db.Productos.update_one({'_id':ObjectId(id)},{"$set":{"Precio":nuevo_costo+(nuevo_costo*20/100)}})
#         if resultado:
# # Si la consulta es exitosa, devuelve los datos en formato JSON
#             return jsonify({"mensaje": "precio actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"})
#     except Exception as e:

#         return jsonify({"error": str(e)}), 500

# #inner join
# @prod.route('/Productos/get_all_with_prov_marca', methods=['GET'])
# def listar_prod_with_prov_marca():
#     query = [
#         {
#             '$lookup': {
#                 'from': "Proveedores",
#                 'localField': "provId",
#                 'foreignField': "provId",
#                 'as': "proveedor"
#             }
#         },
#         {
#             '$unwind': {
#                 'path': "$proveedor",
#                 'preserveNullAndEmptyArrays': True # Mantener documentos de Productos aunque no tengan coincidencias en Proveedores
#             }
#         },
#         {
#             '$lookup': {
#                 'from': "Marcas",
#                 'localField': "Marca",
#                 'foreignField': "idMarca",
#                 'as': "marca"
#             }
#         },
#         {
#             '$unwind': {
#                 'path': "$marca",
#                 'preserveNullAndEmptyArrays': True # Mantener documentos de Productos aunque no tengan coincidencias en Marcas
#             }
#         },
#         {
#             '$project':{
#                 "_id": 0,
#                 "idProducto": 1,
#                 "Nombre": 1,
#                 "Costo": 1,
#                 "Precio": 1,
#                 "Color": 1,
#                 "Marca": "$marca.nom_marca",
#                 "Categoria": 1,
#                 "Forma": 1,
#                 "Tipo": 1,
#                 "Uso": 1,
#                 "Porcentaje_agua": 1,
#                 "Material": 1,
#                 "Afeccion": 1,
#                 "Estilo": 1,
#                 "Medida": 1,
#                 "TipodeArmazon": 1,
#                 "fechaAdq": 1,
#                 "fechaRegistro": 1,
#                 "Origen": 1,
#                 "Foto": 1,
#                 "Descripcion": 1,
#                 "cantidad_existente": 1,
#                 "Status": 1,
#                 "Proveedor": "$proveedor.Nombre",
#                 "DescuentoProveedor": "$proveedor.DescuentoPor"
#             }
#         }
#     ]
    
#     try:
#         resultado = list(mongo.db.Productos.aggregate(query))
#         if resultado:
#             # Ordenar los resultados por idProducto
#             resultado_sorted = sorted(resultado, key=lambda x: x.get('_id', ''))
#             return resultado_sorted
#         else:
#             return jsonify({"mensaje": "No se encontraron documentos de Productos"}), 404
#     except Exception as e:
#         return jsonify({"error":str(e)}), 500