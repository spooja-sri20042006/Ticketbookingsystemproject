import boto3

# ── AWS DynamoDB Configuration ──
AWS_ACCESS_KEY_ID     = 'YOUR_ACCESS_KEY_ID'      # Replace this
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'  # Replace this
AWS_REGION            = 'ap-south-1'              # Mumbai - India

# ── DynamoDB Connection ──
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

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