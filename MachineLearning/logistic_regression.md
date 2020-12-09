# 逻辑回归

从理解上应该叫 **对数几率回归**，或者 **对数几率二分类判别**

首先要了解线性回归，对数几率回归是由线性回归变换而来



## 线性回归

对于线性回归，我们使用的拟合模型是
$$
y = a^Tx+b \\
a=[a_1, a_2, ..., a_n]^T \in R^n , x = [x_1, x_2, ..., x_n]^T\in R^n, b \in R^1, y \in R^1
$$


### 一元线性回归

最简单的线性回归模型：$x$ 是一维向量， 即 $ x \in R^1$，此时 $x^T = x$

给定数据 $(x_1, y_1), (x_2, y_2), (x_3, y_3)$ ，用模型 $y=ax+b$ 去拟合，使得 $\sum_{i=1}^3 (a^T*x_i + b -y_i)^2$ 最小

最小二乘方程组为
$$
\begin{gathered}
\begin{bmatrix} x_1^T & 1 \\ x_2^T & 1 \\ x_3^T & 1 \end{bmatrix} \times
\begin{bmatrix} a  \\ b \end{bmatrix} =
\begin{bmatrix} y_1  \\ y_2 \\ y_3 \end{bmatrix} 
\end{gathered}
$$
用最小二乘法可以解得参数近似值
$$
\begin{gathered}
\begin{bmatrix} a  \\ b \end{bmatrix} = 
(\begin{bmatrix} x_1^T & 1 \\ x_2^T & 1 \\ x_3^T & 1 \end{bmatrix}^T \begin{bmatrix} x_1^T & 1 \\ x_2^T & 1 \\ x_3^T & 1 \end{bmatrix})^{-1}\begin{bmatrix} x_1^T & 1 \\ x_2^T & 1 \\ x_3^T & 1 \end{bmatrix}^T
\begin{bmatrix} y_1  \\ y_2 \\ y_3 \end{bmatrix} 
\end{gathered}
$$
于是我们就得到了一个最简单的模型



### 多元线性回归

此时 $x$ 是一个 $n$ 维列向量，即 $x = (x_1, x_2, ..., x_n)^T \in R^n$ 

现在我们有一组数据 $(x_1, y_1), (x_2, y_2), ..., (x_m, y_m)$ ，其中 $x_i = (x_{1i}, x_{2i}, ..., x_{mi})^T \in R^n$ ， $y_i \in R$

我们要求 $a=(a_1, a_2, ..., a_n)^T \in R^n, b \in R$ 的值，使得 $\sum_{i=1}^m (a^T*x_i + b -y_i)^2$ 达到最小

由最小二乘法，方程组可变为
$$
\begin{gathered}
\begin{bmatrix} x_1^T & 1 \\ x_2^T & 1 \\ ...&... \\ x_m^T & 1 \end{bmatrix} \times
\begin{bmatrix} a_1  \\ a_2 \\ ... \\ a_n \\ b \end{bmatrix} =
\begin{bmatrix} y_1  \\ y_2 \\ ... \\ y_m \end{bmatrix} <==>
X \times W=Y
\end{gathered}
$$
方程的近似解为
$$
W = \begin{bmatrix} a_1  \\ a_2 \\ ... \\ a_n \\ b \end{bmatrix} =  (X^TX)^{-1}X^TY
$$


## 对数几率回归



### 什么是对数几率回归

用于二分类，$y \in \{0, 1\}$  , 所以需要一个 $x \in R, y \in (0, 1)$ 的函数，对数几率回归使用的是
$$
y = \frac{1}{1+e^{-x}}
$$
此函数是任意阶可导的凸函数，有很好的数学性质，现有的许多数值优化算法都可直接用于求取最优解

所以我们使用的拟合模型是 
$$
y = \frac{1}{1+e^{-(a^Tx+b)}} , x \in R^n, a \in R^n, b \in R, y \in (0, 1)
$$
我们要求 $a=(a_1, a_2, ..., a_n)^T \in R^n, b \in R$ 的值，使得 $\sum_{i=1}^n (\frac{1}{1+e^{-(a^Tx_i+b)}} -y_i)^2$ 达到最小

函数形式可变为
$$
y = \frac{1}{1+e^{-(a^Tx+b)}} ==> ln \frac{y}{1-y} = a^Tx+b
$$
若将 $y$ 视为样本作为正例的可能性，则 $1-y$ 是其反例可能性

两者的比值 $\frac{y}{1-y}$ 称为几率，反映了 $x$ 作为正例的相对可能性，对 几率 取对数，就得到对数几率  
$$
ln \frac{y}{1-y}
$$
所以**对数几率拟合模型**实际上是用**线性回归模型**的预测结果去逼近真实标记的对数几率



### 如何求解对数几率回归

现在我们要求解 $a, b$ 的值， 但是我们的样本数据 $y \in \{0, 1\}$， 不能直接用最小二乘法带入计算

而我们的拟合模型
$$
y = \frac{1}{1+e^{-(a^Tx+b)}}
$$
算出的 $y$ , 是在 $x$ 条件下作为正例的概率, 即
$$
y = p(y=1| x) = \frac{1}{1+e^{-(a^Tx+b)}} = \frac{e^{a^Tx+b}} {1+e^{a^Tx+b}}
$$
 

而 $1-y$ 是在 $x$ 条件下作为反例的概率，即
$$
1-y = p(y=0|x) = 1- \frac{1}{1+e^{-(a^Tx+b)}} = \frac{1} {1+e^{a^Tx+b}}
$$
于是我们可以通过**极大似然法**来估计 $a, b$ 的值，即求 $a, b$ 使下式最大化
$$
\sum_{i=1}^m ln(p(y_i|x_i)) = \sum_{i=1}^m [y_i(p(y=1|x)) + (1-y_i)p(y=0|x)]
$$
变换上式后，上式 最大化 等价于 下式 最小化
$$
f(W) = \sum_{i=1}^m [-y_i W^T \hat{x}_i + ln(1+ e^{W^T \hat{x}_i})]\\
\hat{x} = [x_1, x_2, ..., x_m, 1]^T, W = [a_1, a_2, ..., a_m, b]^T, y_i \in \{0, 1\}
$$
$f(W)$ 是关于 $W$ 的高阶可导连续凸函数，根据凸优化理论，可用梯度下降法，牛顿法等求最优解

求最优解 $W$ 不在对数几率二分类的关键内容，且可用多种方法求解，故不作讨论





