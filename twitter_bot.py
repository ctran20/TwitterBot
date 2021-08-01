import tweepy
import time


def main():
    # Authentication
    auth = tweepy.OAuthHandler('')
    auth.set_access_token('')
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, timeout=30)

    while True:
        follow_back(api)
        unfollow(api)
        time.sleep(400)


def follow_back(api):
    following = api.friends_ids(api.me().id)
    followers = tweepy.Cursor(api.followers).items()
    for follower in followers:
        if follower.id in following:
            print(f'Already followed {follower.screen_name}')
        else:
            follower.follow()
            tweets = api.user_timeline(user_id=follower.id, count=5)
            print(f'Follow {follower.screen_name}')
            for tweet in tweets:
                try:
                    tweet.favorite()
                    print("Liked")
                    time.sleep(0.5)
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break


def unfollow(api):
    follower = api.followers_ids(api.me().id)
    followings = tweepy.Cursor(api.friends).items()
    for following in followings:
        if not following.id in follower:
            api.destroy_friendship(following.id)
            tweets = api.user_timeline(user_id=following.id, count=5)
            print(f'Unfollow {following.screen_name}')
            for tweet in tweets:
                try:
                    api.destroy_favorite(tweet.id)
                    print("Unliked")
                    time.sleep(0.5)
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break


if __name__ == "__main__":
    main()