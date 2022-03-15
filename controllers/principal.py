from flask import jsonify, render_template,session,redirect,url_for
from database.postgresql import conn


def index_principal(request):

    try:

        alerts = {"tipo":"","message":""}

        products = []

        with conn.cursor() as cursor:
            sql = "Select *from productos order by prod_vistas desc limit 6"
            cursor.execute(sql)
            products = cursor.fetchall()

        return render_template('/views/index.html', productos=products)    
                                    
    except Exception as e:
        alerts["tipo"] ="danger"
        alerts["message"] = str(e)

    return render_template('/views/index.html',alert=alerts, productos=products)

