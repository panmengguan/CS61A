"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples, testmod
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait, message
from string import ascii_letters
from ucb import main, trace, interact, log_current_line

#run_docstring_examples(extract_words, globals(), True)

# Phase 1: The Feelings in Tweets

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.

    text      -- A string; the text of the tweet, all in lowercase
    time      -- A datetime object; the time that the tweet was posted
    latitude  -- A number; the latitude of the tweet's location
    longitude -- A number; the longitude of the tweet's location

    >>> t = make_tweet("Just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['Just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_words(tweet):
    """Return a list of the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return extract_words(tweet['text'])


def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    "*** YOUR CODE HERE ***"

    return tweet['time'];
    
def tweet_location(tweet):
    """Return a position (see geo.py) that represents the tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet['latitude'], tweet['longitude']);
    
def tweet_string(tweet):
    """Return a string representing the tweet."""
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('adsgj@($.jjoa^#$&@mmxp***@#*')
    ['adsgj', 'jjoa', 'mmxp']
    """
    "*** YOUR CODE HERE ***"
    
    i = 0 #counter
    new_list = list(text) #creates a copy of text
    return_list = []
    new_word = ""
    for each_letter in new_list:
        i += 1
        if i == len(new_list) and each_letter in ascii_letters:
            new_word += each_letter
            return_list += [str(new_word)]
        elif each_letter not in ascii_letters:
            if new_word != "":
                return_list += [str(new_word)]
            new_word = ""        
        elif (each_letter == ' ') :
            return_list += [str(new_word)]
            new_word = ""
        else:
            new_word += each_letter

    return return_list

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> s = make_sentiment(0.2)
    >>> t = make_sentiment(None)
    >>> has_sentiment(s)
    True
    >>> has_sentiment(t)
    False
    >>> sentiment_value(s)
    0.2
    >>> z = make_sentiment(0)
    >>> has_sentiment(z)
    True
    >>> sentiment_value(z)
    0
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    "*** YOUR CODE HERE ***"
    return value

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    return s != None

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return make_sentiment(s)

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word, if word is not in the sentiment dictionary.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    return make_sentiment(word_sentiments.get(word, None))

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("Thinking, 'I hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment((negative)))
    -0.25
    >>> no_sentiment = make_tweet("Go bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    >>> even = make_tweet("no no big big no@big%@39udas_pew", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(even))
    True
    >>> sentiment_value(analyze_tweet_sentiment(even))
    0.0
    """
    average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    sentiment_list = []
    words = tweet_words(tweet)
    total, count = 0,0
    for each_word in words:  #In each word, find total sentiment and number of words
        if has_sentiment(get_word_sentiment(each_word)) == True:
            total += sentiment_value(get_word_sentiment(each_word))
            count += 1
    if count == 0: #If there is no count, then the sentiment is Nuetral, or None
        return make_sentiment(None)
    else: #Else takes the average of the sentiments for words
        average = make_sentiment(total/count)
        return average


