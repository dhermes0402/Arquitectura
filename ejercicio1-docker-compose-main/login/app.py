from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import mysql.connector
import os
import hashlib

app = Flask(__name__)
CORS(app)

SECRET_KEY = "b59a91917620316e6375b5f884a715e6d677b1b8" # generado de forma aleatoria.

# Leer configuración de la base de datos desde variables de entorno
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME_AUTH', 'authentication')
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')
    
    if not user_name or not password:
        return jsonify({'error': 'Invalid input'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (user_name,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Generar el hash de la contraseña ingresada usando el salt almacenado
        salted_password = password + user['salted_pass']
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        # Comparar el hash generado con el almacenado en la base de datos
        if user['password'] == hashed_password:
            payload = {
                'user': user_name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/check', methods=['GET'])
def check():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'valid': False}), 401
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'valid': True, 'user': payload['user']})
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
