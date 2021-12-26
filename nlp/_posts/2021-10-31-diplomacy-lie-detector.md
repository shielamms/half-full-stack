---
layout: post
title: Detecting lies from messages in Diplomacy - an evil game of deception
slug: diplomacy-lie-classifier
date:   2021-10-31 22:22:00 +0000
categories: [NLP]
tags: [python, data-cleaning, tfidf, classifiers, smote]
---

Working at a remote-first company, we had to find some team-building activities that we could do online. Playing Diplomacy was not one of them.

Diplomacy is a board game of 7 players representing 7 nations at war in the early 20th century: Turkey, Russia, Austria, Italy, Germany, France, and England. To win the game, one must take over 18 "supply centres" (cities) in the map of Europe, by engaging in private "diplomatic" conversations with each other. You can pretty much say anything you want - offer your allegiance, promise to be neutral, suggest a win-win deal, promise to support an attack - and then choose to do the exact opposite. So now you know how the game can spark lots of backstabbing, bitterness, and outrage - the perfect office situtation, right?

## Treasure Dataset found!
So in my spare time contemplating about the most recent backstabbing and lies in the game, I found an interesting and very timely dataset online: a collection of Diplomacy games and conversations! _Perfect, just perfect_, I thought to my self with an evil grin on my face.

You can find the dataset here:
[Diplomacy: A Dataset for Deception Detection](https://sites.google.com/view/qanta/projects/diplomacy)

### Data Format
The link above gives us three files - train.jsonl, validate.jsonl, and test.jsonl. Each file contains a bunch of JSON objects, each representing an entire game dialog. You can check the data source link above for the metainfo about each feature in the dataset. It's interesting, though, that these games have annotations for whether a message is a truth or a lie.

A game looks like this:

```json
{
    "messages": [
        "Heya there, just dropping in to say hello",
        "Hey turkey. Our paths probably won't cross for a while l, but may I suggest you attack Russia? I've seen way to many games where Russia is ignored and all of the sudden they have half the board. Anyways, good lucks and have fun!",
        "Thanks! I'll definitely see what I can do, a big Russia is just as bad for me as everyone else",
        "Sweet!",
        "I was talking with Russia, negotiating over Norway and such. They told me they were planning on attacking you, as they thought I was there ally. The truth is, I really don't want to see russia run off with this game, so I decided to let you know.",
        "Thanks for the heads up"],
    "sender_labels": [true, true, false, true, false, true],
    "receiver_labels": [true, true, true, true, true, true],
    "speakers": ["turkey", "england", "turkey", "england", "england", "turkey"],
    "receivers": ["england", "turkey", "england", "turkey", "turkey", "england"],
    "absolute_message_index": [5, 9, 27, 28, 1157, 1188],
    "relative_message_index": [0, 1, 2, 3, 4, 5],
    "seasons": ["Spring", "Spring", "Spring", "Spring", "Fall", "Winter"],
    "years": ["1901", "1901", "1901", "1901", "1902", "1902"],
    "game_score": ["3", "3", "3", "3", "5", "4"],
    "game_score_delta": ["0", "0", "0", "0", "1", "0"],
    "players": ["england", "turkey"],
    "game_id": 9
}
```


So there's lots of things we could possibly build out of this dataset. But the first thing that came to my mind (and probably the easiest to implement) was finding out if there is a way to detect lies in Diplomacy messages by training a model with just the `messages` (feature) and the `sender_labels` (label). Simple enough, so we can discard the rest of the data - or reserve it for some other project. (Watch out for Part 2 of this post?)


## Lie detection as an NLP problem
There's a few challenges with this dataset:
1. The label `sender_labels` has only two values: True or False (truth or lie). This asserts that each message sent by a player is intri either definitely true or definitely false. But in reality,


## Cleaning the messages

## Vectorization

## Training an algorithm to detect lies - and failing

## Why is it so hard to trust anyone in this game??

## The Object-oriented approach
