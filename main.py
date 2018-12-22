import os
import tweepy
from dotenv import load_dotenv

load_dotenv(".env")


def list_split(n: int, list):
    return [list[i:i+n] for i in range(0, len(list), n)]


# 環境変数取得
ck = os.environ["ck"]
cs = os.environ["cs"]
tk = os.environ["tk"]
ts = os.environ["ts"]
list_name = os.environ["list"]

# 認証
auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(tk, ts)
api = tweepy.API(auth)

list_id = None

for x in api.lists_all():
    if x.name == list_name:
        list_id = x.id

list_members = set([x.id for x in tweepy.Cursor(
    api.list_members, list_id=list_id).items()])

friends = set(
    list(tweepy.Cursor(api.friends_ids, user_id=api.me().id).items()))

followers = set(
    list(tweepy.Cursor(api.followers_ids, user_id=api.me().id).items()))


targets = friends-followers-list_members

for xs in list_split(100, list(targets)):
    for x in api.lookup_users(user_ids=xs):
        print(x.name)
        print("@"+x.screen_name)
        print("https://twitter.com/"+x.screen_name)
        while True:
            print("l:add_list\nu:unfollow\ns:skip")
            cmd = input()
            if cmd == "l":
                api.add_list_member(list_id=list_id, user_id=x.id)
                break
            if cmd == "u":
                api.destroy_friendship(user_id=x.id)
                break
            if cmd == "s":
                break
        print("------------------------")