# Phase 2: The Geometry of Maps

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, return its first position as its centroid

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p2, p1])
    (1, 2, 0)
    >>> p1, p2, p3 = make_position(28, 34), make_position(130, 28), make_position(38, -43)
    >>> triangle = [p1, p2, p3, p1]
    >>> find_centroid(triangle)
    (65.33333333333333, 6.333333333333333, 3897.0) #Don't worry if your values are a little (<0.001) off here
    >>> p1, p2, p3, p4 = make_position(0, 0), make_position(0, 10), make_position(10, 10), make_position(10, 0)
    >>> find_centroid([p1, p2, p3, p4, p1])
    (5.0, 5.0, 100.0)
    """
    "*** YOUR CODE HERE ***"
    #begin code
    poly_len = len(polygon)-1
    """area, c_lat, c_long = 0, 0, 0 
    first_count = 0 #counter
    while first_count < len(polygon)-1:
        lat_i = latitude(polygon[first_count])
        lat_i2 = latitude(polygon[first_count+1])
        long_i = longitude(polygon[first_count])
        long_i2 = longitude(polygon[first_count+1])
        area += 0.5*((lat_i*long_i2)-(lat_i2*long_i))
        first_count += 1
    second_count = 0 #resetting counter for next iteration
    if area == 0:
        return latitude(polygon[0]) , longitude(polygon[0]) , 0
    while second_count < len(polygon)-1:
        lat_i = latitude(polygon[second_count])
        lat_i2 = latitude(polygon[second_count+1])
        long_i = longitude(polygon[second_count])
        long_i2 = longitude(polygon[second_count+1])        
        c_lat += ((long_i2 *lat_i- long_i*lat_i2)*(lat_i + lat_i2))/(6*area)                 
        c_long += ((long_i + long_i2)*(lat_i*long_i2 - lat_i2 * long_i))\
                  /(6*area)
        second_count += 1
    return (c_lat), (c_long), abs(area)"""
    """poly_len = len(polygon)-1 #Number of points in the polygon list

    #finds the sum of general function to make the center latitude and
    #center longitude
    area, c_lat, c_long = 0,0,0
    counter = 0
    while counter < poly_len:
        lat_i = latitude(polygon[counter])
        lat_i2 = latitude(polygon[counter+1])
        long_i = longitude(polygon[counter])
        long_i2 = longitude(polygon[counter+1])
        area += (0.5)*((lat_i*long_i2)-(lat_i2*long_i))
        if area == 0 and :
            return latitude(polygon[0]) , longitude(polygon[0]) , 0
        c_lat += ((long_i2 *lat_i- long_i*lat_i2)*(lat_i + lat_i2))                
        c_long += ((long_i + long_i2)*(lat_i*long_i2 - lat_i2 * long_i))
        counter += 1
    return c_lat/(6*area), c_long/(6*area), abs(area)

    #try 3"""
    #finds the area of the polygon
    def poly_area(x=0):
        area = 0
        while x < len(polygon)-1:
            area+=(0.5)*(latitude(polygon[x])*longitude(polygon[x+1])-\
                   (latitude(polygon[x+1])*longitude(polygon[x])))
            x+=1
        return area
    new_area = poly_area()
    
    #states that if area of polygon is 0, returns initial position
    if new_area == 0:
        return latitude(polygon[0]), longitude(polygon[0]), 0
    
    #finds the central latitude
    def cent_latitude(x = 0):
        cent_lat = 0
        while x < len(polygon)-1:
            cent_lat += (latitude(polygon[x])+latitude(polygon[x+1]))*\
                         (latitude(polygon[x])*longitude(polygon[x+1])-\
                          latitude(polygon[x+1])*longitude(polygon[x]))
            x+=1
        return (cent_lat)/(6*new_area)
    
    #finds the central longitude
    def cent_longitude(x = 0):
        cent_long = 0
        while x < len(polygon)-1:
            cent_long += (longitude(polygon[x])+longitude(polygon[x+1]))*\
                         (latitude(polygon[x])*longitude(polygon[x+1])-\
                          latitude(polygon[x+1])*longitude(polygon[x]))
            x+=1
        return (cent_long)/(6*new_area)
    
    return cent_latitude(), cent_longitude(), abs(new_area)

