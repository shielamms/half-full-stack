---
layout: post
title: Matching names through the Levenshtein Distance
slug: levenshtein-distance
date:  2022-01-01 20:28:00 +0000
categories: [NLP]
tags: [python, strings, similarities]
---

Suppose you have a string that you need to match with any of a set of strings that may or may not contain an exact match. The usual solution is to find the string within the set that is the *most similar* to the string that you are looking for. But, this *similarity* needs to be quantifiable in order to be programmable, and one of the popular ways to measure the *similarity* between two strings is called the *Levenshtein Distance*.

The **Levenshtein Distance** is the minimum number of steps to transform one string into another. One transformation means one operation on a character of the original string. An operation can be any of the following:

1. Insert (insert a new character in a specified index)
2. Replace (replace the character at a specified index with another character)
3. Remove (remove the character at a specified index)

Luckily in Python, there is a library called `python-Levenshtein` that provides a function to calculate the Levenshtein Distance for us:
```
pip install python-Levenshtein
```

Then to use this library:
```python
import Levenshtein

Levenshtein.distance(string1, string2) # outputs an integer
```

But, of course, I wouldn't post about this without knowing how the algorithm behind the distance calculation works. I've coded my own implementation using a numpy array (matrix) to represent the transformations on each character in a given string. Before looking at the code, I've outlined below my use case for this algorithm.

---

## Background of the Project

At work, I sometimes get data about universities from multiple sources on the internet. The problem is that a university may have a slightly different name between different sources. For example, I got a university named *"Saint Joseph's College (ME)"* from one source, but I can't find an exact match on our database. I currently have the following subset of universities:

```
Saint Joseph's College of Indiana
Saint John's College
Saint John's University Thailand
Saint Josephs College
College of Saint Joseph in Vermont
```

In this case, I could have easily matched "Saint Joseph's College (ME)" with "Saint Josephs College" by removing special characters and anything between parentheses. But it would be foolhardy to make such a generalised rule for all other universities with special characters and parentheses values. We want a way to match names with minimal loss of information. Enter the Levenshtein Distance!

## The Code

