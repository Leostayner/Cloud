import boto3

def save(name, data):
    outfile = open(name,'w')
    outfile.write(data)
    outfile.close()
    print("Key Pair Saved")

def create_key_pair(client):
    try:
        response = client.delete_key_pair(
            KeyName='L',
        )
        print("Delete old Key Pair")

    except:
        pass

    key_pair = client.create_key_pair(
        KeyName='L',
    )
    print("Create Key Pair")
    
    save("./key/L.pem", str(key_pair["KeyMaterial"]))
    

def create_security_group(client):
    try:
        client.delete_security_group(
            GroupName='APS_L',
        )
        print("Delete Old Security Group")
    
    except:
        pass

    s_gp = client.create_security_group(
        Description='Security group APS3',
        GroupName='APS_L',
    )
    print("Create Security Group")

    client.authorize_security_group_ingress(
        GroupName ='APS_L',
        IpPermissions = [{
                'IpProtocol' :"tcp",
                'FromPort' : 5000,
                'ToPort'  : 5000,
                'IpRanges': [{"CidrIp" : "0.0.0.0/0"}]
                },
                {
                'IpProtocol' :"tcp",
                'FromPort' : 22,
                'ToPort' : 22,        
                'IpRanges': [{"CidrIp" : "0.0.0.0/0"}]
                }
            ]
        
    )
    print("Authorize Security Group")

def create_instance(ec2):
    instances = ec2.create_instances(
        ImageId='ami-0ac019f4fcb7cb7e6',
        MinCount= 3,
        MaxCount= 3,
        InstanceType = 't2.micro',
        SecurityGroups = ["APS_L"],
        KeyName= "L",
        TagSpecifications=[
            {
                'ResourceType': 'instance',

                'Tags': [
                    {
                        'Key': 'Owner',
                        'Value': "Leonardo Medeiros",
                    },
                ]
            },
        ],
        UserData = """#!/bin/bash
        git clone https://github.com/Leostayner/Cloud-APS1
        cd /Cloud-APS1  
        . install.sh
        """
    )
    print("Create Instance")

def check_terminate(ec2, client):
    print("Check Treminate")
    list_instances = ec2.instances.all()
    
    list_id = []
    
    for instance in list_instances:
        list_tags = (instance.tags)

        try:
            for tag in list_tags:
                if (tag["Key"] == "Owner") and (tag["Value"] == "Leonardo Medeiros"):
                    list_id.append(instance.id)
                             
        except:
            pass
        
    if len(list_id) > 0:
        terminate_instances(client, list_id)

def terminate_instances(client, list_id):
    waiter = client.get_waiter('instance_terminated')
    client.terminate_instances(
        InstanceIds = list_id
    )
    print("Wait Delete {0} Instance".format(len(list_id)))
    waiter.wait(InstanceIds=list_id)
    print("Instances Deleted: {0}".format(len(list_id)))



#Client and Resource
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

#Teminate instances
check_terminate(ec2, client)

#Create Key Par
create_key_pair(client)

# Create Security Group
create_security_group(client)

# Create Instance
create_instance(ec2)






