import psycopg2
def get_connection():
    return psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    