# tf_auto_import

A hacked together idea of how to import aws_iam_role resources based on a list of role names, It will check AWS and terraform state for the existence of said role and generate terraform configuration if it exists in aws but not in state


# Usage

if needed add your aws profile name to line 7

1. cd src
2. pip install boto3
3. add some roles that exist and some roles that don't exist to `roles_by_name` on line 11
4. specify your terraform state file (or run cd ../terraform && terraform init / plan / apply on an empty config to generate one )
4. python3 main.py


This will: 
1. for each role_by_name
2. If the role exists in aws
3. AND the role does NOT exist in state
4. Generate a terraform import block for it and write it to a file inside the ../terraform directory
5. Use terraform to generate the configuration 
