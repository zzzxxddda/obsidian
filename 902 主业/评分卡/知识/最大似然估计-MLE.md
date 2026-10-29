
---

在逻辑回归（Logit 模型）中，**最大似然估计（MLE）** 用于找到最能拟合观测数据的模型参数。下面详细解释最大似然值的计算过程，包括似然函数的构建、对数似然、参数优化算法等。

## 一、逻辑回归的模型设定

对于二分类问题，设  
- $y_i \in \{0,1\}$ 为第 $i$ 个样本的观测标签（1 表示坏样本/事件发生，0 表示好样本/事件未发生）。  
- $\mathbf{x}_i = (1, x_{i1}, x_{i2}, \dots, x_{ip})$ 为包含截距项的特征向量。  
- $\boldsymbol{\beta} = (\beta_0, \beta_1, \dots, \beta_p)$ 为模型参数。

逻辑回归假设：

$$
P(y_i = 1 | \mathbf{x}_i) = \pi_i = \frac{1}{1 + e^{-\mathbf{x}_i \boldsymbol{\beta}}}
$$

## 二、似然函数的构建

对于单个样本，其概率质量函数为：

$$
P(y_i | \mathbf{x}_i) = \pi_i^{y_i} (1 - \pi_i)^{1 - y_i}
$$

假设所有样本独立，则整个数据集的**似然函数**为：

$$
L(\boldsymbol{\beta}) = \prod_{i=1}^{n} \pi_i^{y_i} (1 - \pi_i)^{1 - y_i}
$$

## 三、对数似然函数

直接最大化似然函数乘积较困难，通常取自然对数，得到**对数似然函数**：

$$
\ell(\boldsymbol{\beta}) = \ln L(\boldsymbol{\beta}) = \sum_{i=1}^{n} \left[ y_i \ln \pi_i + (1 - y_i) \ln (1 - \pi_i) \right]
$$

代入 $\pi_i = \frac{1}{1+e^{-\mathbf{x}_i\boldsymbol{\beta}}}$，化简得：

$$
\ell(\boldsymbol{\beta}) = \sum_{i=1}^{n} \left[ y_i \mathbf{x}_i\boldsymbol{\beta} - \ln\left(1 + e^{\mathbf{x}_i\boldsymbol{\beta}}\right) \right]
$$

目标就是找到 $\boldsymbol{\beta}$ 使 $\ell(\boldsymbol{\beta})$ 最大化。这个最大值就是**模型的最大似然值**（通常指最大化后的对数似然值，即 $\ell(\hat{\boldsymbol{\beta}})$）。

## 四、优化算法：如何求解 $\hat{\boldsymbol{\beta}}$

对数似然函数没有闭式解，需要使用数值优化算法。最常用的是**牛顿-拉弗森（Newton-Raphson）** 或等价的**迭代重加权最小二乘（IRLS）**。以下是牛顿法的核心步骤。

### 1. 梯度（一阶导数）

对 $\ell(\boldsymbol{\beta})$ 求偏导：

$$
\frac{\partial \ell}{\partial \beta_j} = \sum_{i=1}^{n} x_{ij} (y_i - \pi_i)
$$

向量形式：$\nabla \ell(\boldsymbol{\beta}) = \mathbf{X}^T (\mathbf{y} - \boldsymbol{\pi})$

其中 $\mathbf{X}$ 为设计矩阵（$n \times (p+1)$），$\boldsymbol{\pi} = (\pi_1, \dots, \pi_n)^T$。

### 2. 海森矩阵（二阶导数）

$$
\frac{\partial^2 \ell}{\partial \beta_j \partial \beta_k} = - \sum_{i=1}^{n} x_{ij} x_{ik} \pi_i (1 - \pi_i)
$$

矩阵形式：$\mathbf{H} = -\mathbf{X}^T \mathbf{W} \mathbf{X}$，其中 $\mathbf{W} = \text{diag}(\pi_i(1-\pi_i))$ 是 $n \times n$ 对角权重矩阵。

### 3. 牛顿迭代公式

从初始 $\boldsymbol{\beta}^{(0)}$（通常为零向量）开始，迭代：

