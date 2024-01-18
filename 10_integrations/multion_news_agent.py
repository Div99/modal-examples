# ---
# lambda-test: false
# ---
# # Twitter News Agent

# In this example, we use Modal to deploy a cron job that periodically checks for cool AI news everyday and tweets it on Twitter using the MultiOn Agent API.

# ## Import and define the stub
#
# Let's start off with imports, and defining a Modal stub.

import os
from datetime import datetime, timedelta

import modal

stub = modal.Stub("ai-news-tweet-agent")

# ## Searching for AI News
#


# Let's also define an image that has the `multion` package installed, so we can query the API.

multion_image = modal.Image.debian_slim().pip_install("multion")

# We can now define our main entrypoint, that uses [MultiOn](https://www.multion.ai/) to scrape AI news everyday and post it on our twitter account. We specify a [schedule](/docs/guide/cron) in the function decorator, which  
# means that our function will run automatically at the given interval.

# ## Setup MultiOn
# MultiOn is a nex-gen Web Action Agent that can take actions on behalf of the user. You can watch it in action here: [Youtube demo](https://www.youtube.com/watch?v=Rm67ry6bogw)
# The MultiOn API enables building the next level of web automation & custom AI agents capable of performing complex actions on the internet with just a few lines of code.

# To get started, first created an account with [MultiOn](https://app.www.multion.ai/), install the [MultiOn chrome extension](https://chrome.google.com/webstore/detail/ddmjhdbknfidiopmbaceghhhbgbpenmm) and login to your Twitter account in your browser.

@stub.function(image=multion_image, secret=modal.Secret.from_name("MULTION_API_KEY"))
def news_tweet_agent():
    # Import MultiOn
    import multion

    # Login to MultiOn using the API key
    multion.login(use_api=True, multion_api_key=os.environ["MULTION_API_KEY"])

    # Enable the Agent to run locally
    multion.set_remote(False)

    params = {
        "url": "https://www.multion.ai",
        "cmd": "Go to twitter (im already signed in). Search for the last tweets i made (check the last 10 tweets). Remember them so then you can go a search for super interesting AI news. Search the news on up to 3 different sources. If you see that the source has not really interesting AI news or i already made a tweet about that, then go to a different one. When you finish the research, go and make a few small and interesting AI tweets with the info you gathered. Make sure the tweet is small but informative and interesting for AI enthusiasts. Don't do more than 5 tweets",
        "maxSteps": 100,
    }

    response = multion.browse(params)

    print(f"MultiOn response: {response}")


# ## Test running
#
# We can now test run our scheduled function as follows: `modal run news_tweet.py::stub.news_tweet_agent`

# ## Defining the schedule and deploying
#
# Let's define a function that will be called by Modal every day


# runs at 9 am (UTC) every day
@stub.function(schedule=modal.Cron("0 9 * * *"))
def run_daily():
    news_tweet_agent.remote()


# In order to deploy this as a persistent cron job, you can run `modal deploy news_tweet.py`,

# Once the job is deployed, visit the [apps page](/apps) page to see
# its execution history, logs and other stats.
