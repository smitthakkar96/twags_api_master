from flask import *
from documents import *
import unicodedata
from settings import *
import tweepy

app = Flask(__name__)

@app.route('/signup',methods=['POST'])
def signup():
    if request.json["name"] is not None and request.json["email"] is not None and request.json["interests"] is not None:
        interest_list = request.json["interests"]
        for i in interest_list:
            try:
                g = globalInterests()
                g.text = i
                g.save()
            except Exception as e:
                print "already exits"
        u  = user()
        u.name = request.json["name"]
        u.email = request.json["email"]
        u.interests = request.json["interests"]
        u.save()
        return str(u.id)
    else:
        abort(400)

@app.route('/getposts',methods=['GET'])
def getposts():
    objectId = request.args.get('objectId')
    _users = user.objects(id=objectId)
    interests = []
    for u in _users:
         interests = u.interests
         break
    dict = []
    _tweets = tweets.objects(tag__in=interests)
    for t in _tweets:
        temp={}
        for key in t:
            if key == "id" or key == "createdAt":
                temp[key] = str(t[key])
            else:
                temp[key] = unicodedata.normalize('NFKD', t[key]).encode('ascii','ignore')
        dict.append(temp)
    return json.dumps(dict)

@app.route('/getpostsbygeo',methods=['GET'])
def byGeo():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    geo_str = lat + "," + lon + ",5km"
    print geo_str
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    dict=[]
    for t in tweepy.Cursor(api.search,geocode=geo_str).items(20):
        temp={}
        text = t.text.lower()
        print text
        name = t.user.name
        profilepicture_url = t.user.profile_image_url
        createdAt = t._json["created_at"]
        temp["text"] = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        temp["by_name"]=name
        temp["by_profilepicture"]=profilepicture_url
        temp["createdAt"] = createdAt
        dict.append(temp)
    return json.dumps(dict)

app.run(host="0.0.0.0",debug=True)
