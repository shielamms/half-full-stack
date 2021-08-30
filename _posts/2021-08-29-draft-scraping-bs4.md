---
layout: post
title: Scraping with requests and BeautifulSoup
date:   2021-08-29 22:44:38 +0100
categories: data-collection python
---

_Check out the `code` branch of this repository for the complete Python code._

Suppose you have a project that requires data that can only be found on the internet. For example, you want to analyse tweets about a certain topic, or get a list of the top movies that people watch. So you go to your browser, open up the websites that contain all the information that you need, but you can't possibly copy and paste hundreds of thousands of data points into your spreadsheet or database. It's not practical nor scalable.

Web scraping tools help automate the extraction of data from websites. There are dozens of libraries in Python for web scraping, but we'll take a look at one of the most popular ones (and probably the easiest to learn) - BeautifulSoup.


## What is BeautifulSoup?
`BeautifulSoup` is basically a Python library that extracts data from HTML, XML, or other markup languages. It's usually used hand-in-hand with the `requests` library, which retrieves the webpage from a given URL. Webpages contain HTML code, and HTML is a tree structure that can be navigated algorithmically. Consider the following example:

{% highlight html %}
<html>
    <div id="div_A" class="class_A">
        <p>Hello world!</p>
    </div>
    <div id="div_B" class="class_A">
        <p>
            <a href="www.abcd.com">This is a link!</a>
        </p>
    </div>
</html>
{% endhighlight %}

Suppose you want to write a program to get the text contents of the `<a>` tag from the HTML code above. To get to that tag and get its text content, your program would traverse the following:
1. `<html>`
2. `<div id="div_B" class="class_A">`
3. `<p>`
4. `<a href="www.abcd.com">` # <-- Found the tag!
5. `This is a link!` # <-- Extract this text

This whole traversal of the HTML tree is abstracted for us by BeautifulSoup, so you'll only need to tell it roughly **where to look**, and **what data you want to extract**. If we were to use `BeautifulSoup` to do the traversal above, and suppose the html code is stored in a variable called `html_content`, it would be as simple as the following two lines of code:

{% highlight python %}
soup = BeautifulSoup(html_content)
text = soup.select_one('#div_B a').text
{% endhighlight %}

In this case, `.select_one('#div_B a')` tells `BeautifulSoup` to look for the `<a>` tag within `#div_B` (*where to look*), and `.text` tells it to extract that text within the tag (*what data you want to extract*).

Let's take a look at a simple scraping project to understand this better. In this post, we'll scrape the [the IMDB Top Rated Movies webpage](https://www.imdb.com/chart/top/?ref_=nv_mv_250) for a list of top-rated movies. We'll also employ classes and functions instead of writing a plain-vanilla Python script, so our code is more extensible and (close to being) production-ready.


## Scraping Project
### Installation
For this project, we'll install two libraries: `bs4` and `requests`.
```
pip install bs4 requests
```

### Analysing the website
Null

### Object-oriented approach
First we'll represent one movie in the list as a `Movie` object, so we'll create a `Movie` class. In this example, we only want to get three attributes of a movie: the title, its IMDB rating, and its short description.
{% highlight python linenos %}
class Movie:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.imdb_rating = kwargs.get('imdb_rating')
        self.description = kwargs.get('description')

    def output_dict(self):
        return {
            'title': self.title,
            'imdb_rating': self.imdb_rating,
            'description': self.description,
        }
{% endhighlight %}
I also added the function `output_dict()` so that we can represent `Movie` in a dictionary format.

Then, we can think of the scraper as an object in itself. Let's name the object `IMDBScraper` and initialize it with the some properties.

{% highlight python linenos %}
class IMDBScraper:
    def __init__(self, start_url, params=None):
        self.start_url = start_url
        self.params = params
        self.soup = None
        self.output = []
{% endhighlight %}

- `start_url` : the url of the IMDB Top Movies webpage
- `params` : the params part of the url
- `soup` : the BeautifulSoup object containing the 

