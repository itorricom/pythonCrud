
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "mykey"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'python'
mysql.init_app(app)


@app.route('/')
def index():
    #sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Isidoro', 'itorrico.m@gmail.com', 'foto.jpg');"
    sql = "SELECT * FROM `empleados` ;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    
    empleados = cursor.fetchall()
    print(empleados)

    conn.commit()
    return render_template('empleados/index.html',empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id))
    empleados = cursor.fetchall()
    conn.commit()
    print(empleados)
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _telefono = request.form['txtTelefono']
    id = request.form['txtID']
    sql = "UPDATE empleados SET nombre=%s, correo=%s, telefono=%s WHERE id=%s;"
    datos= (_nombre, _correo, _telefono ,id)
    conn = mysql.connect()
    cursor = conn.cursor()  
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _telefono = request.form['txtTelefono']

    if _nombre == '' or _correo == '' or _telefono == '':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))   
        
    # sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Isidoro', 'itorrico.m@gmail.com', 'foto.jpg');"
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `telefono`) VALUES (NULL, %s, %s, %s);"
    
    #datos = (_nombre, _correo, _foto.filename) 
    datos = (_nombre, _correo, _telefono) 
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    #return render_template('empleados/index.html')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

# 1:55 Manejo de mensajes de validacion