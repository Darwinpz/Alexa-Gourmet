from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn
from objects.carrito import Carrito

def index_carrito(request):

    try:
        
        alerts = {"tipo":"","message":""}

        cars = []

        totals = (0,)

        user_id = session['id']

        cod_compras = ""

        with conn.cursor() as cursor:
            sql = "Select car_id,prod_imagen,prod_nombre,prod_precio,car_cantidad,car_cod_compra from carrito,productos where car_producto=prod_id and car_user=%s and car_estado=true"
            cursor.execute(sql,(user_id,))
            cars = cursor.fetchall()

            sql = "Select sum(prod_precio*car_cantidad) from carrito,productos where car_producto=prod_id and car_user=%s and car_estado=true"
            cursor.execute(sql,(user_id,))
            totals = cursor.fetchone()

            if len(cars) >= 1:
                cod_compras = cars[0][5]


        return render_template('/views/carrito.html', carritos=cars, total = totals, cod_compra=cod_compras)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/carrito.html',alert=alerts, carritos=cars, total = totals)


def add_carrito(request):

    if request.method == 'POST':

        try:

            user_id = session['id']

            cars = Carrito(
                cantidad = request.form["car_cantidad"],
                prod_id = request.form["car_producto"],
                estado = True,
                car_cod_compra= "user"+user_id.__str__()+"_"
            )
            
            alerts = {"tipo":"","message":""}

            with conn.cursor() as cursor:

                sql = "Select MAX(car_cod_compra), car_estado from carrito where car_user=%s group by car_id"
                cursor.execute(sql,(user_id,))
                max_car =  cursor.fetchone()

                sql = "Select * from productos where prod_id = %s"
                cursor.execute(sql,(cars.prod_id,))
                product = cursor.fetchone()

                if product[7] < int(cars.cantidad) :
                    alerts["tipo"] = "danger"
                    alerts["message"] = "Pedido menor al stock actual"

                    return render_template('/views/platos/detalle.html',alert=alerts, producto=product) 

                else:

                    if max_car!= None and max_car[0] !=None:
                    
                        #cars.car_cod_compra = cars.car_cod_compra+ (int(max_car[0].split('_')[1])+1).__str__()
                        cars.car_cod_compra = max_car[0]

                        if max_car[1] == True:
                            cars.car_cod_compra = max_car[0]
                        else:
                            cars.car_cod_compra = cars.car_cod_compra+ (int(max_car[0].split('_')[1])+1).__str__()
                            

                    else:
                        cars.car_cod_compra = cars.car_cod_compra+"1"

                    sql = "Insert into carrito(car_user, car_producto, car_cantidad, car_estado, car_cod_compra) VALUES(%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(user_id,cars.prod_id,cars.cantidad,cars.estado,cars.car_cod_compra))

                    alerts["tipo"] = "success"
                    alerts["message"] = "Carrito Agregado"

            conn.commit()

                
            return redirect(url_for('carrito'))
            
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)
            print(e)
            return redirect(url_for('err_500'))    
        
    else:
        return jsonify({"message":"metodo no correcto"}),500


def eliminar_carrito(request):

    try:

        car_id = request.args.get("id")
        
        user_id = session['id']

        alerts = {"tipo":"","message":""}

        with conn.cursor() as cursor:
            sql = "Delete from carrito where car_user = %s and car_id=%s"
            cursor.execute(sql,(user_id,car_id))
        conn.commit()

        alerts["tipo"] ="success"
        alerts["message"] = "Carrito Eliminado"
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return redirect(url_for('carrito'))

