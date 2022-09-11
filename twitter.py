import os
import tweepy


def create_client():
    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']
    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    # try:
    #     client.get_me()
    #     print('Successful Authentication')
    # except Exception as e:
    #     print('Failed authentication')
    #     print(e)
    return client


def post_tweet(message):
    try:
        client = create_client()
        response = client.create_tweet(
            text=message)
    except Exception as e:
        print('Error trying to tweet!.')
        print(e)
    return response


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    api = create_client()
    r = post_tweet(api, "This is a test! :-)")
    print(r)
