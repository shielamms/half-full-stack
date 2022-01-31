---
layout: post
title: "Matrix Factorization: Eigendecomposition"
slug: eigendecomposition
date:   2022-01-02 19:00:00 +0000
categories: [Maths]
tags: [linear-algebra,python]
mathjax: true
---

Sometimes matrices become too large that performing operations on them can become computationally expensive or that they take up too much space. This is especially the case for *sparse matrices*, wherein there are more 0s or null values than useful data. For example, we have a dataset of what movies customers in an online platform have watched. Supposing we have several movies and several customers, representing each customer's watched movies through One-Hot Encoding would look like this:

| customer_id | movie 1 | movie 2 | movie 3 | movie 4 | movie 5 | ...
| a | 0 | 0 | 1 | 0 | 0 | ...
| b | 0 | 0 | 0 | 1 | 0 | ...
| c | 1 | 0 | 0 | 0 | 0 | ...
| d | 0 | 0 | 0 | 1 | 1 | ...
| e | 0 | 0 | 0 | 0 | 0 | ...
| ... | ... | ... | ... | ... | ... | ... |

Observe that each customer has more movies they haven't watched yet than they watched, which puts a lot more 0s than 1s in any row. If we want to perform an operation on the numeric columns in this matrix, we'd be wasting storage, time, and computing power performing operations on 0s which do not contain information. Plus, the more features we add to the dataset, the more dimensions in the matrix, resulting to more complex operations on the sparse data.

A useful tool for simplifying matrices is the process of *matrix decomposition*, or *matrix factorization*, which reduces the matrix into simpler components, thereby simplifying the operations on the matrix. One of the most popular matrix decomposition methods is **eigendecomposition**, which reduces the matrix into **eigenvalues** and **eigenvectors**.

Eigendecomposition can only be done on square matrices, and not all square matrices can be eigendecomposed.

To understand eigenvectors, we go back to a basic matrix-vector operation: Multiplying a matrix by a vector results in another vector. For example, multiplying matrix $$A$$ with vector $$v$$ below:

$$
\begin{aligned}
&A =
\left(\begin{array}{cc}
2 & 4 \\
6 & 8 \\
\end{array}\right)
\\[1em]

&v =
\left(\begin{array}{cc}
1 & 2 \\
\end{array}\right)
\\[2em]

&A \circ v=
\left(\begin{array}{cc}
10 & 22 \\
\end{array}\right)
\end{aligned}
$$

Most of the time, when a matrix is multiplied by a vector, the direction of the resulting vector changes; i.e, the new vector is not a scaled version of the original vector. However, there are special cases when the resulting vector is in the same direction as the original vector. In this case, the original vector is called an *eigenvector* of the matrix.

An eigenvector is a vector that, when multiplied by the matrix that we want to decompose, results to a vector whose direction does not change from the original vector.
{:.note title="Definition"}

So now we know that a matrix multiplied by an eigenvector produces a vector of the same *direction*, we can determine the vector's *magnitude* through a scalar. This scalar is called the **eigenvalue**.

An eigenvalue is a scalar that tells how much an eigenvector is shrunk, stretched, or reversed in relation to the eigenvector's direction when multiplied by a matrix.
{:.note title="Definition"}

In notation, we can look at eigenvectors and eigenvalues this way:

$$
\begin{aligned}
A \cdot v = \lambda \cdot v
\end{aligned}
$$

Where $$A$$ is the matrix, $$v$$ is the eigenvector, and $$\lambda$$ is the eigenvalue.
A matrix can have an eigenvector and an eigenvalue for each of its dimensions.

Normally, the eigenvalues are calculated first before the eigenvectors. To calculate the eigenvalues, we use the equation above and move everything to the left hand side of the equation.

$$
\begin{aligned}
A \cdot v - \lambda \cdot v = 0
\end{aligned}
$$

We can go further and simplify the equation to disregard the eigenvectors $$v$$ for now, since we're still computing for the eigenvalues.

$$
\begin{aligned}
A - \lambda = 0
\end{aligned}
$$

But, in this case, $$A$$ is a matrix, and $$\lambda$$ is a scalar, which we can't subtract directly from a matrix. This is where the *identity matrix* comes in handy: anything multiplied by the identity is itself. The identity matrix is a matrix where the main diagonals are composed of 1s, and the rest are 0s. The dimensions of the identity matrix are the same as the dimensions of the matrix $$A$$. The identity matrix of a 3x3 matrix looks like this:

$$
\begin{aligned} \\
\left(\begin{array}{cc}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\end{array}\right)
\end{aligned}
$$

So, if we multiply the scalar $$\lambda$$ by the identity matrix $$I$$, we'll get the following equation:

$$
\begin{aligned}
A - \lambda * I = 0
\end{aligned}
$$

But wait, if $$A$$ and $$\lambda * I$$ are matrices, how does that equate to a 0, which is a scalar (technically, a scalar without magnitude..which might spark some debate, but anyway..)?
Matrices have a special property called the **determinant**, which is a scalar representation of the volume of a matrix. You can find out __here__ for how to compute for the determinant of a matrix. So, actually, what we're trying to get to is this:

$$
\begin{aligned}
det(A - \lambda * I) = 0
\end{aligned}
$$

What this essentially means is that if, by definition, an eigenvalue is a component of a matrix, then subtracting the eigenvalue (multiplied by the identity) from the matrix should result to a 0 determinant. Solving for $$\lambda$$ would yield a scalar: 2 scalars if the the matrix were 2x2, 3 scalars if 3x3, and so on.

For each value of $$\lambda$$ that you compute from above, you can get the corresponding eigenvector by substituting $$\lambda$$ in the original equation then solving for $$v$$:

$$
\begin{aligned}
A - \lambda * I = 0
\end{aligned}
$$
