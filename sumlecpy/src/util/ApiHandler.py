import openai
import time
import math

base = 4

def call_api(func, *args, **kwargs):
    success = False
    output = None
    num_retries = 0
    while not success:
        try:
            output = func(*args, **kwargs)
            success = True
        except openai.error.APIError as e:
            print("API call failed, retrying...") 
            print("error msg: {}".format(e))
            time.sleep(0.5 * math.pow(base, num_retries))
            num_retries += 1
        except (openai.error.APIConnectionError, openai.error.TryAgain, openai.error.Timeout) as e:
            print("API connection failed, retrying...") 
            print("error msg: {}".format(e))
            time.sleep(0.5 * math.pow(base, num_retries))
            num_retries += 1
        except openai.error.RateLimitError as e:
            print("Rate limit exceeded, retrying...") 
            print("error msg: {}".format(e))
            time.sleep(0.5 * math.pow(base, num_retries))
            num_retries += 1
    return output