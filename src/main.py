import boto3
import json
import subprocess
import os


boto3.setup_default_session(profile_name='')


state_file = '../terraform/terraform.tfstate'
roles_by_name = ["", "", ""]

# Create a boto3 client for IAM
client = boto3.client('iam')

def role_exists_in_aws(role_name):
    # Here we list all the roles in our account
    # if the role we're looking for exists we return true

    response = client.list_roles()
    roles = response['Roles']
    
    for role in roles:
        if role['RoleName'] == role_name:
            print(f"[AWS] Role {role_name} found in AWS")
            return True

    print(f"[AWS] Role {role_name} not found in AWS")
    return False


def role_exsits_in_state(state_file, role_name):
    # Open state file, this works only with a local state file
    # could be refactored to work with s3 or some other remote state
    with open(state_file, 'r') as f:
        state = json.load(f)
        
    for resource in state['resources']:
        if resource['type'] == 'aws_iam_role':
            if resource['name'] == role_name:
                print(f"[STATE] Role {role_name} found in state file")
                return True
    print(f"[STATE] Role {role_name} not found in state file")
    return False



def generate_import_file():
    # Here we generate a list of import blocked formatted like so: 

    # import {
    #     to = aws_iam_role.role_name
    #     id = "the_id_of_the_role"
    # }

    # a block is generated for each role that exists in AWS but not in the state file

    import_blocks = []

    for role in roles_by_name:
        if not role_exsits_in_state(state_file, role):
            if role_exists_in_aws(role):
                print(f"Generating import block for role {role}")
                import_blocks.append(f"import {{\n    to = aws_iam_role.{role}\n    id = \"{role}\"\n}}")

    for block in import_blocks:
        with open('../terraform/import_blocks.tf', 'a') as f:
            f.write(block)
            f.write('\n\n')




def run_terraform():
    # Run terraform plan --generate-config-out=generated_imports.tf to generate 
    # the appropriate terraform config based on our import blocks above

    if os.path.exists('../terraform/generated_imports.tf'):
        os.remove('../terraform/generated_imports.tf')

    subprocess.run(['terraform', 'plan', '-generate-config-out=generated_imports.tf'], cwd='../terraform')



# run that shiz:
generate_import_file()
run_terraform()