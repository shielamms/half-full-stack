---
layout: post
title: A Serverless web scraper on AWS Lambda
slug: serverless-web-scraper-on-aws-lambda
date:   2021-08-29 22:44:38 +0100
categories: [DataOps]
tags: [python, aws, serverless]
---

Suppose you want to get information from a website regularly and want to do that automatically on the cloud with as little configuration as possible. First, you'll need to write a web scraper (or spider), then have that scraper be run by a scheduler on some cloud provider.

In this project, I've chosen to use Python to write the scraper and AWS as the cloud provider. There are several ways to deploy functions through code, like terraform or docker. I chose Serverless because it's the quickest to set up and write. Here's how the project looks like in concept:

<!-- <img src="{{site.baseurl}}/assets/images/serverless-scraper.png"> -->
![Full-width image]({{site.baseurl}}/assets/images/serverless-scraper.png){:.lead loading="lazy"}
<!-- Caption
{:.figcaption} -->

The webpage I chose to scrape is this [**IMDB page containing a list of movies**](https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm){:target="_blank"}.

I've written a simple Python-based scraper to collect certain information from each movie on the list. The Serverless configuration file specifies the resources that need to be created in AWS for the scraper to work. The Lambda function will run every midnight of the first day of each month through an EventBridge schedule, and upload the scraped data as JSON into an S3 bucket.

---

