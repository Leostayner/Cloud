from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='openstack')

images = conn.list_images()

for image in images:
	print("Images: ")
	print(image)
	print("\n")

flavors =  conn.list_flavors()

for flavor in flavors:
	print("Flavors: ")
	print(flavor)
	print("\n")

#Create Image
image_id = 'b65a38f8-a432-469a-ac69-5b810d92cfc4'
image = conn.get_image(image_id)
print("Imagem Criada: ")
print(image)
print("\n")

#Create Flavor
flavor_id = '07c60d5d-f7da-4308-a2e1-81593d3ce3fb'
flavor = conn.get_flavor(flavor_id)
print("Flavor Criado: ")
print(flavor)
print("\n")


#Create Instance
instance_name = 'teste'


#Print Instance
instances = conn.list_servers()
for instance in instances:
	print("\n")
	print("instancia: ")
	print(instance)
	print("\n")

#Check SSH Public Key
print('Checking for existing SSH keypair...')
keypair_name = 'LeoKey'
pub_key_file = '/home/cloud/.ssh/L.pub'

if conn.search_keypairs(keypair_name):
	print('Keypair already exists. Skipping import.')
	print("\n")
else:
	print('Adding keypair...')
	print("\n")
	conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

for keypair in conn.list_keypairs():
    print(keypair)

#Check Security Group
print('\n Checking for existing security groups...\n')
sec_group_name = 's_L'
if conn.search_security_groups(sec_group_name):
	print("\n")
	print('Security group already exists. Skipping creation.')
	print("\n")
else:
    print('Creating security group.')
    print("\n")
    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

conn.search_security_groups(sec_group_name)


ex_userdata = '''#!/bin/bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

instance_name = 'all-in-one'
testing_instance = conn.create_server(wait=True, auto_ip=False,
    name=instance_name,
    image=image_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[sec_group_name],
    userdata=ex_userdata)

f_ip = conn.available_floating_ip()


#step-14
conn.add_ip_list(testing_instance, [f_ip['floating_ip_address']])

