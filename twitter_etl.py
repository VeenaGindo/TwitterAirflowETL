import json
from datetime import datetime
import tweepy
import boto3
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
BEARER_TOKEN = "<YOUR_TWITTER_BEARER_TOKEN>"
S3_BUCKET_NAME = "<YOUR_S3_BUCKET_NAME>"
# ---------------------

def run_twitter_etl():
    # 1. Initialize Clients
    x_client = tweepy.Client(bearer_token=BEARER_TOKEN)
    s3_client = boto3.client('s3')
    
    target_username = "elonmusk"
    
    try:
        # 2. Get Elon Musk's numerical User ID
        print(f"Looking up User ID for @{target_username}...")
        user = x_client.get_user(username=target_username)
        if not user.data:
            print("Error: Could not find user account.")
            return
        user_id = user.data.id
        
        # 3. Paginate to fetch up to 200 tweets with public metrics
        print("Fetching up to 200 tweets with engagement metrics...")
        tweets_list = []
        
        for page in tweepy.Paginator(
            x_client.get_users_tweets,
            id=user_id,
            max_results=100,  # Max allowed per request page
            tweet_fields=['created_at', 'public_metrics'],  # Pulls timestamp and counts
            limit=2           # 2 pages * 100 = 200 total tweets
        ):
            if page.data:
                for tweet in page.data:
                    # Safely extract metrics dictionary
                    metrics = tweet.public_metrics if tweet.public_metrics else {}
                    
                    # Construct your exact custom JSON schema
                    tweets_list.append({
                        "user": target_username,
                        "text": tweet.text,
                        "favourite_count": metrics.get('like_count', 0),    # Mapping v2 like_count
                        "retweet_count": metrics.get('retweet_count', 0),
                        "created_at": tweet.created_at.strftime('%Y-%m-%dT%H:%M:%SZ') if tweet.created_at else None
                    })
        
        print(f"Successfully collected {len(tweets_list)} tweets.")
        
        if not tweets_list:
            print("No tweets found to upload.")
            return

        # 4. Format payload data
        payload = {
            "account": target_username,
            "extracted_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "total_tweets": len(tweets_list),
            "tweets": tweets_list
        }
        
        json_data = json.dumps(payload, indent=4)
        
        # Partitioning pattern for clean S3 directory structures
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        s3_key = f"twitter_ingestion/{target_username}/tweets_{timestamp}.json"
        
        # 5. Upload payload to S3
        print(f"Uploading payload to s3://{S3_BUCKET_NAME}/{s3_key}...")
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json_data,
            ContentType='application/json'
        )
        print("✅ Custom ingestion successfully completed!")

    except tweepy.errors.TweepyException as e:
        print(f"Twitter API Error: {e}")
    except ClientError as e:
        print(f"AWS S3 Error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

