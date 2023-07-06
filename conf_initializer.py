import os

CONF_DONE = False

DBUSER = None
DBPASS = None
DBHOST = None
DBNAME = None

BUCKET_NAME=None
BUCKET_ACCESS_KEY_ID=None
BUCKET_SECRET_ACCESS_KEY=None
BUCKET_SESSION_TOKEN=None

AWS_KEY_NAME=None


def conf_init():
    print('Inicializando variables globales a partir de variables de entornos')
    DBUSER = os.getenv("DBUSER")
    DBPASS = os.getenv("DBPASS")
    DBHOST = os.getenv("DBHOST")
    DBNAME = os.getenv("DBNAME")

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET_ACCESS_KEY_ID = os.getenv("BUCKET_ACCESS_KEY_ID")
    BUCKET_SECRET_ACCESS_KEY = os.getenv("BUCKET_SECRET_ACCESS_KEY")
    BUCKET_SESSION_TOKEN = os.getenv("BUCKET_SESSION_TOKEN")


    AWS_KEY_NAME = os.getenv("AWS_KEY_NAME")

    CONF_DONE = True
    print('Se cargaron todas las variables de entorno')
    print('Configuración terminada...')
