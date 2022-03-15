from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn
from objects.categoria import Categoria

def index_categorias(request):

    try:

        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Select *from categorias"
            cursor.execute(sql)
            categories = cursor.fetchall()
        
        return render_template('/views/categories/index.html', categorias=categories)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/categories/index.html',alert=alerts, categorias=categories)


def crear_categoria(request):

    if request.method == 'POST':
        
        categories = Categoria(
            nombre = request.form["cat_nombre"],
            descripcion = request.form["cat_descripcion"],
        )

        try:
            
            alerts = {"tipo":"","message":""}

            with conn.cursor() as cursor:
                sql = "Insert into categorias(cat_nombre,cat_descripcion) VALUES(%s,%s)"
                cursor.execute(sql,(categories.nombre,categories.descripcion))
            conn.commit()

            alerts["tipo"] = "success"
            alerts["message"] = "Categoría Creada"
                
            return redirect(url_for('categorias'))
            

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/categories/crear.html', alert=alerts, categoria=categories)
        
    else:
        return jsonify({"message":"metodo no correcto"}),500


def modificar_categoria(request):
    
    if request.method == 'POST':

        categories = Categoria(
            nombre = request.form["cat_nombre"],
            descripcion = request.form["cat_descripcion"],
        )

        cat_id = request.args.get("id")

        try:
            
            alerts = {"tipo":"","message":""}

            with conn.cursor() as cursor:
                sql = "Update categorias set cat_nombre = %s, cat_descripcion =%s where cat_id= %s"
                cursor.execute(sql,(categories.nombre,categories.descripcion,cat_id))
            conn.commit()

            alerts["tipo"] = "success"
            alerts["message"] = "Categoria Editada"

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/categories/editar.html',alert=alerts, categoria=categories)
    else:

        try:
            
            categories = {}

            alerts = {"tipo":"","message":""}

            cat_id = request.args.get("id")

            with conn.cursor() as cursor:
                sql = "Select *from categorias where cat_id = %s"
                cursor.execute(sql,(cat_id,))
                categories = cursor.fetchone()
            
            return render_template('/views/categories/editar.html', categoria=categories)    
                                        
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/categories/editar.html',alert=alerts, categoria=categories)



def eliminar_categoria(request):

    cat_id = request.args.get("id")

    try:
            
        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Delete from categorias where cat_id = %s"
            cursor.execute(sql,(cat_id,))
        conn.commit()

        alerts["tipo"] ="success"
        alerts["message"] = "Categoria Eliminada"
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return redirect(url_for('categorias'))