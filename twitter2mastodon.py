import tweepy
from mastodon import Mastodon
import twcreds
import macreds

def crosspost():
    # Set up Mastodon connection
    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        api_base_url = 'https://lgbt.io'
    )

    mastodon.log_in(
        macreds.username,
        macreds.password,
        to_file = 'pytooter_usercred.secret'
    )

    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        access_token = 'pytooter_usercred.secret',
        api_base_url = macreds.base_url
    )

    # Set up Twitter connection
    auth = tweepy.OAuthHandler(twcreds.consumer_key, twcreds.consumer_secret)
    auth.set_access_token(twcreds.access_token, twcreds.access_token_secret)
    api = tweepy.API(auth)

    # Set up files
    idfile = "twcache.txt"
    idfromfile = open(idfile, 'r')
    lastid = idfromfile.read()
    #print("Last status ID read from file: " + laststatus)

    # Get tweets since last status recorded in idfile
    try:
        status = api.user_timeline(since_id=lastid, count=20, )
    except:
        status = api.user_timeline(count=20)

    # Loop through tweets
    for i in reversed(status):
        # Toot
        if (i.in_reply_to_user_id == 53925971 or not i.in_reply_to_user_id) and i.is_quote_status == False and i.retweeted == False:
            mastodon.toot(i.text)
            #print(i.text)
        
        # Update idfile with ID of last successfully tooted tweet
        lastid = i.id
        idtofile = open(idfile, 'w')
        idtofile.write(str(lastid))
        idtofile.close()

crosspost()