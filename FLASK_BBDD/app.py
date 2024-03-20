#!/bin/env python3
import re
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

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
        query = "INSERT INTO logs (data_hora, num_targeta_logs, acces) VALUES (NOW(), %s, %s)"
        cursor.execute(query, (numero_rfid, int(acceso)))
        db.commit()
    except mysql.connector.IntegrityError as err:
        # Maneig d'errors d'integritat de la base de dades
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print(f"Error en registrar el log: No hi ha referència per a la targeta {numero_rfid}.")
        else:
            print(f"Error d'integritat en registrar el log: {err}")
    except Exception as e:
        # Maneig d'altres errors
        print(f"Error en registrar el log: {e}")
    finally:
        # Tanca el cursor i la connexió amb la base de dades
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    numero_rfid = request.form.get('numero_rfid', '')
    try:
        if not re.match("^\d+$", numero_rfid):
            registrar_log(numero_rfid, False)  # Registra un log per un accés denegat a causa d'un format invàlid del número RFID
            return jsonify(False)

        # Estableix la connexió amb la base de dades
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )
        cursor = db.cursor()
        # Modifica la consulta per incloure la verificació de l'estat de la targeta
        cursor.execute("SELECT Estat FROM targeta WHERE num_targeta = %s", (numero_rfid,))
        resultat = cursor.fetchone()

        if resultat and resultat[0] == 1:
            registrar_log(numero_rfid, True)  # Registra un log per un accés concedit
            resultat = True
        else:
            registrar_log(numero_rfid, False)  # Registra un log per un accés denegat perquè la targeta està inactiva o no es va trobar
            resultat = False

    except Exception as e:
        registrar_log(numero_rfid, False)  # Registra un log per un accés denegat en cas d'error
        resultat = False
    finally:
        # Tanca el cursor i la connexió amb la base de dades
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

    return jsonify(resultat)

if __name__ == '__main__':
    # Inicia l'aplicació Flask i escolta a totes les adreces disponibles a través del port 5000
    app.run(host='0.0.0.0', debug=True)
