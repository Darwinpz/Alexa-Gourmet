from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn


def index_platos(request):

    try:
        
        cat_id = request.args.get("categoria")

        categories = []

        alerts = {"tipo":"","message":""}

        products = []

        cat_actual = ""

        with conn.cursor() as cursor:
            sql = "Select *from categorias"
            cursor.execute(sql)
            categories = cursor.fetchall()
            
            if cat_id :
                sql = "Select *from productos,categorias where prod_categoria = cat_id and cat_id = %s"
                cursor.execute(sql,(cat_id,))
                products =  cursor.fetchall()
                cat_actual = products[0][10]

            else:
                sql = "Select *from productos"
                cursor.execute(sql)
                products =  cursor.fetchall()
                cat_actual = "Todo"

        return render_template('/views/platos/index.html', categorias=categories, productos=products, categoria_actual=(": "+cat_actual))    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/platos/index.html',alert=alerts, categorias=categories, productos=products, categoria_actual=(": "+cat_actual))


def detalle_platos(request):

    try:
        
        prod_id = request.args.get("id")

        alerts = {"tipo":"","message":""}

        if prod_id:

            with conn.cursor() as cursor:
                
                sql = "Update productos set prod_vistas = (prod_vistas+1) where prod_id= %s"
                cursor.execute(sql,(prod_id,))

                sql = "Select *from productos,categorias where prod_categoria = cat_id and prod_id =%s"
                cursor.execute(sql,(prod_id,))
                product = cursor.fetchone()
            conn.commit()
                
            return render_template('/views/platos/detalle.html', producto=product) 
        
        else:
            return redirect(url_for('platos'))
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/platos/detalle.html',alert=alerts, producto=product )