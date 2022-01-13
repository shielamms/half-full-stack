---
layout: post
title: Bulk Import DNS records to Route53 with AWS Lambda
slug: bulk-import-dns-records-route53-lambda
date:   2021-12-05 12:00:30 +0100
categories: [dataops]
tags: [python, aws]
---

When migrating an on-premise DNS server to the cloud, particularly AWS, it's a common requirement to be able to move DNS data by bulk rather than adding records one by one. Unfortunately, the Amazon Route53 Console does not have a native data file uploader. Instead, we can use a Lambda function to read the DNS records from a file in S3 and upload the records into Route53 using the AWS CLI.

![Full-width image]({{site.baseurl}}/assets/images/bulk-route53-import.png){: loading="lazy" width="600"}

---

## The Code
You can checkout the complete code in Github: **[lambda-functions/02-route53-bulk-import](https://github.com/shielamms/lambda-functions/tree/master/02-route53-bulk-import){:target="_blank"}**.




---

## Quick background about DNS records

DNS records are instructions to servers that tell information on how to route requests for a particular domain. For example, a website with the domain name `www.this-sample-site.com` is hosted in a server within Company ABC. For people on the internet to be able to access `www.this-sample-site.com`, Company ABC has to provide the records of the website to other servers on the internet. These are DNS records that contain the domain name and IP address, as well as other useful text information, of the server in Company ABC.

So, a domain name can have several DNS records of different types (each type serves a particular purpose). The common types of records are A, AAAA, NS, MX, and TXT records. DNS servers group records by domain name to quickly access information once they get a request to a domain name.

---
---

# Code Walkthrough

From a high-level perspective, there will be four main steps (functions):
(1) reading the CSV file from S3;
(2) Grouping records from the file by domain name;
(3) ...

## Input format

## Reading the file from S3

## Grouping DNS records by domain name


##
