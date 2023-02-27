---
layout: post
title: End-to-end data pipeline with dbt, BigQuery, and Streamlit
slug: e2e-google-trends-dbt-bq-streamlit
date: 2022-10-08 16:10:00 +0100
categories: [data-engineering]
tags: [dbt, bigquery, streamlit, python]
---

This article demonstrates a data pipeline from data transformations in BigQuery using dbt, to quickly displaying the data in a web application using Streamlit. I've chosen the Google Trends dataset in BigQuery's public datasets for this project - specifically transforming data from the `international_top_terms` table. This is a mini-simulation of a data warehouse project using a modern data stack.

## Overview
<!-- <img src="{{site.baseurl}}/assets/images/serverless-scraper.png"> -->
![Full-width image]({{site.baseurl}}/assets/images/my-dbt-project-setup.png){:.lead loading="lazy"}
<!-- Caption
{:.figcaption} -->