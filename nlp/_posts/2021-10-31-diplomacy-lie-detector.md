---
layout: post
title: Detecting lies from messages in Diplomacy - an evil game of deception (Part 1)
slug: diplomacy-lie-classifier
date:   2021-10-31 22:22:00 +0000
categories: [NLP]
tags: [python, data-cleaning, tfidf, classifiers, smote]
---

![Full-width image]({{site.baseurl}}/assets/images/diplomacy-map.png){: width="410" loading="lazy" style="float: right; margin-left: 1em; margin-bottom: 1em"}

Working at a remote-first company, my colleagues and I had to find some fun team-building activities that we could do online. Playing Diplomacy was **not** one of them.

[Diplomacy](https://www.backstabbr.com){:target="_blank"} is a board game of 7 players representing 7 nations at war in the early 20th century: Turkey, Russia, Austria, Italy, Germany, France, and England. To win the game, one must take over 18 "supply centres" (cities) in the map of Europe, by engaging in private "diplomatic" conversations with each other. You can pretty much say anything you want - offer your allegiance, promise to be neutral, suggest a win-win deal, promise to support an attack - and then choose to do the exact opposite. So now you know how the game can spark severe cases of backstabbing, bitterness, and outrage - the perfect workplace situtation, right?

## Treasure Dataset found!
So in my spare time contemplating about the most recent backstabbing that I've experienced in the game, I found an interesting and very timely dataset online: a collection of Diplomacy games and conversations! _Perfect, just perfect_, I thought to my self with an evil grin on my face.

You can find the dataset here:
[Diplomacy: A Dataset for Deception Detection](https://sites.google.com/view/qanta/projects/diplomacy){:target="_blank"}

### Data Format
The link above gives us three files - *train.jsonl*, *validate.jsonl*, and *test.jsonl*. Each file contains a bunch of JSON strings, each representing an entire game dialog. You can check the data source link above for the meta-info about each feature in the dataset. Note that each game has an array of `messages` and a corresponding array of `sender_labels` (whether the sender of the message is lying or not) as well as of `receiver_labels` (whether the receiver thought the message was a lie or not).

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

## The Scope of this Project

So there's loads of things we could possibly build out of this dataset. In this project,
I attempted to train a model with a subset of its features in order to predict if a given message is a truth or a despicable lie.

I've started with a simplistic model first - The only feature I used is `messages`, and `sender_labels` is the label. Simple enough, so I discarded the rest of the data - or reserved it for some other project. I told my self that if the model's performance doesn't turn out well, then I'll write a Part 2 of this project for the improvements (Spoiler alert: it didn't turn out well).


### Lie detection as an NLP problem
There's a few things to note about this project:

1. The label `sender_labels` in the dataset has only two values: `true` or `false` (truth or lie). This could imply that each message sent by a player has the intention to either mislead or make a genuine suggestion to another player (so it's either definitely false or definitely true). But in reality, Diplomacy messages can just be neutral messages, like greetings, questions, or just general chatter. So, instead of interpreting `true` or `false` as either truth or lie, we can interpret `true` as truth or neutral, and `false` as not truth. This representation is particularly useful to avoid confusion when we convert `true` to 1 and `false` to 0.

2. When playing the game, context is very important for humans to detect lies - E.g., At what point in the game was the message sent? Who sent it? What's the current state of the map? In the current approach of this project, those are not considered yet. I only want to know how well word frequencies on messages correlate to the intent of the players sending those messages. In other words, is the presence of certain words in a Diplomacy message make that message more likely to be a lie?

---

## The Code
You can download or clone the code repository for this project on Github: **[Diplomacy-NLP](https://github.com/shielamms/diplomacy-nlp){:target="_blank"}**

The code was tested on Python 3.8.8.

- Before running the code, it's recommended to create a virtual environment in your local directory with the specified Python version. You can do this with pyenv, for example:
```bash
pyenv install -v 3.8.8
pyenv local 3.8.8
python -m pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
```

- Once your virtual environment is created, install the required libraries by:
```bash
pip install -r requirements.txt
```

- Run the code:
```bash
python main.py
```

The program starts with some console messages saying that the model is being trained and validated. After which, it will run in an infinite loop which will ask for your text input (which is your own Diplomacy message that you want to test) and then it will say if your message is a truth or a despicable lie. To exit the program, press Ctrl+C on the terminal.

Here's a sample run on the console:

```
-- DiplomacyGamesReader init --
-- DiplomacyMessageVectorizer init --
-- DiplomacyMessageClassifier init --
Training in progress...
Validation Results: (model: SVC)
Classification Report: ...

Test Results: (model: SVC)
Classification Report: ...

Your test message:
I was talking with Russia, negotiating over Norway and such. They told me they were planning on attacking you, as they thought I was there ally. Just decided to let you know.

The AI thinks...
That is a despicable lie!


Your test message:
France will cross the English Channel next round. You have to take over their SCs now!

The AI thinks...
That is a truth!
```

---
---

# Code Walkthrough

## Reading the Files
Reading *.jsonl* files is just the same way as reading any text file through Python.
I've created a `DiplomacyGamesReader` class, which contains a function for reading an input file and parsing each line as a game.

```python
# file: "reader.py"
import pandas as pd

class DiplomacyGamesReader:
    def __init__(self):
        self.data = None

    def read_from_file(self, filedir):
        games = []
        with open(filedir) as f:
            for line in f:
                game = json.loads(line)
                games.append(game)

        games_df = pd.DataFrame(games).set_index('game_id')

        # to be continued...
```

So far, `read_from_file()` stores all the messages in each game in one row in the dataframe. In our current scope, we're not too concerned about which games the messages are in. This means that in place of operating on a dataframe of games, we should be operating on a dataframe of messages. Here's what I mean:

```python
# file: "reader.py"
        # ... continuation
        messages_df = games_df.apply(pd.Series.explode).reset_index()
        self.data = messages_df
        return self.data
```

If we look back at what each game looks like in the *.jsonl* file, each attribute of a game is an array (apart from its `game_id`). The `Series.eplode` function turns each element of an array into elements of a Series (i.e., a row). Applying this function on `games_df` means all columns of the dataframe will be transformed. Here's what the head of the "exploded" training dataframe looks like:

```
game_id	messages	                                    sender_labels  receiver_labels  speakers	receivers   absolute_message_index    seasons	years
1	Germany!\n\nJust the person I want to speak wi...	True	   True	            italy       germany       74                      Spring     1901
1	You've whet my appetite, Italy. What's the sug...	True	   True	            germany       italy       76                      Spring     1901
1	👍	                                                True       True	            italy       germany	      86                      Spring     1901
1	It seems like there are a lot of ways that cou...	True	   True	            germany       italy       87                      Spring     1901
1	Yeah, I can’t say I’ve tried it and it works, ...	True	   NOANNOTATION	    italy       germany       89                      Spring
```


## Cleaning the messages
Just by looking at the head of the dataframe, one could already find some notable things that could use some fixing. First, there are emojis in the messages. Emojis can be useful for determining intention, but then again some messages with heavy use of emojis could skew our results. Nevertheless, I've written a function to remove these emojis (if you're doing this yourself, you can choose not to remove the emojis, and then compare your results with mine). Emojis are a range of unicode characters, and the ranges for different kinds of emojis can be easily found with a Google search.

```python
# file: "vectorizer.py"
import re

def remove_emojis(message):
    emoji_pattern = re.compile(
                pattern = u"[\U0001F600-\U0001F64F"     # emoticons
                            "\U0001F300-\U0001F5FF"     # symbols & pictographs
                            "\U0001F680-\U0001F6FF"     # transport & map symbols
                            "\U0001F1E0-\U0001FAD6]+",  # flags (iOS)
                flags = re.UNICODE)
    return emoji_pattern.sub(r'', message)

# to be continued...
```

Secondly, before we could tokenize the messages, we'll need to remove some symbols and repeated characters, as well as putting letters into lowercase as a standard.

```python
# file: "vectorizer.py"
# ...continuation
def clean_message(message):
    message = (message.replace('\n', ' ')
                      .replace('-', ' - ')
                      .replace('...', ' ')
                      .replace('???', '?')
              )
    message = remove_emojis(message)

    return message.lower().strip()
```

## Tokenization and Vectorization
Python's NLTK library has a neat little module named `casual_tokenize` that works like a normal tokenizer but specifically made for casual text (like the diplomacy messages) which contain lots of exagerated words and symbols. This tokenizer also allows us to separate punctutations from words, so we can filter out the unnecessary tokens.

```python
# file: "vectorizer.py"
import nltk
import string
from nltk.tokenize.casual import casual_tokenize

stopwords = nltk.corpus.stopwords.words('english')
punctuations = string.punctuation + '\’\”'

# ...continuation
def tokenize_and_remove_stopwords(message):
    tokens = casual_tokenize(message, reduce_len=True)
    tokens = ([t for t in tokens
                    if t not in stopwords
                    and t not in punctuations
                ])
    return tokens
```

After all the messages have been cleaned, we can now feed our tokens into a vectorizer to represent tokens into a numeric format for our prediction model to use.

Recall that the simplistic goal of this project is to determine if the appearance of certain words (or group of words) within a message in a game is a good indicator of whether the whole message is a lie. This roughly translates to the concept of **TF-IDF** (Term Frequency-Inverse Document Frequency), which is a statistical measure of the relevance of a word within a document among a collection of documents (in this case, a document is a message). As a rough example of its consequence, if the words "attack" and "follow" appear more often in messages which are lies, then given a new message which contains both words (irrelevant of its context), then that new message has a higher probability of being a lie.

Scikit-learn's `TfidfVectorizer` represents each token from the messages as a TF-IDF score, which is a numeric score of that token in relation to other tokens in our corpus.

```python
# file: "vectorizer.py"
from sklearn.feature_extraction.text import TfidfVectorizer

# ...continuation
def _create_vectorizer(self):
    vectorizer = TfidfVectorizer(
                    max_df=0.90,
                    max_features=100000,
                    min_df=0.05,
                    stop_words=stopwords,
                    use_idf=True,
                    tokenizer=tokenize_and_remove_stopwords,
                    ngram_range=(1,3)
                )
    return vectorizer
```

Note here that we can pass the `tokenize_and_remove_stopwords()` function that we wrote earlier to the `tokenizer` parameter of `TfidfVectorizer`. This means that the output of the tokenizer function is the input of the instatiated vectorizer.

### Transforming the training data... and finding an *oopsie*
One last step before we can train a prediction model with the training data - we need to fit the message data into our vectorizer. While I was doing this, I found my self in a "facepalm" moment when I realised I haven't looked at the proportion of lies within the training dataset.

```python
reader = reader.DiplomacyGamesReader()
training_df = reader.read_from_file('data/train.jsonl')

print('False:', len(training_df[training_df['sender_labels'] == False]))  # 591
print('True:', len(training_df[training_df['sender_labels'] == True]))    # 12,541
print('Total:', len(training_df))   # 13,132
```

**Out of 13,132 messages, only 4.5% are lies.** That would have severely skewed our predictions towards almost-absolute trust that Diplomacy players tell the truth all the time - which we definitely know is wrong. There's a few ways to avoid this - one being to generate synthetic samples of lies to balance with the truths. This technique is called SMOTE (Synthetic Minority Oversampling Technique), which conveniently comes with the `imblearn` Python library. SMOTE can be used like the following, where `training_matrix` can be a dataframe or a sparse matrix of features, and `training_labels` is a vector of labels.

```python

from imblearn.over_sampling import SMOTE

oversampler = SMOTE(sampling_strategy='minority', k_neighbors=5)
resampled_training_matrix, resampled_training_labels = (
    oversampler.fit_resample(training_matrix, training_labels.ravel())
)
```

This oversampling technique replicates the messages with `sender_labels==False` so that there are as many False labels as True labels in the training data.

To use this with our vectorizer code, I chose to fit the whole preprocessed training data features into the vectorizer first, and then oversample the vectorized data. I added the `oversample` option to disable oversampling when I want to in subsequent trainings.

```python
# file: "vectorizer.py"
from imblearn.over_sampling import SMOTE

# ...continuation
training_matrix = None
training_labels = None

def fit_transform(train_df, oversample=True):
    # convert True labels to 1, False to 0
    training_labels = train_df['sender_labels'].astype(int)
    # vectorize the messages
    training_matrix = (vectorizer
                       .fit_transform(train_df['messages'])
                       .todense())

    if oversample:
        oversample_training_minority()

def oversample_training_minority():
    oversampler = SMOTE(sampling_strategy='minority', k_neighbors=5)

    training_matrix, training_labels = (
        oversampler.fit_resample(training_matrix,
                                 training_labels.ravel())
    )
```


## Training a simple classifier
Choosing the classification algorithm was actually the simplest activity in this exercise. As they say, about 70% of machine learning is just analysing and cleaning the data. For a start, I tried a Support Vector Classifier (SVC), a model that linearly separates data points into two distinct sections on a graph. A classifier class typically has a `train()` and a `predict()` function.

```python
# file: "classifier.py"
from sklearn import svm

CLASSIFIERS = {
    'SVC': svm.SVC(C=1, kernel='linear', decision_function_shape='ovo')
}

class DiplomacyMessageClassifier:
    def __init__(self, classifier='SVC'):
        self.classifier = CLASSIFIERS[classifier]
        self.name = classifier
        self.predictions = None

    def train(self, messages, labels):
        print('Training in progress...')
        self.classifier.fit(messages, labels)
        return self.classifier

    def predict(self, test_messages):
        result = self.classifier.predict(test_messages)
        self.predictions = [bool(p) for p in list(result)]
        return self.predictions
```

To be able to compare this to other models in the future, I've set the `CLASSIFIERS` variable above as a dictionary of classification models. We can then create multiple instances of `DiplomacyMessageClassifier` with different underlying classifiers. We pass the vectorized training features `X_train` and the expected labels `y_train` to the classifier's `train()` function.

```python
import classifier as clf

classifier = clf.DiplomacyMessageClassifier('SVC')
classifier.train(X_train, y_train)
```

## Validation and Evaluation
Recall that we have three files: *train.jsonl*, *validation.jsonl*, and *test.jsonl*.
For the validation and testing, we just do the same pre-processing (data cleaning) steps above, vectorize the messages, and skip the oversampling step, which is only needed in training. We then pass the vectorized messages of the validation set to the classifier's `predict()` function, which returns either 1 (truth) or 0 (lie).

```python
# file: "main.py"
import classifier as clf
import pandas as pd
import reader
import vectorizer as vct

reader = reader.DiplomacyGamesReader()
training_df = reader.read_from_file('data/train.jsonl')

# Vectorize the training messages
vectorizer = vct.DiplomacyMessageVectorizer()
X_train, y_train = vectorizer.fit_transform(training_df)

# Train the classifier with the vectorized training messages
classifier = clf.DiplomacyMessageClassifier('SVC')
classifier.train(X_train, y_train)

# Validate
validation_df = reader.read_from_file('data/validation.jsonl')
X_val = vectorizer.transform(validation_df)
predictions = classifier.predict(X_val)
```

To evaluate the performance of our classification model on the validation and test sets, we'll use scikit-learn's `classification_report` module, which outputs a given model's precision, recall, F1 score, and accuracy.

```python
# file: "main.py"
from sklearn.metrics import classification_report

# ...continuation
def evaluate(X, y, predictions):
    eval_report = classification_report(list(y), predictions)
    eval_results = pd.DataFrame({
        'Messages': X,
        'Prediction': list(predictions),
        'Actual': y,
    })

    print('Classification Report:\n', eval_report)
    return eval_results
```

And then we can call `evaluate()` after making predictions on the validation set:

```python
# file: "main.py"

# ...continuation
print(f'Validation Results: (model: {classifier.name})')
evaluate(validation_df['messages'],
         validation_df['sender_labels'],
         predictions)
```

## The results...

To interpret the results of the classification report, it might be useful to first clarify what true positives, false positives, true negatives, and false positives are in this context.

**True Positives (TP)**: the number of actual true messages that we predicted as true.

**True Negatives (TN)**: the number of actual false messages that we predicted as false.

**False Positives (FP)**: the number of actual false messages that we predicted as true, i.e., we were deceived by a lie.

**False Negatives (FN)**: the number of actual true messages that we predicted as false, i.e, we were overly mistrusting over a message.

When playing the game, it usually weighs more to a player (it *hurts* a lot more) if they believed a lie than if they mistrusted a genuine message. This means that while False Negatives may mean wasted opportunity to be friends with another player, we value False Positives more in our predictions because we don't like believing in lies. Thus, our aim is to minimize those False Positives.

With those definitions out of the way, let's take a look at the classification report on our validation set:

```
Validation Results: (model: SVC)
Classification Report:
               precision    recall  f1-score   support

       False       0.06      0.54      0.11        56
        True       0.97      0.64      0.77      1360

    accuracy                           0.64      1416
   macro avg       0.51      0.59      0.44      1416
weighted avg       0.94      0.64      0.75      1416
```

Let's start with the `False` class (lie):
**Negative Precision:** *Out of all the messages we predicted were lies, how many were actually lies?* Only 6% of what we thought were lies were actually lies.

**Negative Recall:** *Out of all the real lies in the validation set, how many did we catch?* Only 54% of the real lies in the validation set were caught by our model. It's a pretty low performance.

Then we interpret the `True` class (truth or neutral message):
**Positive Precision:** *Out of all the messages we predicted were truths/neutral, how many were actually truths/neutral?* 97% of what we thought were truths/neutral were actually truths/neutral.

**Positive Recall:** *Out of all the real truths/neutral messages in the validation set, how many did we catch?* Only 64% of the real truths/neutral messages in the validation set were caught by our model.

The high Negative Precision means that our model is having a major difficulty finding the real lies within the validation set, either because it's either too trusting or too skeptical. The low Negative Recall and high Positive Precision suggests the former, meaning that it is still too oblivious of deception by other players. This is also well-noted by the higher F1 score for the positive class than the negative class. It's understandable, though, given that even humans have difficulty catching lies from textual information, and that our model is simply using word frequencies as the basis of judging the intention within an entire sentence.

Knowing the models performance on the validation set, we can make a few tweaks either to the data (for example, retain emojis in the messages) or to the model's hyperparameter, or even create more classifiers and compare their performance. For the sake of simplicity of this post, we'll stop here and output the classification report of the SVC model on the test dataset.

```python
# file: "main.py"
# ...continuation
# Test
test_df = reader.read_from_file('data/test.jsonl')
X_test = vectorizer.transform(test_df)
predictions = classifier.predict(X_test)

print(f'Test Results: (model: {classifier.name})')
evaluate(test_df['messages'],
         test_df['sender_labels'],
         predictions)
```

Output:
```
Test Results: (model: SVC)
Classification Report:
               precision    recall  f1-score   support

       False       0.11      0.48      0.18       240
        True       0.93      0.63      0.75      2501

    accuracy                           0.62      2741
   macro avg       0.52      0.56      0.47      2741
weighted avg       0.86      0.62      0.70      2741
```

## Conclusion and Ideas for Improvement
So the first model's performance isn't so great, and it doesn't do any better than human players guessing if a message they receive in the game is a lie. But it's a good start, I think, to practicing data pre-processing to get a better look at the data and think of ways to derive intention. So far, we've only relied on word frequencies and inverse document frequencies to weigh the relevance of certain words in our corpus. In Part 2 of this project (coming soon), we'll take a look into the use of Embeddings, which brings us closer to the meaning of words within sentences, and hopefully help us better detect lies in this friendship-destroying game of deception.
