from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_ssm as ssm
)

def create_dynamodb_table(scope) :
    ddb_table = dynamodb.Table(
        scope, 
        "DemoTable",
        partition_key = dynamodb.Attribute(name = "Name", type = dynamodb.AttributeType.STRING),
        billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
    )

    ssm.StringParameter(scope, "DynamoTableNameParam",
        parameter_name = "/config/cdk_demo/dynamodb/table_name",
        string_value = ddb_table.table_name
    )


    return ddb_table