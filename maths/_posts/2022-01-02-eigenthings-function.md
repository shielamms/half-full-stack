---
layout: post
title: Confirming Eigenvectors and Reconstructing the Matrix from Eigenthings
slug: eigenthings-confirm-and-reconstruct-functions
date:   2021-01-02 15:00:00 +0000
categories: [Maths]
tags: [linear-algebra,python]
mathjax: true
---

This mini project contains two functions:
1. a function to check whether a vector is an eigenvector of a matrix
2. a function to reconstruct the matrix using its eigenvectors and eigenvalues ("eigenthings")

The code makes use of numpy modules to implement matrices and vectors, and getting the eigenthings of matrices.
Each function has an associated test function that is called when the program starts.


## The Code:
You can checkout the complete code in **[my linear algebra repository](https://github.com/shielamms/maths-for-data-science/tree/main/1_linear-algebra){:target="_blank"}**.

This code was tested on Python 3.8 with numpy version 1.21.

- Before running the code, it's recommended to create a virtual environment in your local directory with the specified Python version. You can do this with pyenv, for example:
```bash
pyenv install -v 3.8.8
pyenv local 3.8.8
python -m pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
```

- Install the latest numpy version or a specific version of 1.21.
```bash
pip install numpy==1.21.5
```
- Run the code:
```bash
python eigenthings.py
```

The output comes in two parts:
The first part prints out the output of the function `test_confirm_eigenvectors()`.
The first printout is a test 2x2 matrix, and then followed by test vectors and test values. The function then says if each set of test vectors is an eigenvector of the matrix:

```
--- test_confirm_eigenvectors ---
Matrix:
 [[1 2]
 [3 4]]
Test vectors:
 [[-0.82456484 -0.41597356]
 [ 0.56576746 -0.90937671]]
Test values:
 [-0.37228132  5.37228132]

Is vector 1 an eigenvector?  True
Expected:  True

Is vector 2 an eigenvector?  True
Expected:  True
```

The second part prints out the output of the function `test_reconstruct_matrix_from_eigenthings()`. The first printout is a test matrix, followed by its eigenvalues and eigenvectors calculated by using `numpy.linalg.eig()`. The final output is the matrix reconstructed from the eigenvalues and eigenvectors. The reconstructed matrix should be equal to the original test matrix.

```
Original matrix:
 [[1 2]
 [3 4]]
Eigenvectors:
 [[-0.82456484 -0.41597356]
 [ 0.56576746 -0.90937671]]
Eigenvalues:
 [-0.37228132  5.37228132]
Reconstructed matrix:
 [[1. 2.]
 [3. 4.]]
```


## Code Walkthrough
Under Construction! The author is still translating the code into easily digestible concepts. Stay tuned! Meanwhile, you can checkout the code yourself: **[my linear algebra repository](https://github.com/shielamms/maths-for-data-science/tree/main/1_linear-algebra){:target="_blank"}**
