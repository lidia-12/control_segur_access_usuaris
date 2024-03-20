#!/bin/env python3

# Importació de les llibreries necessàries per al funcionament de l'aplicació.
import re  # Utilitzat per a la validació del format mitjançant expressions regulars.
from flask import Flask, request, jsonify  # Flask per crear l'aplicació web i manejar les sol·licituds.
import mysql.connector  # Connector de MySQL per a operacions de base de dades.
from mysql.connector import errorcode  # Mòdul per identificar errors específics de MySQL.

# Inicialització de l'aplicació Flask.
app = Flask(__name__)

def registrar_log(numero_rfid, acceso, desc='D'):
    """
    Funció per registrar un intent d'accés a la taula de logs.

    Args:
        numero_rfid (str): El número de la targeta RFID que s'intenta validar.
        acceso (bool): Indica si l'accés ha estat concedit (True) o denegat (False).
        desc (str): Descripció de l'intent, amb '-' si la targeta és vàlida i 'D' si no ho és.
    """
    try:
        # Establiment de la connexió amb la base de dades.
        db = mysql.connector.connect(
            host="*",  # Adreça del servidor de la base de dades.
            user="*",  # Usuari de la base de dades.
            password="*",  # Contrasenya de l'usuari.
            database="*"  # Nom de la base de dades a utilitzar.
        )
        cursor = db.cursor()  # Creació d'un cursor per executar operacions a la base de dades.

        # Definició de la consulta SQL per inserir el registre a la taula de logs.
        query = "INSERT INTO logs (data_hora, num_targeta_logs, acces, targ_desc) VALUES (NOW(), %s, %s, %s)"
        cursor.execute(query, (numero_rfid, int(acceso), desc))  # Execució de la consulta amb els paràmetres proporcionats.
        db.commit()  # Confirmació de la transacció per assegurar que els canvis es guarden a la base de dades.
    except Exception as e:
        # Gestió de qualsevol excepció que es produeixi durant el procés i la impressió de l'error.
        print(f"Error en registrar log: {e}")
    finally:
        # Tancament del cursor i la connexió a la base de dades.
        cursor.close()
        db.close()

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    """
    Endpoint per processar sol·licituds POST, validar el número de targeta RFID i registrar l'intent a la base de dades.

    Returns:
        JSON response: Resposta en format JSON indicant si l'accés ha estat concedit (True) o denegat (False).
    """
    # Extracció del número RFID enviat en la sol·licitud POST.
    numero_rfid = request.form.get('numero_rfid', '')
    desc = 'D'  # Descripció inicial suposant que la targeta no existeix.
    acceso_concedido = False  # Suposició inicial que l'accés serà denegat.

    # Validació del format del número RFID usant expressions regulars.
    if not re.match("^\d+$", numero_rfid):
        # Si el número no compleix el format, es registra com a accés denegat i es respon.
        registrar_log(numero_rfid, acceso_concedido, desc)
        return jsonify(acceso_concedido)

    try:
        # Connexió a la base de dades per verificar l'estat de la targeta.
        db = mysql.connector.connect(
            host="*",
            user="*",
            password="*",
            database="*"
        )
        cursor = db.cursor()
        # Consulta per obtenir l'estat de la targeta basat en el número RFID.
        cursor.execute("SELECT Estat FROM targeta WHERE num_targeta = %s", (numero_rfid,))
        resultado = cursor.fetchone()

        # Si troba un registre i l'estat és 1 (actiu), s'atorga l'accés.
        if resultado and resultado[0] == 1:
            desc = '-'  # La targeta existeix i està activa.
            acceso_concedido = True
    except Exception as e:
        # Gestió d'excepcions durant el procés de verificació.
        print(f"Error al processar dades: {e}")
    finally:
        # Es registra l'intent d'accés amb els detalls obtinguts.
        registrar_log(numero_rfid, acceso_concedido, desc)
        # Tancament del cursor i la connexió a la base de dades.
        cursor.close()
        db.close()

    # Resposta indicant si l'accés ha estat concedit o denegat.
    return jsonify(acceso_concedido)

# Punt d'entrada principal que inicia l'aplicació Flask si aquest script s'executa directament
if __name__ == '__main__':
    # Inicia l'aplicació Flask per escoltar a totes les adreces disponibles a través del port 5000
    app.run(host='0.0.0.0', debug=True)
