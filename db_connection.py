# db_connection.py
import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="Abrechnung",    # Name deiner Datenbank
            user="mommegrewe",      # dein Benutzername
            password="",            # leer lassen, wenn du kein Passwort gesetzt hast
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("❌ Fehler bei der Verbindung:", e)
        return None