def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    >>> a = find_center(us_states['TX'])
    >>> round(latitude(a), 5)
    31.49517
    >>> round(longitude(a), 5)
    -99.35787
    >>> b = find_center(us_states['NY'])
    >>> round(latitude(b), 5)
    42.94336
    >>> round(longitude(b), 5)
    -75.50111
    >>> c = find_center(us_states['NJ'])
    >>> round(latitude(c), 5)
    40.19284
    >>> round(longitude(c), 5)
    -74.66187
    >>> d = find_center(us_states['MS'])
    >>> round(latitude(d), 5)
    32.7498
    >>> round(longitude(d), 5)
    -89.6635
    >>> e = find_center(us_states['ME'])
    >>> round(latitude(e), 5)
    45.37857
    >>> round(longitude(e), 5)
    -69.23245
    >>> f = find_center(us_states['OH'])
    >>> round(latitude(f), 5)
    40.29607
    >>> round(longitude(f), 5)
    -82.78821
    """
    "*** YOUR CODE HERE ***"
    area_sum, sum_x, sum_y = 0, 0, 0
    for shape in polygons:  #iterates between all the shapes in list
        spec_centroid = find_centroid(shape)
        area = spec_centroid[2]
        area_sum += spec_centroid[2]
        sum_x += spec_centroid[0]*area  #adds latitude of centroid * prev area
        sum_y += spec_centroid[1]*area  #adds longitude of centroid * prev area
    gen_center_x = sum_x/area_sum  #finds general center of latitudes
    gen_center_y = sum_y/area_sum  #finds general center of longitudes
    return make_position(gen_center_x, gen_center_y)


# Phase 3: The Mood of the Nation

def find_closest_state(tweet, state_centers):
    """Return the name of the state closest to the given tweet's location.

    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.

    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.

    >>> us_centers = {n: find_center(s) for n, s in us_states.items()}
    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> find_closest_state(sf, us_centers)
    'CA'
    >>> find_closest_state(ny, us_centers)
    'NJ'
    >>> a = make_tweet("", None, 20, -100)
    >>> find_closest_state(a, us_centers)
    'TX'
    >>> b = make_tweet("", None, 30, -120)
    >>> find_closest_state(b, us_centers)
    'CA'
    >>> c = make_tweet("", None, 37, -90)
    >>> find_closest_state(c, us_centers)
    'MO'
    """
    "*** YOUR CODE HERE ***"
    pos1 = tweet_location(tweet) #first position
    dist_list = {} #dictionary of distances
    state = ""
    for each_center in state_centers:  #iterates through centers of states
        distance = geo_distance(pos1, state_centers[each_center])
        dist_list[each_center] = distance  #orders distance of tweet with centers
    for state_key in dist_list: #iterates through keys in distance dictionary
        if distance > dist_list[state_key]:
            distance = dist_list[state_key]
            state = state_key
    return state

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> ca_tweets = group_tweets_by_state([sf, ny])['CA']
    >>> tweet_string(ca_tweets[0])
    '"Welcome to San Francisco" @ (38, -122)'


    #In tweets_by_state['MO'], if you put this doctest into your trends.py file, it should work correctly. If you just read it on Piazza, there'll be double-slashes (\\) on Piazza but not in the Python output. Don't worry about that.
    >>> tweets = load_tweets(make_tweet, 'obama')
    >>> tweets_by_state = group_tweets_by_state(tweets)
    >>> tweets_by_state['MO']
    [{'latitude': 37.17454213, 'text': 'obama: "we will not forget you." // the nation hasn\\'t, but obama must have \\'slept since then.\\'  or gone golfing. #joplin #fema', 'longitude': -95.10078354, 'time': datetime.datetime(2011, 8, 28, 18, 47, 46)}, {'latitude': 37.17454213, 'text': 'obama: "we will not forget you." // the nation hasn\\'t, but obama must have \\'slept since then.\\'  or gone golfing. #joplin #fema', 'longitude': -95.10078354, 'time': datetime.datetime(2011, 8, 28, 18, 47, 46)}, {'latitude': 39.05533081, 'text': 'obama uncle got arrested ! lmao', 'longitude': -94.57681917, 'time': datetime.datetime(2011, 8, 30, 11, 16, 13)}, {'latitude': 38.924711, 'text': 'cnn ipad notification pops up "president obama requests joint" that\\'s all i read. ended with "session of congress" it was cool for a second.', 'longitude': -94.500465, 'time': datetime.datetime(2011, 8, 31, 16, 26, 41)}, {'latitude': 38.44219, 'text': 'rt @ancientproverbs: insanity is doing the same thing in the same way & expecting a different outcome. -chinese proverbslisten up obama!', 'longitude': -90.3041, 'time': datetime.datetime(2011, 8, 29, 12, 57, 57)}, {'latitude': 39.305996, 'text': 'dream ?: better president...dubya, or obama? #gopdebate', 'longitude': -94.47124039, 'time': datetime.datetime(2011, 9, 8, 16, 40, 16)}, {'latitude': 36.84158628, 'text': 'ok, obama say sumthing smart, impress me.', 'longitude': -93.63118948, 'time': datetime.datetime(2011, 9, 8, 23, 8, 20)}, {'latitude': 39.03867236, 'text': "'all jews, pack up your things and head to your nearest train station.' - barack obama", 'longitude': -94.58384525, 'time': datetime.datetime(2011, 9, 8, 23, 20, 7)}, {'latitude': 38.78630813, 'text': 'great message by obama. now, back it up! #standmotv8d', 'longitude': -90.67543365, 'time': datetime.datetime(2011, 9, 8, 23, 42, 32)}, {'latitude': 38.57640134, 'text': 'pass this jobs bill .... pass this jobs bill.... in my obama vc*', 'longitude': -90.40396075, 'time': datetime.datetime(2011, 9, 8, 23, 44, 41)}, {'latitude': 38.9098151, 'text': "good thing that's over.. don't get in the way of football, obama. that would not make you popular to americans..", 'longitude': -94.6897306, 'time': datetime.datetime(2011, 9, 8, 23, 56, 4)}, {'latitude': 37.17959, 'text': "all i hear when obama talks is blah blah blah. he's the poster child for a presidential epic fail #2012hurrypleasehurry", 'longitude': -89.65636, 'time': datetime.datetime(2011, 9, 9, 12, 6, 44)}, {'latitude': 38.66376835, 'text': '@wsj i know obama is studying this!!!', 'longitude': -92.11143839, 'time': datetime.datetime(2011, 9, 2, 20, 24, 50)}]
    >>> len(tweets_by_state['MO'])
    13
    """
    tweets_by_state = {}
    
    "*** YOUR CODE HERE ***"
    us_centers = {n: find_center(s) for n, s in us_states.items()} #Lists states
    for tweet in tweets: #In each tweet find the closest state to group by
        location = find_closest_state(tweet,us_centers)
        if location in tweets_by_state:
            tweets_by_state[location] += [tweet,]
        else:
            tweets_by_state[location] = [tweet,]

    return tweets_by_state
 
        
        
 

