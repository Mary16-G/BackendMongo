from app import create_app
from productos import prod
from proveedores import prove
from marcas import marca
from usuarios import usuari
from Empleados import empleado
from clientes import client
from departamentos import depa
from carrito import carrito
from flask_cors import CORS

app = create_app()
app.register_blueprint(prod)
app.register_blueprint(prove)
app.register_blueprint(marca)
app.register_blueprint(usuari)
app.register_blueprint(empleado)
app.register_blueprint(client)
app.register_blueprint(depa)
app.register_blueprint(carrito)


cors = CORS(app, resources={r"/api/*": {"origins": "*"}, 
                            r"/productos/nuevoprod": {"origins": "*"}, 
                            r"/productos/eliminar/*": {"origins": "*"},
                            r"/provedores/eliminar/*": {"origins": "*"},
                            r"/proveedores/nuevo*":{"origins":"*"},
                            r"/marca/eliminar/*": {"origins": "*"},
                            r"/Empleado/eliminar/*": {"origins": "*"},
                            r"/Usuario/eliminar/*": {"origins": "*"},
                            r"/marcas/nuevo/*":{"origins":"*"},
                            r"/Empleado/nuevo/*": {"origins": "*"}}, supports_credentials=True)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=4000, debug=True)
    
