from aws_cdk import (
   aws_eks as eks,
   aws_ec2 as ec2,
   aws_ssm as ssm
)
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v27 import KubectlV27Layer

def create_eks_ckuser(scope, vpc): 
        kubectl_layer = KubectlV27Layer(scope, "KubectlLayer")
        cluster = eks.Cluster(
            scope, "MyEksCluster",
            vpc=vpc,
            version=eks.KubernetesVersion.V1_27,
            default_capacity=1,  # uses t3.small by default
            kubectl_layer=kubectl_layer  # required
        )
        # Store cluster name in SSM Parameter Store
        cluster_name = ssm.StringParameter(scope, "EksClusterNameParam",
            parameter_name="/config/cdk_demo/eks/cluster_name",
            string_value=cluster.cluster_name
        )

        # Store cluster endpoint in SSM Parameter Store
        cluster_endpoint = ssm.StringParameter(scope, "EksClusterEndpointParam",
            parameter_name="/config/cdk_demo/eks/cluster_endpoint",
            string_value=cluster.cluster_endpoint
        )

        return cluster
