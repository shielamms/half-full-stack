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

In this project, I've chosen to use Python to write the scraper and AWS as the cloud provider. There are three common ways to deploy functions through code: Terraform, Ansible, or Serverless. I chose Serverless because it's the quickest to set up and write.

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

In this project, we'll write a scraper in Python to collect certain information from each movie on the list. We'll then write a Serverless configuration file to specify the resources that need to be created in AWS for the scraper to work. When we run serverless, it will deploy the scraper into AWS Lambda and create those resources we specified in AWS. The Lambda function will run every midnight of the first day of each month through an EventBridge schedule, and upload the scraped data as JSON into an S3 bucket.


### What resources are we going to create in AWS?
1. **An S3 bucket** - so, this one I prefer to create manually through the AWS Console than through Serverless, since I could accidentally delete data with one serverless command. I named my S3 bucket `imdb-data`.
2. **IAM permissions** (to be created by Serverless) - to allow the Lambda Function to access the S3 bucket and send logs to CloudWatch
3. **EventBridge Rule** (to be created by Serverless) - to trigger the Lambda function according to a schedule we specify

<br />
Alright, let's start!

---

<br />

## The Scraper


`BeautifulSoup` is a lightweight Python library to help us traverse HTML trees easily.
This library is often used hand-in-hand with the `requests` library.
```python
from bs4 import BeautifulSoup
import requests
```

To use `BeautifulSoup` with `requests`, we do something like this:
```python
response = requests.get("www.sample-website-to-scrape1234.com")
soup = BeautifulSoup(response.content)
```

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
    _output = []
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
    
    return self._output
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
    data = {'movies': scraper.scrape()}
    today = datetime.date.today().strftime('%Y-%m-%d')

    scraper.upload_to_s3(data, event.get('bucket_name'), key=today)
```

The handler function needs `event` and `args` parameters, as required by AWS Lambda. `event` contains the parameters that the function trigger passes along to the function itself. In this case, we're expecting a `bucket_name` attribute to be passed as a parameter from EventBridge (which we'll see later in Serverless). We then upload data into the S3 bucket with the name in `bucket_name`.

The complete `imdb_scraper.py` is found **here**.

<br /><br />

---

<br />

## Serverless Configuration

To deploy the function to AWS via Serverless, we only need a YAML file where we can declare the provider, the function, and its associated resources.

I've created a file named `serverless.yml` in the same directory as the Python file. We declare the service name at the beginning of **`serverless.yml`**. I also wanted to add the bucket name as a custom variable which can be referenced multiple times in the rest of the configuration later.

```yml
service: imdb-scraper
custom:
  bucketName: imdb-data
```

We declare the provider next. Serverless supports deployments to cloud providers like Google Cloud, AWS, and Azure. Since we're deploying the function on AWS Lambda, we'll declare the provider name as `aws`. The `stage` attribute specifies which environment to deploy on. Since I'm only running the code for development, I'll use `dev`. If you're ready to deploy to a production account, then use `prod`.

```yml
provider:
  name: aws
  stage: dev
```

<br />

### __IAM permissions__
To declare the IAM permissions, use the `iam` attribute within the `provider` block, like this:

```yml
    iam:
      role:
        name: ${sls:stage}-${self:service}
        statements:
          ...
```

In the beginning of the file, we declared the attributes `stage` and `service`. To reference these attributes, we use the `${}` notation. To reference `stage`, we use `${sls:stage}`, and to reference `service`, we use `${self:service}`. The `role.name` attribute of above code snippet just concatenates the two values with a `-`.

Next, we specify the IAM permissions that the Lambda function will have. The syntax is similar to how IAM statements are written. It's in this format:

```yml
    statements:
      - Effect: ''
        Action: ''
          - '<action 1>'
          - '<action 2>'
        Resource: ''
```

In our project, we want the Lambda Function to have access to our S3 bucket, so we add `Get` and `Put` permissions. Remember that we declared a custom variable earlier with the name of the S3 bucket. To reference that, we use `${self:custom.bucketName}`

```yml
        statements:
          - Effect: 'Allow'
            Action:
              - 's3:GetObject'
              - 's3:PutObject'
            Resource: 'arn:aws:s3:::${self:custom.bucketName}/*'
```

In addition, if you want Lambda logs and metrics to be sent to CloudWatch, you can add these statements:

```yml
- Effect: 'Allow'
            Action:
              - 'cloudwatch:PutMetricData'
              - 'logs:CreateLogGroup'
              - 'logs:PutLogEvents'
            Resource: '*'
```

<br />

### __Declaring the Lambda Function__
To declare the Lambda function, we use the Serverless `function` attribute in our configuration. Here we can specify Lambda function settings like the handler, runtime, and timeout values. Refer to the [Serverless documentation](https://www.serverless.com/framework/docs/providers/aws/guide/functions) for more attribute details.

```yml
functions:
  imbd_scraper:
    handler: imbd_scraper.handler
    name: ${sls:stage}-${self:service}-function
    description: Scrape movies from IMDB website
    runtime: python3.7
    timeout: 15
    memorySize: 128
```

<br />

### __EventBridge Schedule__
Within the `function` block, we can declare `events`, which are a list of triggers that will execute the Lambda Function. In our case, we want to trigger the function through an EventBridge rule (Every midnight on the 1st of the month).
We'll use a 6-digit cron expression to specify the schedule: `cron(0 0 1 * ? *)`, which means every 00:00 on the 1st day of the month.

```yml
    events:
      - eventBridge:
          # cron: min,hour,dayofmonth,month,dayofweek,year
          schedule: cron(0 0 1 * ? *)
          input:
            environment: ${sls:stage}
            bucket_name: ${self:custom.bucketName}
```

The `input` attribute lets us pass parameters from EventBridge to the Lambda function. In this case, we send the `environment` and `bucket_name` to the Lambda function (Serverless converts these to a JSON string for us).