# 第 2 天 · 题目与参考解答

## 力扣 #49 字母异位词分组 · 25 分钟

把字母种类和各自出现次数完全相同的单词放到同一组。输入只包含小写英文字母，允许空字符串和重复项。保留所有输入项，组与组之间、组内的顺序都可以变化。 [力扣原题](https://leetcode.cn/problems/group-anagrams/)

例如 `['tea', 'eat', 'bat', 'tab', 'tea', '', '']` 可以得到 `[['tea', 'eat', 'tea'], ['bat', 'tab'], ['', '']]`。

### 推荐解法 · 26 个字母计数

```python
from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)
    first_letter = ord("a")

    for word in words:
        counts = [0] * 26
        for letter in word:
            counts[ord(letter) - first_letter] += 1
        # 将可变的计数列表转成可以用作字典键的元组。
        groups[tuple(counts)].append(word)

    return list(groups.values())


class Solution:
    def groupAnagrams(self, strs):
        return group_anagrams(strs)
```

在本地练习时，把 `defaultdict` 的导入和 `group_anagrams(words)` 用到 `practice.py`，该文件的自测会直接调用这个函数。提交到力扣时使用上面带 `Solution` 类的完整代码。

1. **关键函数 `ord()`** 返回一个字符的编码。`ord(letter) - ord("a")` 把 `a` 到 `z` 映射为下标 `0` 到 `25`。扫完 `tea` 后，`a`、`e`、`t` 对应的计数各是 1，`eat` 会得到同样的计数。
2. **关键函数 `tuple()`** 把计数列表转成元组，得到可作为字典键的固定计数。**关键工具 `defaultdict(list)`** 会在首次访问某个键时创建空列表，`append()` 再把当前单词追加进去。
3. 空字符串得到全零的键，重复的单词每次都会被追加。最后 `groups.values()` 取出所有组，`list(...)` 把它们装成结果列表。

设单词数为 $n$，总字符数为 $S$，不同分组数为 $g$。平均时间复杂度为 $O(S+26n)$，固定字母表下写作 $O(S+n)$。分组字典和列表存放 $g$ 个计数键与 $n$ 个单词引用，空间为 $O(26g+n)$。

### 更短的写法 · 排序分组键

```python
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs):
        groups = defaultdict(list)
        for word in strs:
            groups["".join(sorted(word))].append(word)
        return list(groups.values())
```

**关键函数 `sorted()`** 将字符按字母排序并返回列表，**关键方法 `"".join(...)`** 用空字符串连接各个字符。`tea` 和 `eat` 都会变成 `aet`。长度为 $k$ 的单词最坏需要 $O(k\log(k+1))$ 的排序时间，另有每个单词的分组开销。

可以先用这行看输出，再用练习文件的自测核对重复项和空字符串。

```python
print(Solution().groupAnagrams(["tea", "eat", "bat"]))  # [['tea', 'eat'], ['bat']]
```

## 贝叶斯 · 20 分钟

公平硬币和偏置硬币各一枚，随机等概率选一枚抛一次。公平硬币的正面率是 $1/2$，偏置硬币的正面率是 $4/5$。观察到正面后，求所选硬币是偏置硬币的概率。 [Harvard Stat 110 条件概率与全概率课程](https://stat110.hsites.harvard.edu/youtube)

### 参考解答

设 $B$ 表示选到偏置硬币，$H$ 表示抛出正面。两种选币方式互斥且覆盖所有可能，因此总的正面概率是两条路径概率之和。

| 路径 | 选币概率 | 选中后掷出正面的概率 | 联合概率 |
|---|---:|---:|---:|
| 公平硬币且正面 | $1/2$ | $1/2$ | $1/4$ |
| 偏置硬币且正面 | $1/2$ | $4/5$ | $2/5$ |

$$
P(H)=\frac14+\frac25=\frac{13}{20},
\qquad
P(B\mid H)=\frac{P(B\cap H)}{P(H)}=\frac{2/5}{13/20}=\frac{8}{13}\approx61.54\%.
$$

先验 $P(B)=50\%$。偏置硬币更容易出现正面，因此这次观察把后验提高到约 $61.54\%$。

```python
from fractions import Fraction


def biased_coin_posterior():
    fair_and_head = Fraction(1, 2) * Fraction(1, 2)
    biased_and_head = Fraction(1, 2) * Fraction(4, 5)
    total_head = fair_and_head + biased_and_head  # 两种硬币都能掷出正面
    return biased_and_head / total_head


actual = biased_coin_posterior()
expected = Fraction(8, 13)
print(f"实际概率 {actual}，预期概率 {expected}")
assert actual == expected
```

**关键工具 `Fraction(分子, 分母)`** 创建精确分数。`Fraction(4, 5)` 表示 `0.8`，最后得到的结果会自动约分为 `8/13`。

**口述复盘**　先说分子代表哪条路径，再说为什么分母要同时包含两种硬币掷出正面的路径。