## The Code
You can checkout the complete code in [this Github repository](https://github.com/shielamms/lambda-functions/tree/master/01-serverless-scraper){:target="_blank"}.

### Pre-requisites
1. Python 3.7 environment

    If you're a Mac user, you would already have a Python 3 interpreter by default (use `python3` command instead of `python`). If your Python version does not match the needed version for this project, you can switch Python versions using an environment manager like Pyenv (`brew install pyenv`) or Anaconda.

2. AWS account and AWS CLI setup
    - to create an AWS account, [refer to this page](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html){:target="_blank"}.
    - to set up AWS CLI on your machine, [refer to this page](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html){:target="_blank"}

3. Serverless

    The quickest way to install Serverless is through `npm`. [Installation steps here](https://www.serverless.com/framework/docs/getting-started){:target="_blank"}.


<br />

---
---

# Code Walkthrough

## 1. The Scraper


`BeautifulSoup` is a lightweight Python library to help us traverse HTML trees easily.
This library is often used hand-in-hand with the `requests` library.
```python
# file: "imdb_scraper.py"
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

I've created a class to represent the scraper, called `IMDBScraper`. This class will contain 1) the URL of the webpage we'll scrape, 2) a variable to store the "soup" from `BeautifulSoup`, 3) and the output (which is initially empty).

```python
# file: "imdb_scraper.py"
class IMDBScraper():
    _start_url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
    _soup = None
    _output = []
```

The `scrape` function will look for all list items under the element with `class=movies`, and get the title, url, and rating of each item. Each movie is added as a JSON object to the the `output`.

```python
# file: "imdb_scraper.py"
def scrape(self):
    response = requests.get(self._start_url)
    self._soup = BeautifulSoup(response.content)
    movies = self._soup.select('.movies li')

    for movie in movies:
        # get details
        title = movie.select_one('.titleColumn > a').text
        url = movie.select_one('.titleColumn > a').get('href')
        rating = movie.select_one('.imdbRating').text

        self.output.append({
            'title': title,
            'url': url,
            'rating': rating,
        })

    return self._output
```

The last step for the scraper is to upload the output to the S3 bucket, like this:

```python
# file: "imdb_scraper.py"
import boto3

def upload_to_s3(self, data, bucket_name, key):
    s3 = boto3.client('s3')
    s3.upload_file(data, bucket_name, key)
```

Since the script will be deployed to AWS Lambda, we'll need a handler function to serve as the entrypoint to the service. This function is defined outside of the `IMDBScraper` class.

```python
# file: "imdb_scraper.py"
import datetime

def handler(event, args):
    scraper = IMDBScraper()
    data = {'movies': scraper.scrape()}
    today = datetime.date.today().strftime('%Y-%m-%d')

    scraper.upload_to_s3(data, event.get('bucket_name'), key=today)
```

The handler function needs `event` and `args` parameters, as required by AWS Lambda. `event` contains the parameters that the function trigger (in this case, the trigger is EventBridge) passes to the function. The EventBridge trigger contains a `bucket_name` parameter (which is defined in Serverless, see section below).

The complete `imdb_scraper.py` is found [**here**](https://github.com/shielamms/lambda-functions/blob/master/post-deploy-scraper-to-lambda/imdb_scraper.py){:target="_blank"}.

<br />

---

## 2. Serverless Configuration

To deploy the function to AWS via Serverless, we only need a YAML file where we can declare the provider, the function, and its associated resources.

These are the three resources that need to be created in AWS in conjunction with the scraper function:
1. **An S3 bucket** - so, this one I prefer to create manually through the AWS Console than through Serverless, since I could accidentally delete data with one serverless command. I named my S3 bucket `imdb-data`.
2. **IAM permissions** (to be created by Serverless) - to allow the Lambda Function to access the S3 bucket and send logs to CloudWatch
3. **EventBridge Rule** (to be created by Serverless) - to trigger the Lambda function according to a schedule we specify

#### 2.1: __Declaring the service__
I've created a file named `serverless.yml` in the same directory as the Python file. We declare the service name at the beginning of **`serverless.yml`**. I also wanted to add the bucket name as a custom variable which can be referenced multiple times in the rest of the configuration later.

```yml
# file: "serverless.yml"
service: imdb-scraper
custom:
  bucketName: imdb-data
```

Serverless supports deployments to cloud providers like Google Cloud, AWS, and Azure. Since we're deploying the function on AWS Lambda, the provider name is `aws`. The `stage` attribute specifies which environment to deploy on. Since I'm only running the code for development, I've used `dev`. If you're ready to deploy to a production account, then use `prod`.

```yml
# file: "serverless.yml"
provider:
  name: aws
  stage: dev
```

#### 2.2: __IAM permissions__
The IAM permissions that will be assigned to the Lambda function are declared within the `provider` attribute, like this

```yml
provider:
  name: aws
  stage: dev
  iam:
    role:
      name: ${sls:stage}-${self:service}
      statements:
        ...
```

To reference attributes or variables declared within the serverless configuration file, we use the `${}` notation. For example, to reference `stage`, we use `${sls:stage}`, and to reference `service`, we use `${self:service}`. The `role.name` attribute of above code snippet just concatenates the two values with a `-`.

Next, we specify the IAM permissions that the Lambda function will have. The syntax is similar to how IAM statements are written. It's in this format:

```yml
  ...
      statements:
        - Effect: ''
          Action: ''
            - '<action 1>'
            - '<action 2>'
          Resource: ''
  ...
```

In this project, we want the Lambda Function to have access to our S3 bucket, so we add `Get` and `Put` permissions. Remember that we declared a custom variable earlier with the name of the S3 bucket. To reference that, we use `${self:custom.bucketName}`. The `iam` attribute now looks like this:

```yml
# file: "serverless.yml"
  iam:
    role:
      name: ${sls:stage}-${self:service}
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

#### 2.3: __Declaring the Lambda Function__
The Lambda Function is declared inside the `functions` attribute. Here we can specify Lambda function settings like the handler, runtime, and timeout values. Refer to the [Serverless documentation](https://www.serverless.com/framework/docs/providers/aws/guide/functions){:target="_blank"} for more attribute details.

```yml
# file: "serverless.yml"
functions:
  imbd_scraper:
    handler: imbd_scraper.handler
    name: ${sls:stage}-${self:service}-function
    description: Scrape movies from IMDB website
    runtime: python3.7
    timeout: 15
    memorySize: 128
```

#### 2.4: __EventBridge Schedule__
Within the `functions` block, we can declare `events`, which are a list of triggers that will execute the Lambda Function. I prefer using cron expressions to specify schedules. AWS accepts the 6-digit cron format.
In this case, I want to trigger the function every midnight on the 1st of every month: `cron(0 0 1 * ? *)`

```yml
# file: "serverless.yml"
    events:
      - eventBridge:
          # cron: min,hour,dayofmonth,month,dayofweek,year
          schedule: cron(0 0 1 * ? *)
          input:
            environment: ${sls:stage}
            bucket_name: ${self:custom.bucketName}
```

The `input` attribute lets us pass parameters from EventBridge to the Lambda function. In this case, the `environment` and `bucket_name` are sent to the Lambda function (Serverless converts these to a JSON string for us).

---

## Scaling to multiple scrapers
In more complex scenarios, more often you'd need multiple scrapers for multiple web sources. Each scraper might have its own class. Intuitively, more scrapers might mean more Lambda functions. But instead, you can create separate EventBridge schedules for each scraper, and each can trigger the same Lambda Function. Just add a parameter in your EventBridge trigger to specify which scraper to run.

For example, suppose we have an IMDB webpage scraper that will run every midnight of the 1st of the month, and a Netflix page scraper at 2am of the 2nd of the month. We declare them as separate EventBridge events with the scraper name as a parameter to pass to the same Lambda Function.

```yml
# file: "serverless.yml"
    ...
    events:
      - eventBridge: # Schedule for IMDBScraper
          schedule: cron(0 0 1 * ? *)
          input:
            scraper_name: IMDBScraper
      - eventBridge: # Schedule for NetflixScraper
          schedule: cron(0 2 2 * ? *)
          input:
            scraper_name: NetflixScraper
```

Then in the Lambda Function, get the scraper name from the `event` argument.

```python
# file: "scraper.py"
class IMDBScraper():
  ...

class NetflixScraper():
  ...

def handler(event, args):
  scrapers = {
    'IMDBScraper': IMDBScraper,
    'NetflixScraper': NetflixScraper,
  }

  scraper_to_run = event.get('scraper_name')
  scraper = scraper_to_run()
  data = {'movies': scraper.scrape()}
  ...

```


#### Check out this repository for the complete code:
[Lambda Functions](https://github.com/shielamms/lambda-functions/tree/master/01-serverless-scraper){:target="_blank"}.
