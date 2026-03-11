import boto3

AWS_REGION = "ap-southeast-2"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

users_table = dynamodb.Table("users")
bookings_table = dynamodb.Table("bookings")
reviews_table = dynamodb.Table("reviews")
# ── Tables ──
users_table    = dynamodb.Table('users')
bookings_table = dynamodb.Table('bookings')
reviews_table  = dynamodb.Table('reviews')

def create_tables():
    existing = [t.name for t in dynamodb.tables.all()]

    if 'users' not in existing:
        dynamodb.create_table(
            TableName='users',
            KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print("users table created!")

    if 'bookings' not in existing:
        dynamodb.create_table(
            TableName='bookings',
            KeySchema=[
                {'AttributeName': 'user_id',    'KeyType': 'HASH'},
                {'AttributeName': 'booking_id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id',    'AttributeType': 'S'},
                {'AttributeName': 'booking_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("bookings table created!")

    if 'reviews' not in existing:
        dynamodb.create_table(
            TableName='reviews',
            KeySchema=[{'AttributeName': 'review_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'review_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print("reviews table created!")

    print("All DynamoDB tables ready!")

