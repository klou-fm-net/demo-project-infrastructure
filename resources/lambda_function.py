from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambdafunc
)

def create_iam_role(scope) :
    return iam.Role(
        scope,
       "LambdaExecutionRole",
        assumed_by = iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies = [
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        ]
    )

def create_lambda_function(scope, dynamodb_table) :
    lambda_role = create_iam_role(scope)
    dynamodb_table.grant_read_write_data(lambda_role)

    lambda_role.add_to_policy(iam.PolicyStatement(
        actions=["ssm:GetParameter"],
        resources=[f"arn:aws:ssm:{scope.region}:{scope.account}:parameter/config/*"]
    ))
    
    return lambdafunc.Function(
        scope, 
        "lambdaId",
        runtime = lambdafunc.Runtime.PYTHON_3_9,
        code = lambdafunc.Code.from_asset("lambda_functions"),
        handler = "api_handler.main",
        role = lambda_role
    )

