#-- Import modules
from __future__ import print_function
import sys
import os.path
import json
import boto3
from cloud_formation_stack import CloudFormationStack
import aws_config as ac
import shutil


def upload_to_s3(s3_resource, s3_client, bucket, prefix, file):
    s3_key = prefix +'/'+ file
    s3_resource.meta.client.upload_file(file, bucket, s3_key)
    return s3_key


def replace_package_path(template, bucket, package):
    f = open(template,)
    data = json.load(f)
    data["Resources"]["SendNotificatioinLambda"]["Properties"]["Code"]["S3Bucket"] = bucket
    data["Resources"]["SendNotificatioinLambda"]["Properties"]["Code"]["S3Key"] = package
    json_object = json.dumps(data, indent = 4)
    with open(template, "w") as outfile:
        outfile.write(json_object)


def deploy():
    region         = ac.REGION
    stack_name     = ac.STACK_NAME
    aws_access_key = ac.ACCESS_KEY
    aws_secret_key = ac.SECRET_KEY
    template       = ac.CF_TEMPLATE
    bucket         = ac.BUCKET_NAME
    prefix         = ac.BUCKET_PREFEIX

    s3_client              = boto3.resource('s3', region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    s3_resource            = boto3.resource('s3', region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    cloud_formation_client = boto3.client('cloudformation', region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    shutil.make_archive("notification", "zip", "notification_sender")
    package = "notification.zip"
    print("Building Package.")
    s3_key = upload_to_s3(s3_resource, s3_client, bucket, prefix, package)
    replace_package_path(template, bucket, s3_key)

    template_s3_key =upload_to_s3(s3_resource, s3_client, bucket, prefix, template)
    template_url ="https://s3-%s.amazonaws.com/%s/%s" % (region, bucket, template_s3_key)

    cfs = CloudFormationStack(cloud_formation_client, stack_name)
    if cfs.exists():
        cfs.delete()
    response = cfs.create(template_url)
    print("======"*20)
    print("======"*20)
    print("Successfully Deployed the service. You can access it using below link:")
    print("\n")
    print(cfs.deploy_url())
    print("======"*20)
    print("======"*20)

if __name__ == "__main__":
    deploy()