def most_talkative_state(term):
    """Return the state that has the largest number of tweets containing term.

    >>> most_talkative_state('texas')
    'TX'
    >>> most_talkative_state('sandwich')
    'NJ'
    >>> most_talkative_state('math')
    'CA'
    >>> most_talkative_state('ham')
    'OH'
    >>> most_talkative_state('democrat')
    'CA'
    >>> most_talkative_state('republican')
    'WA'
    >>> most_talkative_state('glee')
    'CA'
    >>> most_talkative_state('python')
    'CA'
    >>> most_talkative_state('internet')
    'TX'
    >>> most_talkative_state('ramen')
    'CA'
    >>> most_talkative_state('dreary')
    'NJ'
    >>> most_talkative_state('taxes')
    'NJ'
    >>> most_talkative_state('bad')
    'NJ'
    >>> most_talkative_state('hate')
    'NJ'
    >>> most_talkative_state('tears')
    'NJ'
    >>> most_talkative_state('despair')
    'NJ'
    >>> most_talkative_state('die')
    'NJ'
    """
    tweets = load_tweets(make_tweet, term)  # A list of tweets containing term
    "*** YOUR CODE HERE ***"
    state_counter = {}
    count = 0
    tweet_state_l = group_tweets_by_state(tweets)
    for state in tweet_state_l: # Start iteration for tweets in order
        for tweet in tweet_state_l[state]: #counts number of times term comes up
                if term in tweet_words(tweet):
                    count += 1
        state_counter[state] = count
        count = 0
    most_state_tweet = None
    for state_key in state_counter:
        if most_state_tweet == None:
            most_state_tweet = state_counter[state_key]
            state = state_key
        elif state_counter[state_key] > most_state_tweet:
            most_state_tweet = state_counter[state_key]
            state = state_key

    return state
                
def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets

    >>> tweets = load_tweets(make_tweet, 'love')
    >>> tweets_by_state = group_tweets_by_state(tweets)
    >>> avg=average_sentiments(tweets_by_state)
    >>> avg['CA']
    0.2718685610502868
    >>> avg['TX']
    0.2813076222933947
    >>> avg['MO']
    0.2693714788462128
    >>> avg['OH']
    0.26372411067254053
    >>> avg['DC']
    0.28004002474214695
    >>> avg['NY']
    0.2780108339632151
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    #starts iteration that averages sentiments by state
    for each_state in tweets_by_state:
        if len(each_state) != 0:
            sentiment_counter, total_sentiment =  0, 0

            for each_tweet_in_state in tweets_by_state[each_state]:
                
                sentiment = analyze_tweet_sentiment(each_tweet_in_state)
                if sentiment != None:
                    total_sentiment += sentiment
                    sentiment_counter += 1
                
            if sentiment_counter != 0:
                averaged_state_sentiments[each_state] = total_sentiment/sentiment_counter
                
    return averaged_state_sentiments


    