You can download or clone the code repository for this project on Github: **[nlp/01-levenshtein_distance](https://github.com/shielamms/nlp/tree/main/01-levenshtein_distance){:target="_blank"}**

The code was tested on Python 3.8.8 with numpy version 1.22.

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

---

# The Algorithm

To compute for the Levenshtein distance between two strings, we can create a matrix where each element represents the transformation of a character in string1 to its corresponding character in string2. Let's use a simple example for demonstration. Here, we want to know how many operations at minimum are required to transform the word "smiles" to "simple".

```python
string1 = 'smiles'
string2 = 'simple'
```

  Initialise a zero-matrix where the number of columns is the length of string1 + 1, and the number of rows is the length of string2 + 1. Since both string1 and string2 are of length=6, then we get a 7x7 matrix initialised with 0s.

  A zero-matrix of size m x n can be initialised with `numpy.zeros`.
  ```python
  import numpy as np
  matrix = np.zeros((len(string2)+1, len(string1)+1))
  ```
  The matrix would look something like this (ignore the white row at the top - that's just a markdown problem).

|---------------------------|
|                           |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---------------------------|



  Next, prefix each string with an empty string, such that when we align the characters of string1 into each column in the matrix, the first element (index=0) is the empty string. In the same manner, when we align the characters of string2 into each row, the first element is the empty string. Note that in the following illustration, we still have a a 7x7 matrix (those with 0s), and the non-numeric characters are just labels for the rows and columns.

|-------------------------------|
|                               |
|-------------------------------|
|   |'' | s | m | i | l | e | s |
|-------------------------------|
|'' | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| s | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| i | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| m | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| p | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| l | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| e | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|

  The first row will contain the index of each character in string1, starting from 0 for the index of the empty string. In the same manner, the first column will contain the index of each character in string2 starting from the empty string. The matrix would then look like this:

|-------------------------------|
|                               |
|-------------------------------|
|   |'' | s | m | i | l | e | s |
|-------------------------------|
|'' | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-------------------------------|
| s | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| i | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| m | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| p | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| l | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| e | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|

  We represent this logic with the following python code:
  ```python
  # Initialize the first row
  for col in range(len(matrix[0])):
      matrix[0][col] = col

  # Initialize the first column
  for row in range(len(matrix)):
      matrix[row][0] = row
  ```

  To calculate the value at a certain cell in the matrix, we first need to determine if the character at the current column is the same as the character at the current row. For example, at cell (1,1), the character at column=1 on string1 is 's', while the character at row=1 on string2 is also 's'. In this case where the characters are the same, we just copy the value at the cell on its upper left. For cell (1,1), the value on its upper left cell is 0, so its value is also 0.

  If the characters are not the same, then we get the minimum of the values on the current cell's left, upper left, and its top, and then add 1. For example, at cell (1,2), the character 'm' is not the same as the character 's'. To get the value at (1,2), we get the minimum among the values at (1,1), (0,1), and (0,2), then add 1. In pseudocode:

  ```
  current_row = 1
  current_column = 2

  left = matrix[current_row, current_column-1]
  diagonal = matrix[current_row-1, current_column-1]
  top = matrix[current_row-1, current_column]
  matrix[current_row, current_column] = min(left, diagonal, top) + 1
  ```

  So in the current state of our matrix, if our current cell is (1,2), then we get the minimum among 0, 1, and 2, which is 0. Add 1. The value at cell (1,2) is 1.

  Apply the same logic to the rest of the cells on row 1, and we get the matrix to this state:

|-------------------------------|
|                               |
|-------------------------------|
|   |'' | s | m | i | l | e | s |
|-------------------------------|
|'' | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-------------------------------|
| s | 1 | 0 | 1 | 2 | 3 | 4 | 5 |
|-------------------------------|
| i | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| m | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| p | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| l | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|
| e | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
|-------------------------------|

  We write the logic for getting the value at a certain cell in the matrix throug the following python code:

  ```python
  for row in range(1, len(matrix)):
    for col in range(1, len(matrix[0])):
        if string1[col-1] == string2[row-1]:
            matrix[row][col] = matrix[row-1][col-1]
        else:
            left = matrix[row][col-1]
            diagonal = matrix[row-1][col-1]
            top = matrix[row-1][col]
            matrix[row][col] =  min(left, diagonal, top) + 1
  ```

  Running this loop for all the cells in the matrix gives us this state:

|-------------------------------|
|                               |
|-------------------------------|
|   |'' | s | m | i | l | e | s |
|-------------------------------|
|'' | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-------------------------------|
| s | 1 | 0 | 1 | 2 | 3 | 4 | 5 |
|-------------------------------|
| i | 2 | 1 | 1 | 1 | 2 | 3 | 4 |
|-------------------------------|
| m | 3 | 2 | 1 | 2 | 2 | 3 | 4 |
|-------------------------------|
| p | 4 | 3 | 2 | 2 | 3 | 3 | 4 |
|-------------------------------|
| l | 5 | 4 | 3 | 3 | 2 | 4 | 4 |
|-------------------------------|
| e | 6 | 5 | 4 | 4 | 3 | 2 | 3 |
|-------------------------------|

  Recall that the algorithm counts the number of transformations needed to change string1 to string2, and this was done by comparing the strings character by character and selecting which operation amounts to the least possible changes. The idea behind looking at the left, upper left, and top of a certain cell is that each side represents an operation: insert, replace, or remove.

  If the minimum is on the left of the cell, then it means that the best operation to perform is *inserting* a character on string1 at that particular index. If the minimum is on the upper left of the cell, it means that the best operation to perform is *replacing* the character on string1 to the corresponding character on string2. If the minimum is on the top of the cell, then the best operation is to *remove* the corresponding character from string2. This is done iteratively from left to right, top to bottom of the matrix, such that once we arrive at the very last cell, we would have computed for the minimum value that results into the entire string2.

  For the last cell in our matrix, the minimum of its left (2), upper left (4), and top (4) is 2, so the value at the last cell is 2+1=3. This is solution and the output of the algorithm.

  Putting it all together:

  ```python
  def get_levenshtein_distance(string1, string2):
    matrix = np.zeros((len(string2)+1, len(string1)+1))

    # Initialize the first row
    for col in range(len(matrix[0])):
        matrix[0][col] = col

    # Initialize the first column
    for row in range(len(matrix)):
        matrix[row][0] = row

    for row in range(1, len(matrix)):
        for col in range(1, len(matrix[0])):
            if string1[col-1] == string2[row-1]:
                matrix[row][col] = matrix[row-1][col-1]
            else:
                left = matrix[row][col-1]
                diagonal = matrix[row-1][col-1]
                top = matrix[row-1][col]
                matrix[row][col] =  min(left, diagonal, top) + 1

    return matrix[len(matrix)-1][len(matrix[0])-1]  # value at the last cell
  ```

---

## References and Further Study

  - A good [Youtube video by Jyotinder Singh](https://youtu.be/Dd_NgYVOdLk) explaining the algorithm

  - [python-Levenshtein documentation on Pypi](https://pypi.org/project/python-Levenshtein/#id21)
