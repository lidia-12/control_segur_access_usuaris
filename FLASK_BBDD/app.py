#!/bin/env python3
import re
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def registrar_log(numero_rfid, acceso):
    try:
        # Estableix la connexió amb la base de dades
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )
        cursor = db.cursor()
        
        # Inserta un nou registre de log amb la data i hora actual, el número RFID i l'estat d'accés
        query = "INSERT INTO logs (data_hora, num_targeta_logs, acces) VALUES (NOW(), %s, %s)"
        # Converteix el valor booleà en un enter (True -> 1, False -> 0) per a la compatibilitat amb la base de dades
        cursor.execute(query, (numero_rfid, int(acceso)))
        db.commit()
    except Exception as e:
        print(f"Error al registrar log: {e}")
    finally:
        # Tanca el cursor i la connexió a la base de dades
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    numero_rfid = request.form.get('numero_rfid', '')
    try:
        # Verifica si el número RFID conté només dígits
        if not re.match("^\d+$", numero_rfid):
            registrar_log(numero_rfid, False)  # Registra un log indicant que l'accés ha estat denegat
            return jsonify(False)

        # Estableix la connexió amb la base de dades
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )
        cursor = db.cursor()
        
        # Executa una consulta SQL per comprovar si el número RFID és vàlid
        cursor.execute("SELECT * FROM targeta WHERE num_targeta = %s", (numero_rfid,))
        resultados = cursor.fetchall()

        if resultados:
            registrar_log(numero_rfid, True)  # Registra un log indicant que l'accés ha estat concedit
            resultado = True
        else:
            registrar_log(numero_rfid, False)  # Registra un log indicant que l'accés ha estat denegat
            resultado = False

    except Exception as e:
        registrar_log(numero_rfid, False)  # Registra un log indicant que l'accés ha estat denegat en cas d'error
        resultado = False
    finally:
        # Tanca el cursor i la connexió a la base de dades
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

    return jsonify(resultado)

if __name__ == '__main__':
    # Inicia l'aplicació Flask i escolta a totes les adreces disponibles a través del port 5000
    app.run(host='0.0.0.0', debug=True)
