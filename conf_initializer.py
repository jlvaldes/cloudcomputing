import os

def conf_init():
    print('Carga de variables de entornos')
    dbuser = os.getenv("DBUSER")
    dbpass = os.getenv("DBPASS")
    dbhost = os.getenv("DBHOST")
    dbname = os.getenv("DBNAME")

    bucketname = os.getenv("BUCKET_NAME")
    bucket_access_key = os.getenv("BUCKET_ACCESS_KEY_ID")
    bucket_secret = os.getenv("BUCKET_SECRET_ACCESS_KEY")
    bucket_token = os.getenv("BUCKET_SESSION_TOKEN")


    print('Se cargaron todas las variables de entorno')
    print('Configuración terminada...')
