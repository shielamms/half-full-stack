---
layout: post
title: Matrices and Matrix Operations
date:   2021-12-04 13:00:00 +0000
categories: [Maths]
tags: [linear-algebra,python,numpy]
mathjax: true
---

Matrices are a foundational concept in data science and machine learning. A common application of matrices in data science is the use of datasets or tables. The transformations that are done on these tables, which are essentially matrices, apply linear algebra operations on matrices and vectors. Take the following example of a dataset:

$$
\begin{align*}
f_1 && f_2 && f_3 && f_4 && label \\
1.3 && 2.0 && 1 && 5.6 && cat \\
1.0 && 2.0 && 3 && 3.2 && dog \\
2.0 && 2.5 && 3 && 2.9 && dog \\
2.3 && 2.2 && 1 && 7.0 && cat \\
\end{align*}
$$

Here the columns $$f_1$$ to $$f_4$$, which are the features or inputs, form a matrix. The $$label$$ column, which is the data to be predicted, forms a vector.

In this post, we go through the operations that can be performed on matrices. First, we demonstrate arithmetic operations on matrices to relate them to the familiar scalar operations. The last part briefly discusses matrix transformations like the Inverse, Transpose, Trace, and Determinant.

---

## Matrices in programming
We can think of a matrix as a two-dimensional array of rows and columns. Python's Numpy package allows us to create a matrix through its `array` module, which also provides functions to help us perform matrix operations.

```python
from numpy import array
```

## Matrix Notation
In math notation, a matrix is represented by a capital letter, like $$A$$. Each element of $$A$$ is represented by the small letter equivalent of the matrix variable, and its position in the matrix is indicated by a subscript.
For example: $$a_{1,1}$$ is the element on the first row and first column of matrix $$A$$.

## Matrix Arithmetic
We can perform arithmetic operations on matrices with the same dimensions. The operation is performed element-wise between the matrices.
### 1. Matrix Addition
Adding two matrices of the same dimensions produces a new matrix with the same dimension.

**Notation**: $$C = A + B$$

$$
\begin{aligned}
&A =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} & a_{1,3} \\
a_{2,1} & a_{2,2} & a_{2,3} \\
\end{array}\right)
\\[1em]
&B =
\left(\begin{array}{cc}
b_{1,1} & b_{1,2} & b_{1,3} \\
b_{2,1} & b_{2,2} & b_{2,3} \\
\end{array}\right)
\\[2em]
&C =
\left(\begin{array}{cc}
a_{1,1} + b_{1,1} & a_{1,2} + b_{1,2} & a_{1,3} + b_{1,3} \\
a_{2,1} + b_{2,1} & a_{2,2} + b_{2,2} & a_{2,3} + b_{2,3}
\end{array}\right)
\end{aligned}
$$

**Numpy:**
```python
A = array([[1,2,3], [4,5,6]])
B = array([[1,3,5], [2,4,6]])
C = A + B

print(A,B,C, sep='\n\n')
```

Output:
```
[[1 2 3]
 [4 5 6]]

[[1 3 5]
 [2 4 6]]

[[ 2  5  8]
 [ 6  9 12]]
```

### 2. Matrix Subtraction
Same concept as in addition, subtracting two matrices of the same dimensions produces a new matrix with the same dimension.

**Notation**: $$C = A - B$$

**Numpy:**
```python
C = A - B
print(C)
```

Output:
```
[[ 0 -1 -2]
 [ 2  1  0]]
```


### 3. Matrix Multiplication (Hadamard Product)
The Hadamard Product is the element-wise product of two matrices.

**Notation**: $$C = A \circ B$$

$$
\begin{aligned}
&A =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} & a_{1,3} \\
a_{2,1} & a_{2,2} & a_{2,3} \\
\end{array}\right)
\\[1em]
&B =
\left(\begin{array}{cc}
b_{1,1} & b_{1,2} & b_{1,3} \\
b_{2,1} & b_{2,2} & b_{2,3} \\
\end{array}\right)
\\[2em]
&C =
\left(\begin{array}{cc}
a_{1,1} \times b_{1,1} & a_{1,2} \times b_{1,2} & a_{1,3} \times b_{1,3} \\
a_{2,1} \times b_{2,1} & a_{2,2} \times b_{2,2} & a_{2,3} \times b_{2,3}
\end{array}\right)
\end{aligned}
$$

**Numpy:**
```python
A = array([[1,2,3], [4,5,6]])
B = array([[1,3,5], [2,4,6]])
C = A * B

print(A,B,C, sep='\n\n')
```

