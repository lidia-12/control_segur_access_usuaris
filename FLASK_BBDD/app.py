#!/bin/env python3
import re  # Importem el mòdul per a les expressions regulars
from flask import Flask, request, jsonify  # Importem els mòduls Flask per a l'aplicació web i jsonify per a generar respostes JSON
import mysql.connector  # Importem el mòdul per a la connexió amb MySQL

app = Flask(__name__)  # Inicialitzem l'aplicació Flask

@app.route('/procesar_datos', methods=['POST'])  # Definim una ruta per a rebre les dades i processar-les mitjançant una sol·licitud POST
def procesar_datos():
    try:
        # Establim la connexió a la base de dades dins de la funció
        db = mysql.connector.connect(
            host="*",  # Indiquem l'amfitrió de la base de dades
            user="*",  # Especificem l'usuari per a la connexió
            password="*",  # Indiquem la contrasenya de l'usuari
            database="*"  # Especificem la base de dades a la qual connectar-nos
        )

        numero_rfid = request.form['numero_rfid']  # Obtenim el número RFID enviat a través del formulari

        # Verifiquem si el número RFID conté només dígits utilitzant una expressió regular
        if not re.match("^\d+$", numero_rfid):
            return jsonify(False)  # Si el número RFID no conté només dígits, retornem un missatge d'error

        cursor = db.cursor()  # Creem un cursor per interactuar amb la base de dades
        cursor.execute("SELECT * FROM targeta WHERE num_targeta = %s", (numero_rfid,))  # Executem una consulta SQL per comprovar si el número RFID existeix a la base de dades
        resultados = cursor.fetchall()  # Obtenim els resultats de la consulta

        # Ens assegurem de tancar el cursor i la connexió a la base de dades
        cursor.close()
        db.close()

        # Verifiquem si s'han trobat resultats a la consulta
        if resultados:
            return jsonify(True)  # Si s'han trobat resultats, retornem True indicant que el número RFID és vàlid
        else:
            return jsonify(False)  # Si no s'han trobat resultats, retornem False indicant que el número RFID no és vàlid

    except Exception as e:
        # En cas d'error, retornem False indicant que el processament ha fallat
        return jsonify(False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Iniciem l'aplicació Flask i l'escoltem a totes les interfícies, activant el mode de depuració