$$
\boldsymbol{\beta}^{(t+1)} = \boldsymbol{\beta}^{(t)} - \mathbf{H}^{-1} \nabla \ell
$$

由于 $\mathbf{H}$ 是负定的，牛顿法通常收敛很快。

实际实现中常使用 **IRLS 等价形式**：  
定义工作响应变量 $z_i = \mathbf{x}_i\boldsymbol{\beta}^{(t)} + \frac{y_i - \pi_i^{(t)}}{\pi_i^{(t)}(1-\pi_i^{(t)})}$，然后用加权最小二乘求解：

$$
\boldsymbol{\beta}^{(t+1)} = (\mathbf{X}^T \mathbf{W}^{(t)} \mathbf{X})^{-1} \mathbf{X}^T \mathbf{W}^{(t)} \mathbf{z}
$$

## 五、最大似然值的计算

迭代收敛后，得到参数估计 $\hat{\boldsymbol{\beta}}$，代入对数似然函数计算：

$$
\ell(\hat{\boldsymbol{\beta}}) = \sum_{i=1}^{n} \left[ y_i \ln \hat{\pi}_i + (1 - y_i) \ln (1 - \hat{\pi}_i) \right]
$$

其中 $\hat{\pi}_i = \frac{1}{1 + e^{-\mathbf{x}_i \hat{\boldsymbol{\beta}}}}$。

这个 $\ell(\hat{\boldsymbol{\beta}})$ 就是模型的最大对数似然值。在 `statsmodels` 中可通过 `model.llf` 获取；在 `sklearn` 的 `LogisticRegression` 中可使用 `model.score` 或 `model.predict_log_proba` 自行计算。

## 六、似然值的应用

- **似然比检验**：比较两个嵌套模型的似然值差异。  
- **AIC**：$\text{AIC} = -2\ell(\hat{\boldsymbol{\beta}}) + 2k$（$k$ 为参数个数，含截距）。  
- **BIC**：$\text{BIC} = -2\ell(\hat{\boldsymbol{\beta}}) + k\ln n$。

注意：`statsmodels` 输出的 `llf` 即是 $\ell(\hat{\boldsymbol{\beta}})$，而 AIC 计算公式中的 $-2\ell$ 也被称作 **偏差（deviance）** 的一部分。

## 七、计算注意事项

1. **数值稳定**：当 $\pi_i$ 接近 0 或 1 时，$\ln \pi_i$ 或 $\ln(1-\pi_i)$ 会趋于负无穷。通常通过剪裁（如限制 $\pi_i \in [10^{-15}, 1-10^{-15}]$）避免溢出。  
2. **收敛判断**：通常当参数变化小于某阈值（如 $10^{-6}$）或梯度足够小时停止迭代。  
3. **完全分离问题**：如果特征能完美区分 0/1，似然函数无有限最大值，算法不收敛。这时需加入正则化（如岭回归）或使用 Firth 惩罚。

## 八、示例代码（手动计算似然值）

```python
import numpy as np
from scipy.special import expit  # sigmoid函数

def log_likelihood(beta, X, y):
    """计算逻辑回归的对数似然值"""
    lin = X @ beta
    pi = expit(lin)                      # 预测概率
    # 防止 log(0) 或 log(1)
    pi = np.clip(pi, 1e-15, 1 - 1e-15)
    ll = np.sum(y * np.log(pi) + (1 - y) * np.log(1 - pi))
    return ll

# 示例数据
X = np.array([[1, 2], [1, 3], [1, 4], [1, 5]])
y = np.array([0, 0, 1, 1])
beta = np.array([-5, 1.5])   # 随意猜测的参数
print(log_likelihood(beta, X, y))  # 输出某个似然值

# 使用 statsmodels 得到最大似然值
import statsmodels.api as sm
model = sm.Logit(y, X)
result = model.fit(disp=0)
print("最大对数似然值:", result.llf)
```

## 总结

- 最大似然值的计算过程：定义似然 → 取对数 → 用牛顿法/IRLS 最大化对数似然 → 得到最优参数 → 代入计算最终似然值。
- 这个值直接用于 AIC/BIC 以及模型比较。
- 在 WOE 转换后进行的逻辑回归中，最大似然值反映 WOE 特征对目标的解释能力。

