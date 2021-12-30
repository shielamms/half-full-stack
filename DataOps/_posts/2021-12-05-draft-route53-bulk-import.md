---
layout: post
title: Bulk Import DNS records to Route53 with AWS Lambda
slug: bulk-import-dns-records-route53-lambda
date:   2021-12-05 12:00:30 +0100
categories: [DataOps]
tags: [python, aws]
---

When migrating an on-premise DNS server to the cloud, particularly AWS, it's
a common requirement to be able to move DNS data by bulk rather than adding
records one by one. Unfortunately, the Amazon Route53 Console does not have a
native data file uploader. Instead, we can use a Lambda function
to read the DNS records from a file (records from the on-premise server)
and upload the records into Route53 using the AWS CLI.
