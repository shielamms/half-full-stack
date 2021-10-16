---
layout: post
title: Quickly deploy a scheduled scraper on AWS with Serverless
date:   2021-08-29 22:44:38 +0100
categories: data-collection ops
tags: python aws serverless
---
<img src="{{site.baseurl}}/assets/images/sample.jpg">

# Quickly deploy a scheduled scraper on AWS with Serverless

Suppose you want to get information from a website regularly (maybe daily) and want to do that automatically on the cloud with as little configuration as possible. First, you'll need to write a web scraper (or spider), then have that scraper be run by a scheduler on some cloud provider.

In this project, I've chosen to use Python to write the scraper, AWS as the cloud provider, and Serverless to deploy the needed infrastructure and resources for me.

## Pre-requisites
1. Python 3.7 environment

    [Download Python here](https://www.python.org/downloads/release/python-3712/)

2. AWS account and AWS CLI setup
    - to create an AWS account, [refer to this page](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
    - to set up AWS CLI on your machine, [refer to this page](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

3. Serverless

    The quickest way to install Serverless is through `npm`. [Installation steps here](https://www.serverless.com/framework/docs/getting-started).

## Code repository
Link to Github repo

<br />

---

## Project Summary
The webpage I chose to scrape is this **IMDB page containing a list of movies**. _Note that I **won't** discuss in this post what scraping is or how to inspect the HTML structure of the IMDB page. I'll assume you already know how to do that in your browser and already know HTML concepts like tags, ids, and classes._

In this project, we'll write a scraper in Python to collect certain information from each movie on the list. We'll then write a Serverless configuration file to specify the resources that need to be created in AWS for the scraper to work. When we run serverless, it will deploy the scraper into AWS Lambda and create those resources we specified in AWS. The Lambda function will run every 6am through an EventBridge schedule, and upload the scraped data as JSON into an S3 bucket.


### What resources are we going to create in AWS?
1. **An S3 bucket** - so, this one I prefer to create manually through the AWS Console than through Serverless, since I could accidentally delete data with one serverless command. I named my S3 bucket `imdb-data`.
2. **IAM permissions** (to be created by Serverless) - to allow the Lambda Function to access the S3 bucket and send logs to CloudWatch
3. **EventBridge Rule** (to be created by Serverless) - to trigger the Lambda function according to a schedule we specify

<br />
Alright, let's start!

---

## The Scraper
<br />

`BeautifulSoup` is a lightweight Python library to help us traverse HTML trees easily.
This library is often used hand-in-hand with the `requests` library.
```python
from bs4 import BeautifulSoup
import requests
```

To use `BeautifulSoup` with `requests`, we do something like this:
{% highlight python linenos %}
response = requests.get("www.sample-website-to-scrape1234.com")
soup = BeautifulSoup(response.content)
{% endhighlight %}

The `soup` variable will contain a sort of HTML tree that can be traversed to find a particular element in the page. For example, if we want to look for the element in the page with the `id="movieTitle"` inside an `<h2>` block, then we can do this:
```python
title = soup.select_one('h2 #movieTitle')
```
<br />

I'll create a class to represent the scraper, called `IMDBScraper`. We'll give it three properties: the URL of the webpage we'll scrape, a variable to store the "soup" from `BeautifulSoup`, and the output (which is initially empty).

<br />**`imdb_scraper.py`**

```python
class IMDBScraper():
    _start_url = "<put IMDB url here>"
    _soup = None
    output = []
```
We'll define a `scrape()` function in this class which we can call from the program's entrypoint later. This function will look for all list items under the element with `class=movies`, and get the title, url, description, and rating of each item.

```python 
def scrape(self):
    response = requests.get(self._start_url)
    self._soup = BeautifulSoup(response.content)
    movies = self._soup.select('.movies li')
    
    for movie in movies:
        # get details
        title = movie.select_one('.title')
        url = movie.select_one('.titleLink')
        description = movie.select_one('.description')
        rating = movie.select_one('.rating')

        self.output.append({
            'title': title,
            'url': url,
            'description': description,
            'rating': rating,
        })
```

Each movie is added as a JSON object to the the `output` list variable.
The last step for the scraper is to create a function to upload the output to the S3 bucket.

```python
import boto3

def upload_to_s3(self, data, bucket_name, key):
    s3 = boto3.client('s3')
    s3.upload_file(data, bucket_name, key)
```

Since we're deploying this to AWS Lambda, we'll need a handler function to serve as the entrypoint to the service. This function will be outside of the `IMDBScraper` class.

```python
import datetime

def handler(event, args):
    scraper = IMDBScraper()
    scraper.scrape()
    data = {'movies': scraper.output}
    today = datetime.date.today().strftime('%Y-%m-%d')

    scraper.upload_to_s3(data, event.get('bucket_name'), key=today)
```
The complete `imdb_scraper.py` is found **here**.

<br /><br />

---

## Serverless Configuration