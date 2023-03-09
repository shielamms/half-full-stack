---
layout: post
title: "Cache what you scrape: implementing a caching strategy for scraping projects"
slug: cache-what-you-scrape
date:   2023-03-08 13:00:00 +0100
categories: [python-tips]
tags: [python, scraping, caching]
---

Scraping websites can be a lot of fun and quite easy to do once you've gotten the hang of extracting data from html trees. But as you scrape more data and more complicated websites for production use, you may find yourself exhausting your machine's memory or even making unnecessarily repetitive HTTP requests.

Tracking changes to the data from target websites for scraping can be tricky, especially if you just won't know when the data is going to change. This could result to your scraper failing once it sees some unexpected input it cannot handle, so that any data held in memory during the scrape gets flushed out once the error occurs. In any scraping project, it's a good practice to implement some caching strategy while anticipating changes to your source website.

A "cache", in this case, can be any form of storage - a file, a database, an object bucket, etc. Document-based NoSQL databases are a popular option, as each scraped item can easily be represented as a document, and reading/writing data doesn't need to follow any relational constraints. For this example, we'll use MongoDB as our cache storage.

## Sample scraper: IMDB Top Ranked Movies

Let's say you've implemented a scraper class to scrape top movies data from the IMDB website. You're using the BeautifulSoup library to extract the title and rating of each movie on the list. You'll probably have something like this:

```python
import requests
from bs4 import BeautifulSoup

class IMDBScraper():
    _start_url = "https://www.imdb.com/chart/top/"
    _soup = None
    _output = []
    
    def _extract_movie_details(self, item):
        title = item.select_one('.titleColumn a').text
        rating = item.select_one('.imdbRating strong').text

        return {
            'title': title,
            'rating': rating,
        }

    def scrape(self):
        response = requests.get(self._start_url)
        self._soup = BeautifulSoup(response.content)
        items = self._soup.select('.lister-list tr')

        for item in items:
            self._output.append(self._extract_movie_details(item))
        return self._output
```

The scraper has two functions: `scrape()`, which is the entrypoint for making the http request to the webpage, and then stores the response as a soup of html. It then selects a table element and loops through each of its rows; `_extract_movie_details()` extracts the title and rating from each row and returns a dictionary format of the extracted data.

To run the scraper, just instantiate a new `IMDBScraper` object, and call the `scrape()` function.

```python
scraper = IMDBScraper()
scraper.scrape()
```

This will output a list of json objects consisting of movie titles and ratings:

```
[{'title': 'The Shawshank Redemption',
  'rating': '9.2'},
 {'title': 'The Godfather',
  'rating': '9.2'},
  ...
]
```

Your application can now access the data returned by the scraper. But, what if the application needs to access the data multiple times? Calling the `scrape()` function again would trigger another http call to the target website. In some cases where the application is rather small and the data does not need to be up-to-date, this is ok. But more complicated scraping projects would often involve larger volumes of data that may be too big for your allocated memory, and some would even involve scraping with multiple paginations (i.e., several http calls in succession). This is where a caching strategy comes into play.

---

## A caching strategy

As you scrape more data from websites, you'll soon need a way to persist the data to avoid exhausting your machine's memory or even performing unnecessary re-scraping of data that you know would not even change. You can use any form of storage depending on your data requirements - this can be a file, an object storage, or a database. In this example, we'll use MongoDB, a popular document-based NoSQL database, to cache the data scraped by our IMDB Scraper. At a high level, the solution would look like this:

![Scraper cache]({{site.baseurl}}/assets/images/scraper-cache.png){: width="500" loading="lazy" style="margin-left: 1em; margin-bottom: 1em"}


### Spin up a MongoDB server

If you already have a MongoDB server, that's great! - you can just take note of the address and port from which you can access it. If you don't have a MongoDB server and would like to try out this caching strategy yourself, you can spin up a MongoDB container through Docker:

Pull the latest mongo image from dockerhub:
```
docker pull mongo
```

Then run a mongo container:
```
docker run -r -p 27017:27017 mongo
```

Then you can test your connection to your MongoDB container through the `pymongo` library in Python:

```python
from pymongo import MongoClient

# If you have a non-local mongodb server, replace 'localhost' with your db address
client = MongoClient('localhost', 27017)
client.server_info()
```

This should print out your mongodb connection details if your connection is working normally.