# Phase 4: Into the Fourth Dimension

def group_tweets_by_hour(tweets):
    """Return a dictionary that groups tweets by the hour they were posted.

    The keys of the returned dictionary are the integers 0 through 23.

    The values are lists of tweets, where tweets_by_hour[i] is the list of all
    tweets that were posted between hour i and hour i + 1. Hour 0 refers to
    midnight, while hour 23 refers to 11:00PM.

    To get started, read the Python Library documentation for datetime objects:
    http://docs.python.org/py3k/library/datetime.html#datetime.datetime

    >>> tweets = load_tweets(make_tweet, 'party')
    >>> tweets_by_hour = group_tweets_by_hour(tweets)
    >>> for hour in [0, 5, 9, 17, 23]:
    ...     current_tweets = tweets_by_hour.get(hour, [])
    ...     tweets_by_state = group_tweets_by_state(current_tweets)
    ...     state_sentiments = average_sentiments(tweets_by_state)
    ...     print('HOUR:', hour)
    ...     for state in ['CA', 'FL', 'DC', 'MO', 'NY']:
    ...         if state in state_sentiments.keys():
    ...             print(state, ":", state_sentiments[state])
    HOUR: 0
    CA : 0.08333333333333334
    FL : -0.09635416666666666
    DC : 0.017361111111111115
    MO : -0.11979166666666666
    NY : -0.15
    HOUR: 5
    CA : 0.00944733796296296
    FL : -0.06510416666666667
    DC : 0.0390625
    MO : 0.1875
    NY : -0.046875
    HOUR: 9
    CA : 0.10416666666666667
    NY : 0.25
    HOUR: 17
    CA : 0.09807900432900431
    FL : 0.0875
    MO : -0.1875
    NY : 0.14583333333333331
    HOUR: 23
    CA : -0.10729166666666666
    FL : 0.016666666666666663
    DC : -0.3
    MO : -0.0625
    NY : 0.21875

    tweets -- A list of tweets to be grouped
    """
    tweets_by_hour = {}
    "*** YOUR CODE HERE ***"
    for each_tweet in tweets:
        hour = tweet_time(each_tweet).hour #Get the hour of each tweet
        if hour not in tweets_by_hour: #if not already correlated, correlate tweet by hour
            tweets_by_hour[hour] = [each_tweet,]
        else:
            tweets_by_hour[hour] += [each_tweet,] #add another if already correlated
    return tweets_by_hour


# Interaction.  You don't need to read this section of the program.

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    assert words, 'No words extracted from "' + text + '"'
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in extract_words(text.lower()):
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments={}):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_term(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()
    
def draw_map_by_hour(term='my job', pause=0.5):
    """Draw the sentiment map for tweets that match term, for each hour."""
    tweets = load_tweets(make_tweet, term)
    tweets_by_hour = group_tweets_by_hour(tweets)

    for hour in range(24):
        current_tweets = tweets_by_hour.get(hour, [])
        tweets_by_state = group_tweets_by_state(current_tweets)
        state_sentiments = average_sentiments(tweets_by_state)
        draw_state_sentiments(state_sentiments)
        message("{0:02}:00-{0:02}:59".format(hour))
        wait(pause)

def run_doctests(names):
    """Run verbose doctests for all functions in space-separated names."""
    g = globals()
    errors = []
    for name in names.split():
        if name not in g:
            print("No function named " + name)
        else:
            if run_docstring_examples(g[name], g, True) is not None:
                errors.append(name)
    if len(errors) == 0:
        print("Test passed.")
    else:
        print("Error(s) found in: " + ', '.join(errors))

@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--run_doctests', '-t', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_term', '-m', action='store_true')
    parser.add_argument('--draw_map_by_hour', '-b', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))
