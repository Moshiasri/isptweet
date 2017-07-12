"""
[isptweet]

Tweet @ your ISP whenever your internet speed is below what you pay for.
"""

import os              # for reading environment variables
from sys import argv   # for parsing command-line arguments
from sys import exit   # for exiting the program on fatal errors
import speedtest       # for testing internet speed
import twitter         # for tweeting at your ISPs
from time import sleep # for setting a delay between retesting

SPEED_MARGIN_OF_ERROR = 3 # the margin in which your internet can be slower than you pay for
RETEST_DELAY = 60 * 60    # delay until retesting

# read in down/up speeds
try:
    isp = argv[1]
    expected_down = float(argv[2])
    expected_up = float(argv[3])
    try:
        RETEST_DELAY = float(argv[4])
    except IndexError:
        pass
except TypeError:
    print("[isptweet]: Fatal Error: Unable to convert speeds to numbers.")
    exit()
except IndexError:
    print("Usage: isptweet @ISPTWITTER DOWN UP [DELAY]")
    exit()

# read API tokens from environment variables
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# check if any API values are not set => are of type NoneType
if None in [consumer_key, consumer_secret, access_token, access_token_secret]:
    print('[isptweet]: Fatal Error: Please ensure that CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_TOKEN_SECRET are set correctly for your target Twitter account.')
    exit()

# initialize Twitter API with these variables
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)

def main():
    print("[isptweet]: Initialized.")
    s = speedtest.Speedtest()
    while True:
        
        # whether to tweet your up and/or down speeds
        tweet_down = False
        tweet_up = False
        
        # get the server to upload to/download from
        # to test speed
        s.get_best_server()
        
        print("[isptweet]: Testing speeds...")
        
        # get speeds and convert to Mpbs
        actual_down = s.download() / (1000 ** 2)
        actual_up = s.upload() / (1000 ** 2)
        
        print("[isptweet]: Results: {down} down/{up} up".format(down=actual_down, up=actual_up))
        
        # compare to promised speeds
        if (expected_down - SPEED_MARGIN_OF_ERROR > actual_down):
            tweet_down = True
        
        if (expected_up - SPEED_MARGIN_OF_ERROR > actual_up):
            tweet_up = True

        tweet_text = None # the body of the message to send
        if tweet_down and tweet_up:
            tweet_text = '{isp} my internet speed is {actual_down} down {actual_up} up; but I pay for {expected_down} down {expected_up} up!'.format(isp = isp,
                                                                                                                                                     actual_down = actual_down,
                                                                                                                                                     actual_up = actual_up,
                                                                                                                                                     expected_down = expected_down,
                                                                                                                                                     expected_up = expected_up)


        elif tweet_down:
            tweet_text = '{isp} my internet speed is {actual_down} down; but I pay for {expected_down} down!'.format(isp=isp,
                                                                                                                     actual_down = actual_down,
                                                                                                                     expected_down = expected_down)

            
        elif tweet_up:
            tweet_text = '{isp} my internet speed is {actual_up} up; but I pay for {expected_up} up!'.format(isp=isp,
                                                                                                             actual_up=actual_up,
                                                                                                             expected_up=expected_up)
        
        if tweet_text:
            status = api.PostUpdate(tweet_text)
            print("[isptweet]: Just posted '{tweet_body}'.".format(tweet_body=status.text))
            
        print("[isptweet]: Sleeping for {delay} seconds...".format(delay=RETEST_DELAY))
        sleep(RETEST_DELAY)

if __name__ == '__main__':
    print("[isptweet]: Initializing...")
    main()
    
