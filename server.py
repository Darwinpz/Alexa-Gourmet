from flask import Flask, request, render_template,session,redirect,url_for
from controllers.usuarios import *
from controllers.categorias import *
from controllers.platos import *
from controllers.productos import *
from controllers.principal import *
from controllers.carrito import *
from controllers.facturas import *

app = Flask(__name__,static_folder='./static')
app.secret_key = 'ProyectoProg'

#-----VISTAS SIMPLES-------------------
@app.route('/')
def index():
   return index_principal(request)

@app.route('/ingresar')
def ingresar():
   
   if validar_session():
      return redirect(url_for('index'))
   else:
      return render_template('/views/login.html')

@app.route('/platos/')
def platos():
   return index_platos(request)

@app.route('/platos/detalle/')
def det_platos():
   return detalle_platos(request)


#-------------------------------

@app.route('/salir')
def users_logout():

   if validar_session():
      session.pop('id',None)
      session.pop('nombre',None)
      session.pop('correo',None)
      session.pop('tipo',None)
      return redirect(url_for('index'))
   else:
      return redirect(url_for('err_403'))


#------USUARIOS-------------------

@app.route('/usuarios')
def users():

   if validar_userAdmin():
      return index_usuario(request)
   else: 
      return redirect(url_for('err_401'))

@app.route('/usuarios/registrar')
def users_registrar():
   return render_template('/views/users/crear.html', usuario={})

@app.route('/usuarios/editar/', methods=['GET','POST'])
def users_modificar():
   return modificar_usuario(request)

@app.route('/usuarios/eliminar/')
def users_eliminar():
   return eliminar_usuario(request)

@app.route('/crearusuario',  methods=['POST'])
def users_crear():
   return crear_usuario(request)

@app.route('/login',  methods=['POST'])
def users_login():
   return ingresar_usuario(request)


#-----------------------------------


#-------CATEGORIAS---------------
@app.route('/categorias')
def categorias():

   if validar_userAdmin():
      return index_categorias(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/categorias/registrar')
def categorias_registrar():

   if validar_userAdmin():
      return render_template('/views/categories/crear.html', categoria={})
   else:
      return redirect(url_for('err_401'))

@app.route('/categorias/editar/' ,methods=['GET','POST'])
def categorias_modificar():

   if validar_userAdmin():
      return modificar_categoria(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/categorias/eliminar/')
def categorias_eliminar():

   if validar_userAdmin():
      return eliminar_categoria(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/crearcategoria',  methods=['POST'])
def categorias_crear():

   if validar_userAdmin():
      return crear_categoria(request)
   else:
      return redirect(url_for('err_401'))
#---------------------------

#--------PRODUCTOS-------------------
@app.route('/productos')
def productos():

   if validar_userAdmin() : 
      return index_productos(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/productos/registrar')
def productos_registrar():

   if validar_userAdmin() : 
      return registrar_producto(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/productos/editar/' ,methods=['GET','POST'])
def productos_modificar():

   if validar_userAdmin():
      return modificar_productos(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/productos/eliminar/')
def productos_eliminar():

   if validar_userAdmin():
      return eliminar_productos(request)
   else:
      return redirect(url_for('err_401'))

@app.route('/crearproducto',  methods=['POST'])
def productos_crear():

   if validar_userAdmin():
      return crear_producto(request)
   else:
      return redirect(url_for('err_401'))
#--------------------------------


#--------CARRITO-------------  
@app.route('/carrito')
def carrito():
   
   if validar_session():
      return index_carrito(request)
   else:
      return redirect(url_for('err_403'))

@app.route('/addcarrito', methods=['POST'])
def agregar_carrito():
   
   if validar_session():
      return add_carrito(request)
   else:
      return redirect(url_for('err_403'))

@app.route('/carrito/eliminar/')
def carrito_eliminar():

   if validar_session():
      return eliminar_carrito(request)
   else:
      return redirect(url_for('err_403'))


#----------------------------------

#----------FACTURAS--------------
@app.route('/facturas')
def facturas():
   if validar_session():
      return index_facturas(request)
   else:
      return redirect(url_for('err_403'))

@app.route('/addfacturas', methods=['POST'])
def agregar_facturas():
   if validar_session():
      return add_factura(request)
   else:
      return redirect(url_for('err_403'))

#-----ERRORES---------------

@app.route('/500')
def err_500 ():
   return render_template('/views/errors/500.html')

@app.route('/401')
def err_401 ():
   return render_template('/views/errors/401.html')

@app.route('/404')
def err_404 ():
   return render_template('/views/errors/404.html')

@app.route('/403')
def err_403 ():
   return render_template('/views/errors/403.html')

#-----------------------------



def validar_userAdmin():
   if 'tipo' in session and session["tipo"] == "ADMINISTRADOR" :
      return True

def validar_session():
   if 'correo' in session:
      return True

if __name__ == '__main__':
    app.run(port=5000, debug=True)