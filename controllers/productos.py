from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn
from objects.producto import Producto
import os

def index_productos(request):

    try:
        
        alerts = {"tipo":"","message":""}

        products = []

        with conn.cursor() as cursor:
            sql = "Select *from productos,categorias where prod_categoria = cat_id "
            cursor.execute(sql)
            products = cursor.fetchall()
        
        return render_template('/views/products/index.html', productos=products)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/products/index.html',alert=alerts, productos=products)


def registrar_producto(request):

    try:
        
        categories = []

        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Select *from categorias"
            cursor.execute(sql)
            categories = cursor.fetchall()
        
        return render_template('/views/products/crear.html', producto= {}, categorias=categories)

    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/products/crear.html',alert=alerts, producto={}, categorias=categories)


def crear_producto(request):

    if request.method == 'POST':
        
        products = Producto(
            nombre = request.form["prod_nombre"],
            descripcion = request.form["prod_descripcion"],
            precio = request.form["prod_precio"],
            categoria = request.form["prod_categoria"],
            stock= request.form["prod_stock"],
            imagen = request.files['file']
        )

        try:
            
            alerts = {"tipo":"","message":""}


            if products.imagen != None and products.imagen.filename != '':
                path = os.path.join('static/products/',products.imagen.filename)
                products.imagen.save(path)
                products.imagen = products.imagen.filename
            
            else:
                products.imagen = "default.png"

            with conn.cursor() as cursor:
                sql = "Insert into productos(prod_nombre,prod_descripcion,prod_precio,prod_categoria,prod_stock,prod_imagen) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(products.nombre,products.descripcion,products.precio,products.categoria,products.stock,products.imagen))
            conn.commit()

            alerts["tipo"] = "success"
            alerts["message"] = "Producto Creado"
                
            return redirect(url_for('productos'))

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/products/crear.html', alert=alerts, productos=products)
        
    else:
        return jsonify({"message":"metodo no correcto"}),500


def modificar_productos(request):
    
    if request.method == 'POST':

        products = Producto(
            nombre = request.form["prod_nombre"],
            descripcion = request.form["prod_descripcion"],
            precio = request.form["prod_precio"],
            categoria = request.form["prod_categoria"],
            stock= request.form["prod_stock"],
            imagen = request.files['file']
        )

        prod_id = request.args.get("id")

        categories = []

        try:

            alerts = {"tipo":"","message":""}

            with conn.cursor() as cursor:
                
                sql = "Select *from categorias"
                cursor.execute(sql)
                categories = cursor.fetchall()

                sql = "Select *from productos where prod_id = %s"
                cursor.execute(sql,(prod_id,))
                product = cursor.fetchone()

                if products.imagen != None and products.imagen.filename != '':

                    if product[8] != 'default.png':
                        path = os.path.join('static/products/',product[8])
                        os.remove(path)

                    path = os.path.join('static/products/',products.imagen.filename)
                    products.imagen.save(path)
                    products.imagen = products.imagen.filename

                    sql = "Update productos set prod_nombre = %s, prod_descripcion =%s, prod_precio = %s, prod_categoria = %s, prod_stock = %s, prod_imagen=%s where prod_id= %s"
                    cursor.execute(sql,(products.nombre,products.descripcion,products.precio,products.categoria,products.stock,products.imagen,prod_id))

                else:
                    products.imagen = product[8]
                    sql = "Update productos set prod_nombre = %s, prod_descripcion =%s, prod_precio = %s, prod_categoria = %s, prod_stock = %s where prod_id= %s"
                    cursor.execute(sql,(products.nombre,products.descripcion,products.precio,products.categoria,products.stock,prod_id))

            conn.commit()

            alerts["tipo"] = "success"
            alerts["message"] = "Producto Editado"

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/products/editar.html',alert=alerts, producto=products, categorias=categories )

    else:

        try:
            
            products = {}
            categories = []
            alerts = {"tipo":"","message":""}

            prod_id = request.args.get("id")

            with conn.cursor() as cursor:
                sql = "Select *from productos where prod_id = %s"
                cursor.execute(sql,(prod_id,))
                products = cursor.fetchone()
    
                sql = "Select *from categorias"
                cursor.execute(sql)
                categories = cursor.fetchall()
            
            return render_template('/views/products/editar.html', producto=products, categorias=categories)    
                                        
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/products/editar.html',alert=alerts, producto=products, categorias=categories)


def eliminar_productos(request):

    prod_id = request.args.get("id")

    try:
            
        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Delete from productos where prod_id = %s"
            cursor.execute(sql,(prod_id,))
        conn.commit()

        alerts["tipo"] ="success"
        alerts["message"] = "Producto Eliminado"
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return redirect(url_for('productos'))