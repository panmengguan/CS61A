def group_tweets_by_state(tweet, state_centers):
    tweets_by_state = {}
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    for elem in tweet:
        dist = {}
        for state in us_centers:
            distance = geo_distance(find_center(elem), state)
            dist[state]
        
        tweets_by_state[state] = distance

def most_talkative_state(term):
    state_talk = {}
    tweets = load_tweets(make_tweet, term)
    places = group_tweets_by_state(tweets)
    for states in places:
        for tweets in states:
            if term in tweet_words(tweets):
                state_talk[state] = 
    
    
