import boto3

AWS_REGION = "ap-south-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

users_table = dynamodb.Table("users")
bookings_table = dynamodb.Table("bookings")
reviews_table = dynamodb.Table("reviews")

