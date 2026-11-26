# 第 3 天 · 题目与参考解答

## 力扣 #128 最长连续序列 · 25 分钟

在整数列表中找出最长的一段相邻值相差 1 的序列，返回长度。元素在原列表中的位置和顺序不限，重复值只算一次。空列表返回 `0`。 [力扣原题](https://leetcode.cn/problems/longest-consecutive-sequence/)

例如 `[14, 4, 2, 5, 2, 3]` 含有连续的 `2, 3, 4, 5`，答案是 `4`。

```python
class Solution:
    def longestConsecutive(self, nums):
        values = set(nums)
        longest = 0

        for start in values:
            if start - 1 in values:
                continue  # 有前驱的值在序列中间，跳过它。

            end = start
            while end + 1 in values:
                end += 1
            longest = max(longest, end - start + 1)

        return longest
```

- **关键函数 `set(nums)`** 将数组转换成集合，保留不同的整数。`x in values` 检查集合里有没有 `x`，平均查询时间为 $O(1)$。
- **关键语句 `continue`** 跳过本轮外层循环。例子里 `3`、`4`、`5` 都有前一个整数，所以由该段起点 `2` 负责扫描。
- **关键语句 `while`** 在条件成立时重复执行。`end` 从 `2` 走到 `5`，查到 `6` 缺失时结束。`end - start + 1` 把起点和终点都算进去，得到长度 `4`。
- **关键函数 `max()`** 从已有的最长长度和这一段的长度里取较大值。集合遍历的顺序可以变化，最后得到的最大长度相同。

每个连续段只从起点向右扫一次。所有 `while` 加起来最多成功推进不同值的个数，因此平均时间为 $O(n)$，额外空间为 $O(n)$。

把下面一行接在 `Solution` 的代码后面，可以核对上面的例子。

```python
print(Solution().longestConsecutive([14, 4, 2, 5, 2, 3]))  # 4
```

**自测**　解释为什么 `[8, 8, 8]` 返回 `1`，以及 `[-3, -1, 1, -2]` 返回 `3`。

## 组合计数 · 20 分钟

从 8 个不同的人中等概率抽取 3 人，不放回。求指定的甲、乙两人都被抽中的概率。

### 参考解答

每个无序三人组等概率，所以总情况数是 $\binom{8}{3}=56$。要同时包含甲和乙，只需从其余 6 人中选择第 3 人，有 $\binom{6}{1}=6$ 个满足条件的三人组。因此

$$
P(\text{甲、乙都被抽中})=\frac{\binom{6}{1}}{\binom{8}{3}}=\frac{3}{28}\approx10.71\%.
$$

也可以先算甲被抽中的概率 $3/8$。已知甲在组里，还剩 7 人和 2 个名额，乙入选概率是 $2/7$。相乘得到相同的 $3/28$。

```python
from fractions import Fraction
from math import comb


def fixed_pair_probability():
    total = comb(8, 3)
    favorable = comb(6, 1)
    return Fraction(favorable, total)


answer = fixed_pair_probability()
assert answer == Fraction(3, 8) * Fraction(2, 7)
print(answer)  # 3/28
```

**关键函数 `comb(n, k)`** 计算从 `n` 个对象中选 `k` 个的组合数，只看选中了哪些对象。**关键工具 `Fraction(分子, 分母)`** 保留精确分数并自动约分。 [Python `math.comb`](https://docs.python.org/3/library/math.html#math.comb) · [Python `fractions`](https://docs.python.org/3/library/fractions.html#fractions.Fraction)

**口述复盘**　为什么分子只剩一个名额？给定甲入选后，为什么乙入选是 $2/7$？
