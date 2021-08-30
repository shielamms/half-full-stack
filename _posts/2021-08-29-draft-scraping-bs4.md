---
layout: post
title: Scraping with requests and beautifulsoup
date:   2021-08-29 22:44:38 +0100
categories: data-collection python
---

_Check out the `code` branch of this repository for the complete Python code._

Suppose you have a project that requires data that can only be found on the internet. For example, you want to analyse tweets about a certain topic, or get a list of the top movies that people watch. So you go to your browser, open up the websites that contain all the information that you need, but you can't possibly copy and paste hundreds of thousands of data points into your spreadsheet or database. It's not practical nor scalable.

Web scraping tools help automate the extraction of data from websites. There are dozens of libraries in Python for web scraping, but we'll take a look at one of the most popular one (and probably the easiest to learn) - BeautifulSoup.


## What is `BeautifulSoup`?
`BeautifulSoup` is basically a Python library that extracts data from HTML, XML, or other markup languages. It's usually used hand-in-hand with the `requests` library, which retrieves the webpage from a given URL. Webpages contain HTML code, and HTML is a tree structure that can be navigated algorithmically. Consider the following example:

{% highlight html linenos %}
<html>
    <div id="div_A" class="class_A">
        <p>Hello world!</p>
    </div>
    <div id="div_B" class="class_A">
        <p><a href="www.abcd.com">This is a link!</a></p>
    </div>
</html>
{% endhighlight %}

Suppose you want to write a program to get the text contents of `div_B` from the HTML code above. First, your program will parse `<html>`, then look at its child elements - it finds two `<div>`s with the following ids: `div_A` and `div_B`. It then goes to the child elements of `div_B` - you find `<p>`, then `<a>`, then between `<a>` and `</a>`, you get the text `This is a link!`. This whole traversal of the HTML tree is abstracted for us by BeautifulSoup, so you'll only need to tell it roughly *where to look*, and *what data you want to extract*. If we were to use `BeautifulSoup` to do the traversal above, it would be as simple as the following two lines:

{% highlight python %}
    soup = BeautifulSoup(html_content)
    text = soup.select_one('#div_B').text
{% endhighlight %}

In this case, `.select_one('#div_B')` tells `BeautifulSoup` *where to look*, and `.text` tells it what data we want to extract.

Let's do a simple scraping project to understand this better. In this post, we'll scrape the [the IMDB Top Rated Movies webpage](https://www.imdb.com/chart/top/?ref_=nv_mv_250).


## Scraping Project
### Analysing the website
Null
