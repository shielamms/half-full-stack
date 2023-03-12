---
layout: post
title: Calculating the Determinant of a Matrix with the Laplace Expansion
slug: matrix-determinant-with-laplace-expansion
date:   2021-12-04 14:00:00 +0000
categories: [Maths]
tags: [linear-algebra,python]
mathjax: true
---

In the [Matrix Operations]({{ "/maths/matrix-operations" | relative_url }}) article, getting the determinant of a matrix through Python code could be as simple as importing `numpy.linalg.det`. This project is a simple implementation of that calculation through an algorithm called the **Laplace Expansion**. To understand the algorithm, let's first take a look at a simple matrix.

### 2x2 matrix
For a 2x2 matrix, the determinant is simply the difference between the product of the elements of the main diagonal (left to right) and the product of the elements of the diagonal from right to left. For example, given the following 2x2 matrix:
```
[[1 2]
 [3 4]]
```
The determinant is $$(1\times4) - (2\times3) = -2$$.

### 3x3 matrix
For a 3x3 matrix, we introduce the concept of *minors*. A *minor* of a matrix is a square matrix that is derived from excluding a row and column of the original matrix. For example, given this 3x3 matrix:
```
[[1 2 3]
 [4 5 6]
 [7 8 9]]
```

Starting with the first row and first column of this matrix, the minors are:
```
# row 1 and column 1 excluded:
[[5 6
  8 9]]

# row 1 and column 2 excluded:
[[4 6
  7 9]]

# row 1 and column 3 excluded:
[[4 5
  7 8]]
```

Notice that the minors of a 3x3 matrix are of shape 2x2, so we can apply the formula for the determinant of a 2x2 matrix above. The determinant of a minor is called a *cofactor*. To combine the cofactors and calculate the determinant of the 3x3 matrix, we multiply the cofactor by the element in the row and column that we excluded from the matrix. For example, in the first minor where row 1 and column 1 were excluded, the element that we need to multiply with the cofactor is the element in (row1, column1), which is 1.

```
# row 1 and column 1 excluded:
[[5 6
  8 9]]
cofactor = (5*9) - (6*8) = -3
element in (row1, column1) = 1

# row 1 and column 2 excluded:
[[4 6
  7 9]]
cofactor = (4*9) - (6*7) = -6
element in (row1, column2) = 2

# row 1 and column 3 excluded:
[[4 5
  7 8]]
cofactor = (4*8) - (5*7) = -3
element in (row1, column3) = 3
```

The cofactors are added or subtracted from each other, depending on the position of the element it was multiplied with in the original matrix. This sounds a bit confusing, but the following matrix is a layer to show which elements in the matrix are positive and which are negative:
```
[[+ - +]
 [- + -]
 [+ - +]]
```

```
[[1 2 3]
 [4 5 6]
 [7 8 9]]
```

Since we've only multiplied elements from the first row with the cofactors of each minor in our 3x3 matrix, then we can multiply the first cofactor with +1, the second cofactor with -2, and the third cofactor with +3.

```
cofactor of minor from removing row 1, column 1 = -3
element in row 1, column 1 = 1
cofactor sign = +

cofactor of minor from removing row 1, column 2 = -6
element in row 1, column 2 = 2
cofactor sign = -

cofactor of minor from removing row 1, column 3 = -3
element in row 1, column 3 = 3
cofactor sign = +
```

So now we have the signs, the elements, and the cofactors, we can then calculate the determinant of our 3x3 matrix:

$$
[1\times(1\times-3)] + [-1\times(2\times-6)] + [1\times(3\times-3)] = 0
$$

The determinant of our 3x3 matrix is 0.

A determinant of 0 also means that the matrix is non-invertible, or that there is no corresponding matrix that, when multiplied with this matrix, results to the identity matrix.
{:.note title="Side Note"}

### Any nxn matrix, where n > 3
For any other square matrix of a dimension greater than 3, we apply the same method where we get the minors of the matrix, then get the minors of the minors, and so on, until we reach the minors that are of shape 2x2. Once we have calculated the determinant of the 2x2 minors, we backtrack to the 3x3 minors and get their determinant, then backtrack to the 4x4 minors and get their determinant, and so forth. We can think of this in programming as a recursive computation of the determinant of any nxn matrix.

```python
# file: "determinant.py"
import copy
import numpy as np

def get_determinant(matrix):
    if matrix.shape[0] == 1:
        # The determinant of a 1x1 matrix is 1
        return matrix.shape[0]
    elif matrix.shape[0] == 2:
        # The base condition: if the matrix is 2x2, then use the formula
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
    else:
        determinant = 0

        for col in range(matrix.shape[1]):
            # perform a deep copy so the original matrix is not modified
            minor = copy.deepcopy(matrix)

            # remove the first row (axis=0)
            minor = np.delete(minor, 0, 0)
            # remove the col-th column (axis=1)
            minor = np.delete(minor, col, 1)

            cofactor_sign = ((-1)**col)
            cofactor = get_determinant(minor)  # recursive call
            determinant += cofactor_sign * matrix[0][col] * cofactor

        return determinant
```

To test this function, create a square matrix through a numpy array. Here's a sample of a 4x4 matrix.

```python
from numpy import array

A = array([[1,2,3,4],[4,3,5,6],[8,4,2,1],[3,2,4,1]])
print('Matrix:\n', A)
print('Determinant: ', get_determinant(A))

```

The output of the function given the matrix `A` is -99. It's a bit tedious to verify this by hand, but you can use the `numpy.linalg` library and compare the results:

```python
from numpy import array
from numpy.linalg import det

A = array([[1,2,3,4],[4,3,5,6],[8,4,2,1],[3,2,4,1]])
print(det(A))
```

---

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
python determinant.py
```

This will print out a test matrix and call the `get_determinant()` function. The output is the determinant of that test matrix.

---

## References and Further Reading:
- [Taboga, Marco (2021). "The Laplace expansion, minors, cofactors and adjoints", Lectures on matrix algebra.](https://www.statlect.com/matrix-algebra/Laplace-expansion-minors-cofactors-adjoints){:target="_blank"}

- ["Understanding the Determinant of a Matrix" on Programathically](https://programmathically.com/determinant-of-a-matrix/){:target="_blank"}
