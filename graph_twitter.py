import argparse,json, os, sys, time, tweepy
from datetime import datetime


consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR SECRET TOKEN"
def twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    #twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret)
    print(">>> Date : %s" % str(datetime.now()))
    try:
        api = tweepy.API(auth)
        print(">>> Authentication to %s 's account." % consumer_key)
        return api 
    except:
        print(">>> Error Twitter Authentication.")
        sys.exit(0)


def get_friends(user_screenname):
    api = twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret)
    friends_name = []
    for user in api.friends_ids(user_screenname):
        friends_name.append(user)
    return friends_name

def compare_friends():
    individuals = []
    result_array = {}
    for filename in os.listdir('db'):
        if filename.endswith(".json"): 
            with open('db/' + filename) as f:
                for indiv in json.load(f):
                    individuals.append(indiv)

    every_single_individual = set(individuals)
    for individual in every_single_individual:
        result_array[individual] = individuals.count(individual)
    result_array = sorted(result_array.items(), key=lambda t: t[1],reverse=True)
    with open('most_wanted.json', 'w') as f:
        json.dump(result_array, f, indent=4)



def cross_twitter():
	try:
	    api = twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret)
	    with open('list_to_cross.json') as list_prospect:
	        array_prospects = json.load(list_prospect)
	        for individual_prospect in array_prospects:
	            if not os.path.exists('db/' + individual_prospect + '.json'):
	                individual_friends = get_friends(individual_prospect)
	                file_name ='db/%s_friends.json' % individual_prospect 
	                with open(file_name,"w+") as prospects_friends:
	                    prospects_friends.write(json.dumps(individual_friends))
	except tweepy.RateLimitError:
		print(">> Rate limit error , entering sleep mode.")
		time.sleep(60 * 15)
		cross_twitter()


def get_the_one():
    api = twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret)
    with open('most_wanted.json') as list_prospect:
        array_prospects = json.load(list_prospect)
        i = 0
        for prospect in array_prospects:
            if i < 20:
                user = api.get_user(prospect[0])   
                print("Screen name : %s - Followed by %s persons" % (user.screen_name,prospect[1]))
                i = i + 1



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Twitter friend lists crossing')
    parser.add_argument('--cross', action='store_true', help='Index friends list')
    parser.add_argument('--compare', action='store_true', help='Download friends profiles')
    parser.add_argument('--print', action='store_true', help='Compute common friends')

    args = parser.parse_args()
    try:
        if args.cross:
            api = cross_twitter()
        elif args.compare:
            compare_friends()
        elif args.print:
            get_the_one()
        else:
            api = cross_twitter()
            compare_friends()
            get_the_one()
    except KeyboardInterrupt:
        print('\nshow must go on.')
        pass
