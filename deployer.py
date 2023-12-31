import boto3
import conf_initializer
from conf_initializer import conf_init_local
from botocore.exceptions import ClientError


def deploy():
    print('Inicio de despliegue de infraestructura')
    conf_init_local()
    ec2_up_infra()
    rds_up_infra()
    s3_up_infra()


def ec2_up_infra(region = 'us-east-1', 
                 instanceType = 't2.micro', 
                 imageId='ami-090e0fc566929d98b', 
                 minCount=1, 
                 maxCount=1):

    print('Iniciando despliegue de infraestructura EC2')
    session = boto3.Session()
    ec2 = session.resource('ec2',  region_name = region)

    instance = ec2.create_instances(
        ImageId = imageId,
        MinCount=minCount,
        MaxCount=maxCount,
        InstanceType=instanceType,
        KeyName = conf_initializer.AWS_KEYNAME,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': conf_initializer.EC2NAME
                    },
                ]
            },
        ]
    )
    print(f'  [INFO] Instancia ID={instance[0].id} creada exitosamente')


def vpc_securitygroup(region = 'us-east-1' ):
        print("  [INFO] Creando grupo de seguridad y reglas de acceso")
        genome_group_name = conf_initializer.SEGGROUPNAME
        ec2_client = boto3.client('ec2', region_name = region)
        response = ec2_client.describe_security_groups()
        security_groups = response['SecurityGroups']
        group = [obj for obj in security_groups if obj['GroupName'] == genome_group_name]

        if len(group) == 0:
            print("  [INFO] Creando grupo de seguridad")

            response = ec2_client.create_security_group(
                        Description='Grupo de seguridad para el RDS de Genome',
                        GroupName=genome_group_name,
                        VpcId=conf_initializer.VPCID
                        )

            security_group_id = response['GroupId']

            response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
            security_group = response['SecurityGroups'][0]
            egress_rules = security_group['IpPermissionsEgress']
            ingress_rules = security_group['IpPermissions']
            
            if any(rule['IpRanges'] == [{'CidrIp': '0.0.0.0/0'}] and rule['IpProtocol'] == '3306' for rule in ingress_rules):
                print("  [INFO] La regla de ingress ya existe")
            else:
                print("  [INFO] Creando regla de ingreso")

                ec2_client.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 3306,
                            'ToPort': 3306,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )

            if any(rule['IpRanges'] == [{'CidrIp': '0.0.0.0/0'}] and rule['IpProtocol'] == '-1' for rule in egress_rules):
                print("  [INFO] La regla de egress ya existe.")
            else:
                print("  [INFO] Creando regla de salida")
                ec2_client.authorize_security_group_egress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {
                            'IpProtocol': '-1',
                            'FromPort': -1,
                            'ToPort': -1,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )

            print("  [INFO] Grupo de seguridad y reglas de entrada/salida configuradas")
        else:
            security_group_id = group[0]['GroupId']
            print(f'  [INFO] El grupo de seguridad {genome_group_name} con ID={security_group_id} ya estaba creado')

        return security_group_id


def db_exist(dbname, region = 'us-east-1'):
    rds_client = boto3.client('rds', region_name=region)
    response = rds_client.describe_db_instances()
    instances = response['DBInstances']
    db =  [instance for instance in instances if instance['DBInstanceIdentifier'] == dbname]
    return len(db) > 0
    

def rds_up_infra(region = 'us-east-1', 
                        dbInstance = 'db.t3.micro', 
                        dbEngine = 'postgres', 
                        allocatedStorageGB = 10,
                        backupRetentionPeriod = 0,
                        multiAZ = False):
    
    security_group_id = vpc_securitygroup(region)

    try:
        db_genome_name = conf_initializer.DBNAME
        if db_exist(dbname = db_genome_name, region = region):
            print(f'  [INFO] Ya existe una base de datos con el nombre {db_genome_name} en una instancia de RDS')
        else:
            session = boto3.Session()
            rds = session.client('rds', region_name=region)
            print('  [INFO] Se creó el cliente de RDS')

            rds.create_db_instance(
                DBName = db_genome_name,
                DBInstanceIdentifier = db_genome_name,
                MasterUsername = conf_initializer.DBUSER,
                MasterUserPassword = conf_initializer.DBPASS,
                DBInstanceClass = dbInstance,
                Engine = dbEngine, 
                AllocatedStorage = allocatedStorageGB,
                VpcSecurityGroupIds=[security_group_id], 
                BackupRetentionPeriod = backupRetentionPeriod, 
                MultiAZ = multiAZ,
                AutoMinorVersionUpgrade = True,
                PubliclyAccessible = True,
            )

            print("  [INFO] Base de datos creada con éxito")
    except Exception as e:
        print("  [ERR] Error al crear la base de datos: ", str(e))


def exist_s3(instance_name, region = 'us-east-1'):
    s3_client = boto3.client('s3', region)

    try:
        s3_client.head_bucket(Bucket=instance_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            print(f"  [ERR] Error al verificar la instancia de S3: {e}")
            return False

def s3_up_infra(region = 'us-east-1'):
    bucket_name = conf_initializer.BUCKETNAME

    if exist_s3(bucket_name, region) == False:
        try:
            s3_client = boto3.client('s3', region)
            s3_client.create_bucket(
                    Bucket=bucket_name
                )

            print("  [INFO] Instancia S3 creada con éxito")
        except Exception as e:
            print("  [ERR] Error al crear la la instancia S3: ", str(e))
    else:
        print(f'  [INFO] Ya existe una instancia S3 con el nombre {bucket_name}')


if __name__ == '__main__':
    deploy()