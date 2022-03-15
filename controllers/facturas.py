from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn
from objects.factura import Factura

def index_facturas(request):

    try:
        
        alerts = {"tipo":"","message":""}

        facts = []

        user_id = session['id']

        with conn.cursor() as cursor:
            sql = "Select * from factura where fact_user_id=%s "
            cursor.execute(sql,(user_id,))
            facts = cursor.fetchall()

        return render_template('/views/facturas.html', facturas=facts)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/facturas.html',alert=alerts, facturas=facts)


def add_factura(request):

    if request.method == 'POST':
        
        try:

            alerts = {"tipo":"","message":""}

            user_id = session['id']

            facts = Factura(
                subtotal = request.form["fact_subtotal"],
                total = request.form["fact_total"],
                forma_pago = request.form["fact_forma_pago"],
                valor_pagado = request.form["fact_valor_pagado"],
                cod_compra =  request.form["fact_car_cod_compra"]
            )

            with conn.cursor() as cursor:

                sql = "Insert into factura(fact_subtotal, fact_total, fact_forma_pago, fact_valor_pagado, fact_car_cod_compra, fact_user_id) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(facts.subtotal,facts.total,facts.forma_pago,facts.valor_pagado,facts.cod_compra, user_id))

                sql = "UPDATE carrito set car_estado=false where car_cod_compra=%s"
                cursor.execute(sql,(facts.cod_compra,))

                alerts["tipo"] = "success"
                alerts["message"] = "Pedido Agregado"

            conn.commit()

            return redirect(url_for('facturas'))
        
        except Exception as e:
            alerts["tipo"] ="danger"
            alerts["message"] = str(e)
            print(e)
            return redirect(url_for('err_500'))    
        
    else:
        return jsonify({"message":"metodo no correcto"}),500