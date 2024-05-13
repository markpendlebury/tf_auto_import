# tf_auto_import
A hacked together idea of how to import aws_iam_role resources based on a list of role names, It will check AWS and terraform state for the existence of said role and generate terraform configuration if it exists in aws but not in state
