from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn
from objects.user import User

def index_usuario(request):

    try:
        
        users = []

        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Select *from usuarios"
            cursor.execute(sql)
            users = cursor.fetchall()
        
        return render_template('/views/users/index.html', usuarios=users)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/users/index.html',alert=alerts, usuarios=users)

def crear_usuario(request):
    
    if request.method == 'POST':

        user = User(
            cedula= str(request.form["user_cedula"]),
            nombre=request.form["user_nombre"],
            correo=request.form["user_correo"],
            clave=request.form["user_clave"],
            conf_clave = request.form["user_conf_clave"],
            direccion=request.form["user_direccion"],
            telefono= str(request.form["user_telefono"]),
            tipo=request.form["user_tipo"],
            ciudad=request.form["user_ciudad"],
        )

        try:
            
            alerts = {"tipo":"","message":""}

            if user.validar_clave():

                with conn.cursor() as cursor:
                    sql = "Insert into usuarios(user_cedula, user_nombre, user_correo, user_clave, user_direccion, user_telefono, user_tipo, user_ciudad) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(user.cedula,user.nombre,user.correo,user.clave,user.direccion,user.telefono,user.tipo,user.ciudad))
                conn.commit()

                alerts["tipo"] = "success"
                alerts["message"] = "Usuario Creado"
                
                if 'tipo' in session and session["tipo"] == "ADMINISTRADOR" : 
                    
                    return redirect(url_for('users'))

                else:

                    return render_template('/views/login.html', alert=alerts)
            
            else:
                alerts["tipo"] = "warning"
                alerts["message"] = "Las Claves no coinciden"

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/users/crear.html', alert=alerts, usuario=user)
        
    else:
        return jsonify({"message":"metodo no correcto"}),500


def modificar_usuario(request):
    
    if request.method == 'POST':

        user = User(
            cedula= str(request.form["user_cedula"]),
            nombre=request.form["user_nombre"],
            correo=request.form["user_correo"],
            clave=request.form["user_clave"],
            conf_clave = request.form["user_conf_clave"],
            direccion=request.form["user_direccion"],
            telefono= str(request.form["user_telefono"]),
            tipo=request.form["user_tipo"],
            ciudad=request.form["user_ciudad"],
        )

        user_id = request.args.get("id")

        try:
            
            alerts = {"tipo":"","message":""}

            if user.validar_clave():

                with conn.cursor() as cursor:
                    sql = "Update  usuarios set user_cedula = %s, user_nombre = %s, user_correo = %s, user_clave= %s, user_direccion =%s, user_telefono=%s, user_tipo=%s, user_ciudad=%s where user_id= %s"
                    cursor.execute(sql,(user.cedula,user.nombre,user.correo,user.clave,user.direccion,user.telefono,user.tipo,user.ciudad,user_id))
                conn.commit()

                alerts["tipo"] = "success"
                alerts["message"] = "Usuario Editado"

            else:
                alerts["tipo"] = "warning"
                alerts["message"] = "Las Claves no coinciden"

        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/users/editar.html',alert=alerts, usuario=user)

    else:

        try:
            
            user = {}

            alerts = {"tipo":"","message":""}

            user_id = request.args.get("id")

            with conn.cursor() as cursor:
                sql = "Select *from usuarios where user_id = %s"
                cursor.execute(sql,(user_id,))
                user = cursor.fetchone()
            
            return render_template('/views/users/editar.html', usuario=user)    
                                        
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/users/editar.html',alert=alerts, usuario=user)



def ingresar_usuario(request):
    if request.method == 'POST':

        try:
            
            alerts = {"tipo":"","message":""}

            with conn.cursor() as cursor:
                sql = "Select *from usuarios where user_correo = %s and user_clave = %s"
                cursor.execute(sql,(request.form["user_correo"],request.form["user_clave"]))
                usuario = cursor.fetchone()

                if usuario:
                    session["id"] = usuario[0]
                    session["nombre"] = usuario[2]
                    session["correo"] = usuario[3]
                    session["tipo"] = usuario[7]

                    alerts["tipo"] ="success"
                    alerts["message"] = "Bienvenido: "+usuario[2]

                    return render_template('/views/index.html', alert=alerts)

                else:
                    alerts["tipo"] ="warning"
                    alerts["message"] = "Correo o Clave incorrecto"
                                    
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)

        return render_template('/views/login.html', alert=alerts)

    else:
        return jsonify({"message":"metodo no correcto"}),500

def eliminar_usuario(request):

    user_id = request.args.get("id")

    try:
            
        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Delete from usuarios where user_id = %s"
            cursor.execute(sql,(user_id,))
        conn.commit()

        alerts["tipo"] ="success"
        alerts["message"] = "Usuario Eliminado"

        if session['id'] == user_id:
            return redirect(url_for("users_logout"))
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return redirect(url_for('users'))
