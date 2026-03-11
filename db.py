import boto3

AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
AWS_REGION = "ap-south-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

users_table = dynamodb.Table("users")
bookings_table = dynamodb.Table("bookings")
reviews_table = dynamodb.Table("reviews")
