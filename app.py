from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__, template_folder='pages', static_folder='styles')
app.secret_key = 'clave_secreta_para_sesiones'

# Configuración de la base de datos
DATABASE = 'data/productos.db'

# Información del nodo
NODE_NAME = os.environ.get('NODE_NAME', 'Nodo-Local')
PORT = int(os.environ.get('PORT', 5000))

def init_db():
    """Inicializar la base de datos"""
    # Crear directorio de datos si no existe
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Crear tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')    
    
    # Crear tabla de productos
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    categoria TEXT NOT NULL,
                    cantidad INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    # Crear usuario admin por defecto
    admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO usuarios (username, email, password) VALUES (?, ?, ?)', 
                ('admin', 'admin@sistema.com', admin_password))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Generar hash de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', node_name=NODE_NAME, port=PORT)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT id, username FROM usuarios WHERE email = ? AND password = ?', 
                (email, hashed_password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = hash_password(password)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO usuarios (username, email, password) VALUES (?, ?, ?)', 
                    (username, email, hashed_password))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya existe', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/productos')
def productos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM productos ORDER BY created_at DESC')
    productos = c.fetchall()
    conn.close()
    
    return render_template('productos.html', productos=productos)

@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        cantidad = int(request.form.get('cantidad', 0))
        
        # Validaciones del backend
        if not descripcion or descripcion.strip() == '':
            flash('La descripción es obligatoria', 'error')
            return render_template('nuevo_producto.html')
        
        if cantidad <= 0:
            flash('La cantidad debe ser mayor a 0', 'error')
            return render_template('nuevo_producto.html')
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Verificar que no exista el código
        c.execute('SELECT id FROM productos WHERE codigo = ?', (codigo,))
        if c.fetchone():
            flash('Ya existe un producto con ese código', 'error')
            conn.close()
            return render_template('nuevo_producto.html')
        
        try:
            c.execute('''INSERT INTO productos (codigo, nombre, descripcion, categoria, cantidad)
                        VALUES (?, ?, ?, ?, ?)''', 
                    (codigo, nombre, descripcion, categoria, cantidad))
            conn.commit()
            flash('Producto registrado exitosamente', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            flash(f'Error al registrar producto: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('nuevo_producto.html')

@app.route('/consultar_disponibilidad')
def consultar_disponibilidad():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('consultar_disponibilidad.html')

@app.route('/api/producto/<codigo>')
def api_producto(codigo):
    """API para consultar disponibilidad en tiempo real"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT codigo, nombre, descripcion, categoria, cantidad FROM productos WHERE codigo = ?', (codigo,))
    producto = c.fetchone()
    conn.close()
    
    if producto:
        return jsonify({
            'codigo': producto[0],
            'nombre': producto[1],
            'descripcion': producto[2],
            'categoria': producto[3],
            'cantidad': producto[4],
            'disponible': producto[4] > 0
        })
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/api/productos')
def api_productos():
    """API para obtener todos los productos"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT codigo, nombre, descripcion, categoria, cantidad FROM productos')
    productos = c.fetchall()
    conn.close()
    
    productos_json = []
    for p in productos:
        productos_json.append({
            'codigo': p[0],
            'nombre': p[1],
            'descripcion': p[2],
            'categoria': p[3],
            'cantidad': p[4],
            'disponible': p[4] > 0
        })
    
    return jsonify(productos_json)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando {NODE_NAME} en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