Ouput:
```
[[1 2 3]
 [4 5 6]]

[[1 3 5]
 [2 4 6]]

[[ 1  6 15]
 [ 8 20 36]]
```

---

## Matrix Dot Product (Matrix-Matrix Multiplication)
The Dot Product involves multiplying two matrices such that each row in the first matrix is multiplied by each column in the second matrix. The matrices are not necessarily the same dimensions, but should abide by the following rule: The number of columns of the first matrix must be equal to the number of rows in the second matrix.

Multiplying a matrix of dimension $$m$$ x $$n$$ with another matrix of dimension $$n$$ x $$k$$ results to a new matrix of dimension $$m$$ x $$k$$.

**Notation**: $$C = A \cdot B$$

$$
\begin{aligned} \\
&A =
    \left(\begin{array}{cc}
    a_{1,1} & a_{1,2} & a_{1,3} \\
    a_{2,1} & a_{2,2} & a_{2,3} \\
    \end{array}\right)
\\[1em]
&B =
    \left(\begin{array}{cc}
    b_{1,1} & b_{1,2} \\
    b_{2,1} & b_{2,2} \\
    b_{3,1} & b_{3,2} \\
    \end{array}\right)
\\[1em]
&C =
    \left(\begin{array}{cc}
    a_{1,1} \times b_{1,1} + a_{1,2} \times b_{2,1} + a_{1,3} \times b_{3,1} && a_{1,1} \times b_{1,2} + a_{1,2} \times b_{2,2} + a_{1,3} \times b_{3,2} \\
    a_{2,1} \times b_{1,1} + a_{2,2} \times b_{2,1} + a_{2,3} \times b_{3,1} && a_{2,1} \times b_{1,2} + a_{2,2} \times b_{2,2} + a_{2,3} \times b_{3,2}
    \end{array}\right)
\end{aligned}
$$

```python
A = array([[1,1,1], [2,2,2]])
B = array([[1,2], [3,4], [5,6]])
C = A.dot(B)    # From Python 3.5 and later: A @ B

print(A,B,C, sep='\n\n')
```

Output:
```
[[1 1 1]
 [2 2 2]]

[[1 2]
 [3 4]
 [5 6]]

[[ 9 12]
 [18 24]]
```

## Matrix-Vector Multiplication

Similar to the matrix-matrix dot product, a matrix multiplied by a vector assumes that the number of columns in the matrix is equal to the number of items in the vector. Since a vector is essentially a matrix with one column, when we multiply a matrix of dimension $$m$$ x $$n$$ with a vector of size $$n$$, we can imagine the vector like a matrix of dimension $$n$$ x $$1$$ to produce a new matrix of dimension $$m$$ x $$1$$. Thus, the product of a matrix and a vector is a vector.

**Notation**: $$C = A \cdot v$$
$$
\begin{aligned} \\
&A =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} & a_{1,3} \\
a_{2,1} & a_{2,2} & a_{2,3}
\end{array}\right)
\\[1em]
&v =
\left(\begin{array}{cc}
v_1 \\
v_2 \\
v_3 \\
\end{array}\right)
\\[1em]
&C =
\left(\begin{array}{cc}
(a_{1,1} \times v_1) + (a_{1,2} \times v_2) + (a_{1,3} \times v_3) && (a_{2,1} \times v_1) + (a_{2,2} \times v_2) + (a_{2,3} \times v_3) \\
\end{array}\right)
\end{aligned}
$$

**Numpy:**

```python
A = array([[1,2,3], [2,3,4]])
v = array([0.75,0.25,0.5])
C = A.dot(v)

print(A,v,C, sep='\n\n')
```

Output:
```
[[1 2 3]
 [2 3 4]]

[0.75 0.25 0.5 ]

[2.75 4.25]
```

---

## Matrix Transformations
### 1. Transpose
To transpose a matrix means flipping the dimensions of a matrix. For example, a 2x3 matrix is transposed to a 3x2 matrix, where the rows become the columns and the columns become the rows.

**Notation**:  $$A^T$$

$$
\begin{aligned} \\
&A =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} & a_{1,3} \\
a_{2,1} & a_{2,2} & a_{2,3} \\
\end{array}\right)

&A^T =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} \\
a_{2,1} & a_{2,2} \\
a_{3,1} & a_{3,2}
\end{array}\right)
\end{aligned}
$$

**Numpy:**
```python
A = array([[1,2,3], [3,4,5]])
print(A)
print(A.T)
```

Output:
```
[[1 2 3]
 [3 4 5]]

[[1 3]
 [2 4]
 [3 5]]
```

