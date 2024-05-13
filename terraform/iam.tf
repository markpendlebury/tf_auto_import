# Leaving this as an example: 

# data "aws_iam_role" "imported" {
#   for_each = { for role in local.roles : role => role }
#   name     = each.value
# }
