import os

def conf_init():
    global AWS_KEYNAME, VPCID, DBUSER, DBPASS, DBHOST, DBNAME, BUCKETNAME,SEGGROUPNAME, EC2NAME

    print('Inicializando variables globales a partir de variables de entornos')
    DBUSER = os.getenv("DBUSER")
    DBPASS = os.getenv("DBPASS")
    DBHOST = os.getenv("DBHOST")
    DBNAME = os.getenv("DBNAME")


    BUCKETNAME = os.getenv("BUCKETNAME")
    DBNAME = os.getenv("SEGGROUPNAME")
    DBNAME = os.getenv("EC2NAME")

    AWS_KEYNAME = os.getenv("AWS_KEYNAME")
    VPCID = os.getenv("VPCID")

    print('[INFO] Se cargaron todas las variables de entorno')
    print('[INFO] Configuración terminada...')



def conf_init_local():
    global AWS_KEYNAME, VPCID, DBUSER, DBPASS, DBHOST, DBNAME, BUCKETNAME,SEGGROUPNAME, EC2NAME

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
    BUCKETNAME = env_vars["BUCKETNAME"]
    SEGGROUPNAME = env_vars["SEGGROUPNAME"]
    EC2NAME = env_vars["EC2NAME"]
    
    

    AWS_KEYNAME = env_vars["AWS_KEYNAME"]
    VPCID = env_vars["VPCID"]

    print('[INFO] Se cargaron todas las variables de entorno')
    print('[INFO] Configuración terminada...')