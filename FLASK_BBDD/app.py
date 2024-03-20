#!/bin/env python3
import re
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    try:
        # Estableix la connexió a la base de dades utilitzant els paràmetres especificats
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )

        # Obtenir el valor del camp 'numero_rfid' de la sol·licitud POST
        numero_rfid = request.form['numero_rfid']

        # Verificar si el número RFID conté només dígits utilitzant una expressió regular
        if not re.match("^\d+$", numero_rfid):
            return jsonify(False)

        # Crear un cursor per a executar consultes SQL
        cursor = db.cursor()

        # Executar una consulta SQL per obtenir dades de la taula 'targeta' amb el número RFID proporcionat
        cursor.execute("SELECT * FROM targeta WHERE num_targeta = %s", (numero_rfid,))
        resultados = cursor.fetchall()

        # Assegurar-se de tancar el cursor i la connexió a la base de dades
        cursor.close()
        db.close()

        # Verificar si s'han trobat resultats
        if resultados:
            return jsonify(True)
        else:
            return jsonify(False)

    except Exception as e:
        # En cas de qualsevol error, considerar-ho com a fallit i retornar False
        return jsonify(False)

if __name__ == '__main__':
    # Iniciar l'aplicació Flask i escoltar a totes les adreces disponibles a través del port 5000
    app.run(host='0.0.0.0', debug=True)