### Use a wrapper function to cache the output of a function

Recall that our IMDB Scraper class has a `scrape()` function that we can call whenever we want to re-scrape data from a website. We'd want to just retain this function as it is, and just extend it with a caching functionality. Enter **decorators**! Basically, we'd want something like the code below, where the `scrape()` function's implementation is left untouched. We then just decorate it with a wrapper function that's arbitrarily called `cache_me()`, which takes in as a parameter an arbitrary name of the cache in which to store the output of the `scrape()` function.

```python
    @cache_me('imdb')
    def scrape(self):
        response = requests.get(self._start_url)
        self._soup = BeautifulSoup(response.content)
        items = self._soup.select('.lister-list tr')

        for item in items:
            self._output.append(self._extract_movie_details(item))
        return self._output
```

We can then implement the `cache_me()` wrapper function with our caching strategy - that is, saving the output of the `scrape()` function into a MongoDB collection. The `collection_name` parameter is the name of the mongodb collection in which to store the cached data (MongoDB generates this if the collection does not exist yet).


```python
from pymongo import MongoClient

def cache_me(collection_name):
    def wrapper(fn):
        def cache_to_mongo(self):

            client = MongoClient('localhost', 27017)
            coll = client['movies'][collection_name]
            data = list(coll.find())

            if data:
                print('Returning cached data...')
                return data
            else:
                print('Running the scrape function...')
                data = fn(self)
                
                if data:
                    coll.insert_many(data)
                else:
                    print('Unable to scrape data from url!')

            return data
            
        return cache_to_mongo   
    return wrapper

```

So if there's no data in the cache, running `scraper.scrape()` will output:

```
Running the scrape function...
```

But if there is data in the cache, running `scraper.scrape()` will output:

```
Returning cached data...
[{'_id': ObjectId('64091fa964b3b01f6eefc08a'),
  'title': 'The Shawshank Redemption',
  'rating': '9.2'},
 {'_id': ObjectId('64091fa964b3b01f6eefc08b'),
  'title': 'The Godfather',
  'rating': '9.2'},
  ...
  ...
]
```

The output is a list of json objects, each containing a `title`, `rating`, and a unique `_id` generated by mongo db.

---

## Adding a flag to fully refresh the cache

The `cache_me()` function currently returns the cached data (if it exists) and performs the scraping again if there is no cache. However, there may be cases when you'd need to fully empty the cache so that you can re-scrape the target website and store the new data. To do this, we can just add a parameter to the `scrape()` function to indicate whether we want to fully empty the cache or not before caching this newly scraped data.

Let's take a look at this version of `cache_me()`, where its inner function `cache_to_mongo()` now receives keyword arguments `**kwargs`. This allows us to pass any number of keyword arguments when calling the `scrape()` function - which is where we'll put in a keyword argument named `refresh_cache`. Setting this argument to `True` means that the currently cached data will be deleted and newly scraped data will be inserted into the cache. Setting it to `False` means that the function will return the cached data if it already exists.

```python
def cache_me(collection_name):
    def wrapper(fn):
        def cache_to_mongo(self, **kwargs):
            
            client = MongoClient('localhost', 27017)
            coll = client['movies'][collection_name]
            data = list(coll.find())
            
            refresh_cache = kwargs.get('refresh_cache')
            
            if data and not refresh_cache:
                print('Returning cached data...')
                return data
            else:
                print('Running the scrape function...')
                data = fn(self)
                
                if data:
                    # Make sure there is new data first before deleting the cache
                    print('Removing cached data...')
                    coll.delete_many({})
                    coll.insert_many(data)
                else:
                    print('Unable to scrape data from url!')
                
            return data
            
        return cache_to_mongo   
    return wrapper

```

We can then call the `scrape()` function with the `refresh_cache` parameter:

```python
scraper.scrape(refresh_cache=True)

```

This will output the following, indicating that the cache has been fully refreshed and new data has been inserted (the new values for `_id` reveal that they are new data):

```
Running the scrape function...
Removing cached data...
[{'title': 'The Shawshank Redemption',
  'rating': '9.2',
  '_id': ObjectId('640927cd64b3b01f6eefc188')},
 {'title': 'The Godfather',
  'rating': '9.2',
  '_id': ObjectId('640927cd64b3b01f6eefc189')},
  ...
  ...
]
```

---
