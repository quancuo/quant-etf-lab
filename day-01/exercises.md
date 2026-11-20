# Day 01 题目与参考解答

## 力扣 #1 两数之和 · 25 分钟

给定整数数组 `nums` 和整数 `target`，找出两个不同的下标，使对应元素之和等于 `target`。题目保证存在唯一有效答案，下标顺序任意。 [力扣原题](https://leetcode.cn/problems/two-sum/)

| 自测数组 | 目标 | 一组合法输出 |
|---|---:|---|
| `[6, 6]` | 12 | `[0, 1]` |
| `[-4, 9, 6, 2]` | 5 | `[0, 1]` |
| `[4, 1, 7]` | 8 | `[1, 2]` |

先用 5 分钟读题，8 分钟尝试双循环，8 分钟改写为字典查找，最后 4 分钟跑自测并复述复杂度。

### 参考解答

扫描到下标 `i` 时，字典里只保留此前扫描到的值及其下标。先查补数 `target - value`，查不到再记录当前值，这样能保证两个下标不同，也允许用两个相同的值凑出目标。

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for index, value in enumerate(nums):
            complement = target - value
            if complement in seen:
                return [seen[complement], index]
            seen[value] = index
        raise ValueError("未找到有效数对")
```

字典操作的平均时间为 $O(1)$，整体期望时间为 $O(n)$，额外空间为 $O(n)$。用 `[4, 1, 7]` 检查为什么要先查询再写入。

## 绿皮书 §4.1 抛硬币游戏 · 20 分钟

按 Xinfeng Zhou 的 *A Practical Guide to Quantitative Finance Interviews* 中 *Coin toss game* 定位，2008 版印刷页码为 61。题意用自己的话概括如下。 [绿皮书目录](https://openlibrary.org/books/OL27082125M/Practical_guide_to_quantitative_finance_interviews)

甲独立抛公平硬币 $n+1$ 次，乙独立抛公平硬币 $n$ 次，两人的抛掷也相互独立。问甲的正面次数严格大于乙的概率。

先花 5 分钟列 $n=1$ 的样本空间，10 分钟找一般情形的配对办法，最后用 5 分钟关掉答案、口述推导。

### 参考解答

当 $n=1$ 时，用 `H` 表示正面、`T` 表示反面。前两位属于甲，最后一位属于乙。每个序列的概率都是 $(1/2)^3=1/8$。

| 结果 | 甲的正面数 | 乙的正面数 | 甲严格领先 |
|---|---:|---:|---|
| `HHH` | 2 | 1 | 是 |
| `HHT` | 2 | 0 | 是 |
| `HTH` | 1 | 1 | 否 |
| `HTT` | 1 | 0 | 是 |
| `THH` | 1 | 1 | 否 |
| `THT` | 1 | 0 | 是 |
| `TTH` | 0 | 1 | 否 |
| `TTT` | 0 | 0 | 否 |

一般地，设 $X$、$Y$ 分别是甲、乙的正面数，记 $D=X-Y$。将整个序列的每次抛掷结果正反互换，甲、乙的正面数变为 $n+1-X$ 和 $n-Y$，所以差值变为

$$
(n+1-X)-(n-Y)=1-D.
$$

每个原序列与它的翻面序列等概率，翻面两次回到原序列。由于 $D$ 是整数，$D\ge 1$ 的严格领先结果与 $D\le 0$ 的未领先结果一一配对。因此甲严格领先的概率为 $\boxed{1/2}$。平局属于未领先，例如 $D=0$ 会和 $D=1$ 配对。

**口述复盘**　为什么序列等概率？翻面后为什么是 $1-D$？平局归到哪边？
