# # import sched, time
# # import connect
# # from settings import *
# # from documents import *
# # import sentiments
# # import tweepy
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# api = tweepy.API(auth)
#
# s = sched.scheduler(time.time,time.sleep)
# max_id = None
#
# def fillmymongo():
#     try:
#             print "started"
#             interests = globalInterests.objects()
#             for i in interests:
#                 print "fetching " + i.text
#                 for page in tweepy.Cursor(api.search, q=i.text,max_id=i.max_id).pages(2):
#                     for item in page:
#                         print item.text
#                         print item.id
#                         max_id = item.id
#                 i.max_id = str(max_id)
#                 i.save()
#     except:
#         print "error"
#     s.enter(1,1,fillmymongo,())
#     s.run()
# fillmymongo()
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from settings import *
import connect
from documents import *
import json
import timestring

allinterests = []
interests = globalInterests.objects()
for i in interests:
    print i.text
    allinterests.append(str(i.text))

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            d = json.loads(data)
            print d
            text = d["text"].lower()
            name = d["user"]["name"]
            profilepicture_url = d["user"]["profile_image_url"]
            createdAt = d["created_at"]
            tags = ""
            for ai in allinterests:
                if ai in text:
                    tags = ai
                    break
            tweet = tweets()
            tweet.tag = tags
            tweet.text = d["text"]
            tweet.createdAt = timestring.Date(createdAt).date
            tweet.by_name = name
            tweet.by_profilepicture = profilepicture_url
            tweet.save()
        except Exception as e:
            print str(e)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    print allinterests
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=allinterests)
