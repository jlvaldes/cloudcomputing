import boto3

from conf_initializer import conf_init, AWS_KEY_NAME, CONF_DONE, DBNAME, DBUSER, DBPASS

def ec2_up_infra(region = 'us-east-1', 
                 instanceType = 't2.micro', 
                 imageId='ami-090e0fc566929d98b', 
                 minCount=1, 
                 maxCount=1):
    
    if CONF_DONE == False:
        conf_init()

    print('Iniciando despliegue de infraestructura EC2')
    session = boto3.Session()
    ec2 = session.resource('ec2',  region_name = region)

    instance = ec2.create_instances(
        ImageId = imageId,
        MinCount=minCount,
        MaxCount=maxCount,
        InstanceType=instanceType,
        KeyName = AWS_KEY_NAME,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ec2_genome_model'
                    },
                ]
            },
        ]
    )
    print(f'Instancia ID={instance[0].id} creada exitosamente')


def rds_up_infra(vpcSecurityGroupId, 
                        region = 'us-east-1', 
                        dbInstance = 'db.t3.micro', 
                        dbEngine = 'postgres', 
                        allocatedStorageGB = 10,
                        backupRetentionPeriod = 0,
                        multiAZ = False):
    if CONF_DONE == False:
        conf_init()

    try:
        session = boto3.Session()
        rds = session.client('rds', region_name=region)

        rds.create_db_instance(
            DBName = DBNAME,
            DBInstanceIdentifier = 'rds_genome',
            MasterUsername = DBUSER,
            MasterUserPassword = DBPASS,
            DBInstanceClass = dbInstance,
            Engine = dbEngine, 
            AllocatedStorage = allocatedStorageGB,
            VpcSecurityGroupIds=[vpcSecurityGroupId], 
            BackupRetentionPeriod = backupRetentionPeriod, 
            MultiAZ = multiAZ,
            AutoMinorVersionUpgrade = True,
            PubliclyAccessible = True,
        )

        print("Base de datos creada con éxito")
    except Exception as e:
        print("Error al crear la base de datos: ", str(e))

    