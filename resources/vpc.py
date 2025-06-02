from aws_cdk import (
    aws_ec2 as ec2
)

def create_vpc_for_eks(scope) :
    # Create VPC with only private subnets and NAT gateways
    vpc_for_eks = ec2.Vpc(scope, "EksPrivateVpc",
        max_azs=2,
        nat_gateways=0,
        subnet_configuration=[
        ec2.SubnetConfiguration(
            name="Public",
            subnet_type=ec2.SubnetType.PUBLIC,
            cidr_mask=24
        ),
            ec2.SubnetConfiguration(
                name="Private",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                cidr_mask=24
            )
        ]
    )

    return vpc_for_eks