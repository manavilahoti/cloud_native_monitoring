import os
from dotenv import load_dotenv
import boto3

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

ecr_client = boto3.client(
    "ecr",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,
)

repository_name = "devops-project"

try:
    response = ecr_client.create_repository(repositoryName=repository_name)
    repository_uri = response["repository"]["repositoryUri"]
    print(f"ECR Repository '{repository_name}' created successfully.")
    print(f"ECR Repository URI: {repository_uri}")
except ecr_client.exceptions.RepositoryAlreadyExistsException:
    print(f"ECR Repository '{repository_name}' already exists.")
except Exception as e:
    print(f"Error creating ECR Repository: {str(e)}")