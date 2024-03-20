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
        # Defineix la consulta SQL per inserir un nou registre de log
        query = "INSERT INTO logs (data_hora, num_targeta_logs, acces) VALUES (NOW(), %s, %s)"
        # Executa la consulta amb els valors proporcionats i guarda els canvis
        cursor.execute(query, (numero_rfid, int(acceso)))
        db.commit()
    except mysql.connector.IntegrityError as err:
        # Gestiona els errors d'integritat de la base de dades
        print(f"Error en registrar el log: {err}")
    except Exception as e:
        # Gestiona altres errors possibles
        print(f"Error en registrar el log: {e}")
    finally:
        # Tanca el cursor i la connexió amb la base de dades
        cursor.close()
        db.close()

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    numero_rfid = request.form.get('numero_rfid', '')
    acceso_concedido = False  # Suposem inicialment que l'accés serà denegat
    if not re.match("^\d+$", numero_rfid):
        # Si el format no és vàlid, enregistra el intent com a fallit i respon
        registrar_log(numero_rfid, acceso_concedido)
        return jsonify(acceso_concedido)

    try:
        # Estableix la connexió amb la base de dades
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )
        cursor = db.cursor()
        cursor.execute("SELECT Estat FROM targeta WHERE num_targeta = %s", (numero_rfid,))
        resultado = cursor.fetchone()

        # Si troba la targeta i el seu estat és actiu, concedeix l'accés
        if resultado and resultado[0] == 1:
            acceso_concedido = True

    except Exception as e:
        # Gestiona els errors possibles en el processament de les dades
        print(f"Error en processar les dades: {e}")
    finally:
        # Registra l'intent amb el resultat final i tanca els recursos de la BD
        registrar_log(numero_rfid, acceso_concedido)
        cursor.close()
        db.close()

    return jsonify(acceso_concedido)

if __name__ == '__main__':
    # Inicia l'aplicació Flask i escolta a totes les adreces disponibles a través del port 5000
    app.run(host='0.0.0.0', debug=True)
