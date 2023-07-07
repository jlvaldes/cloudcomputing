import os

def conf_init():
    global AWS_KEYNAME, VPCID, DBUSER, DBPASS, DBHOST, DBNAME, BUCKET_NAME, BUCKET_ACCESS_KEY_ID, BUCKET_SECRET_ACCESS_KEY, BUCKET_SESSION_TOKEN

    print('Inicializando variables globales a partir de variables de entornos')
    DBUSER = os.getenv("DBUSER")
    DBPASS = os.getenv("DBPASS")
    DBHOST = os.getenv("DBHOST")
    DBNAME = os.getenv("DBNAME")

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET_ACCESS_KEY_ID = os.getenv("BUCKET_ACCESS_KEY_ID")
    BUCKET_SECRET_ACCESS_KEY = os.getenv("BUCKET_SECRET_ACCESS_KEY")
    BUCKET_SESSION_TOKEN = os.getenv("BUCKET_SESSION_TOKEN")

    AWS_KEYNAME = os.getenv("AWS_KEYNAME")
    VPCID = os.getenv("VPCID")

    print('[INFO] Se cargaron todas las variables de entorno')
    print('[INFO] Configuración terminada...')



def conf_init_local():
    global AWS_KEYNAME, VPCID, DBUSER, DBPASS, DBHOST, DBNAME, BUCKET_NAME, BUCKET_ACCESS_KEY_ID, BUCKET_SECRET_ACCESS_KEY, BUCKET_SESSION_TOKEN

    print('Inicializando variables globales a partir de variables de entornos')
    with open('env.list', 'r') as file:
        lines = file.readlines()

    env_vars = {}
    for line in lines:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            env_vars[key] = value

    
    DBUSER = env_vars["DBUSER"] 
    DBPASS = env_vars["DBPASS"]
    DBHOST = env_vars["DBHOST"]
    DBNAME = env_vars["DBNAME"]

    AWS_KEYNAME = env_vars["AWS_KEYNAME"]
    VPCID = env_vars["VPCID"]

    print('[INFO] Se cargaron todas las variables de entorno')
    print('[INFO] Configuración terminada...')