### 2. Inverse
Inversion means finding a matrix that, when multiplied by the original matrix, results to the identity matrix. The **identity matrix** is a matrix where the main diagonal is composed of 1s.

$$
\begin{aligned} \\
\left(\begin{array}{cc}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\end{array}\right)
\end{aligned}
$$

The concept of a *matrix inverse* is the same as reciprocals of scalar values in solving systems of linear equations. For example, suppose we need to solve for $$x$$ in this equation:
$$
3x = 15
$$

We multiply 3 by its reciprocal, or the *inverse* of 3, which is 1/3. We then do the same on the right side of the equation to maintain equality. A number and its inverse cancel each other out, so the result of $$(1/3)\times3$$ is 1, which is the *identity*.

$$
\begin{aligned}
&\left(1/3\right) \times 3x = \left(1/3\right) \times 15 \\
&x = 15/3 \\
&x = 5
\end{aligned}
$$

We apply the same concept to matrices in place of scalars. For example, suppose we need to establish equality of a matrix multiplied by a vector of variables with another matrix:

$$
\begin{aligned} \\
\left(\begin{array}{cc}
3 & 5 & -1 \\
-2 & 2 & -7 \\
4 & 3 & -4
\end{array}\right)
\left(\begin{array}{cc}
x \\
y \\
z
\end{array}\right)
=
\left(\begin{array}{cc}
3x + 5y - z \\
-2x + 2y -7z \\
4x + 3y -4z
\end{array}\right)
\end{aligned}
$$

To determine the values of the vector $$(x,y,z)$$, we need to multiply the matrix on the left side of the equation with its *inverse*, and also multiply that inverse with the matrix on the right side of the equation.

$$
\begin{aligned} \\
\left(\begin{array}{cc}
(inverse)
\end{array}\right)
\times\left(\begin{array}{cc}
3 & 5 & -1 \\
-2 & 2 & -7 \\
4 & 3 & -4
\end{array}\right)
\left(\begin{array}{cc}
x \\
y \\
z
\end{array}\right)
=
\left(\begin{array}{cc}
(inverse)
\end{array}\right)
\times\left(\begin{array}{cc}
3x + 5y - z \\
-2x + 2y -7z \\
4x + 3y -4z
\end{array}\right)
\end{aligned}
$$

Similar to the inverse of scalars, a matrix and its inverse cancel each other out, producing the identity matrix.

**Notation**:  $$A^{-1}$$

$$
\begin{aligned}
A^{-1} \cdot A = I
\end{aligned}
$$

Finding the inverse $$A^{-1}$$ of a matrix $$A$$ starts by finding the determinant of the matrix.

**Numpy:**

Luckily we don't have to calculate matrix inverses by hand in Python. Numpy's `linalg.inv` module can do that for us.

```python
from numpy.linalg import inv

A = array([[1,2], [3,4]])
I = inv(A)
M = A.dot(I)

print(A,I,M, sep='\n\n')
```

Output:
```
[[1 2]
 [3 4]]

[[-2.   1. ]
 [ 1.5 -0.5]]

[[1.00000000e+00 1.11022302e-16]
 [0.00000000e+00 1.00000000e+00]]
```

### 3. Trace
The trace is the sum of the values in the main diagonal of a square matrix.

**Notation**:  $$tr(A)$$

$$
\begin{aligned}
&A =
\left(\begin{array}{cc}
a_{1,1} & a_{1,2} & a_{1,3} \\
a_{2,1} & a_{2,2} & a_{2,3} \\
a_{3,1} & a_{3,2} & a_{3,3}
\end{array}\right)
\\[1em]
&tr(A) = a_{1,1} + a_{2,2} + a_{3,3} \\
\end{aligned}
$$

```python
from numpy import trace

A = array([[1,2,3], [3,4,5], [6,7,8]])
B = trace(A)

print(A,B, sep='\n\n')
```

Output:
```
[[1 2 3]
 [3 4 5]
 [6 7 8]]

13
```

### 4. Determinant
The determinant is the scalar representation of the volume of the matrix. It is the product of all the eigenvalues of the matrix. In other words, it describes the way the matrix will scale another matrix when they are multiplied together.

A zero determinant means that the matrix is not invertible.

```python
from numpy.linalg import det

A = array([[1,2,3], [4,5,6], [7,8,9]])
d = det(A)

print(A,d, sep='\n\n')
```

Output:
```
[[1 2 3]
 [4 5 6]
 [7 8 9]]

-9.51619735392994e-16
```
