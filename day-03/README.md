# 第 3 天 · 时间索引、行情清洗与缺失判断

学习目标是把 D2 的 510300 不复权日线整理成 `date、symbol、open、high、low、close、volume`，再用日期索引判断：今天没看到收盘价，具体是哪一种情况？

| 时间 | 任务 |
| --- | --- |
| 45 分钟 | 学日期转换、排序、查重和缺失检测 |
| 90 分钟 | 复跑真实快照和练习副本，逐段读懂清洗代码 |
| 25 分钟 | 力扣 #128 最长连续序列 |
| 20 分钟 | 组合计数 · 8 人抽 3 人，指定两人都被选中 |

## 课程 · 45 分钟

- **15 分钟** · C02 看第三周「数据分析之概要」，重点是单元 7「Pandas库入门」和单元 8「Pandas数据特征分析」。能识别 DataFrame 的行、列和索引即可。 [北京理工大学中文 MOOC](https://www.icourse163.org/course/bit-1001870002) · [含单元名称的课程大纲](https://www.icourse163.org/course/BIT-1001870002?tid=1468336445)
- **15 分钟** · 跟做时间戳和日期索引的例子。把两个字符串日期用 `pd.to_datetime()` 转换，再用 `set_index("date").sort_index()` 得到按时间排列的表。 [Joyful Pandas 中文时序教程](https://inter.joyfulpandas.datawhale.club/Content/ch10.html)
- **15 分钟** · 看排序与缺失的例子，重点辨认「这一行在表里但有空字段」和「日期对应的整行都没出现」。 [中文排序教程](https://inter.joyfulpandas.datawhale.club/Content/ch2.html) · [中文缺失数据教程](https://inter.joyfulpandas.datawhale.club/Content/ch7.html)

## 实操结果

脚本读取 [D2 的真实快照](../day-02/data/510300_20250616_20250620.json)，整理出 510300 的五行不复权 OHLCV。检查结果为 **5 行有效，0 个重复键，0 行异常，0 个应有交易日缺行**。其中 6 月 18 日的真实收盘价是 **3.904 元**，6 月 19 日是 **3.873 元**。

另外在副本中打乱行序、复制 6 月 17 日、删掉 6 月 18 日、把 6 月 19 日的收盘价改成 0。重新执行相同的清洗流程，就能同时看到下面这些情况。

| 日期 | 审核结果 | 判断依据 |
| --- | --- | --- |
| 2012-05-25 | 上市前，OHLCV 留空 | 510300 于 2012-05-28 在上交所上市。 |
| 2025-06-02 | 休市，OHLCV 留空 | 星期一，但上交所端午休市。 |
| 2025-06-17 | 检出重复，保留一行 | 副本内同一标的同一天的 OHLCV 完全相同。 |
| 2025-06-18 | 交易日缺行，OHLCV 留空 | 属于预期交易日，副本里没有收到这一行。 |
| 2025-06-19 | 异常行已剔除，OHLCV 留空 | 副本收到一行，收盘价已被人为改成 0。 |
| 2025-06-21、22 | 休市，OHLCV 留空 | 周六、周日休市。 |

日期判定分别依据基金上市资料和上交所的节假日安排。这里的交易日范围只覆盖本课选定的日期。 [510300 基金资料概要](https://www.sse.com.cn/disclosure/fund/announcement/c/new/2024-11-22/510300_20241122_7N07.pdf) · [上交所 2025 年休市安排](https://www.sse.com.cn/disclosure/announcement/general/c/c_20241223_10767108.shtml)

## 教程 · 按运行顺序读代码

### 1. 读快照并整理列

`load_prices()` 从 D2 JSON 取出 `unadjusted` 响应，核对标的和复权口径。**关键方法 `split(",")`** 把日线字符串拆成列表，`pd.DataFrame(..., columns=...)` 给每个位置加上列名。代码将 `symbol` 保留为字符串，选择 `date、symbol、OHLCV` 七列，其中 OHLCV 依次是开盘、最高、最低、收盘、成交量。

### 2. 统一数据类型，找出重复记录

`clean_prices()` 先转换日期和数字。**关键函数 `pd.to_datetime()`** 将日期字符串变成时间戳。**关键函数 `pd.to_numeric(..., errors="coerce")`** 把无法转成数字的值标成缺失，便于随后和其他异常一起排查。

```python
duplicates = prices.loc[prices.duplicated(subset=KEY, keep=False), KEY]
prices = prices.drop_duplicates()
```

**关键方法 `duplicated()`** 返回一列布尔值。`KEY` 是 `["symbol", "date"]`，`keep=False` 会把同组的所有副本标为 `True`。**关键方法 `drop_duplicates()`** 在这里用于移除清洗列完全一样的额外副本。同一天若两条记录的价格或成交量不同，去除完全相同的副本后仍能检出重复键，脚本会报错并给出对应日期，留待回查。

### 3. 拦下异常行情，再建立日期索引

```python
nonpositive = ohlc.le(0).any(axis=1)
clean = prices.loc[~invalid].set_index("date").sort_index()
```

**关键方法 `.le(0)`** 判断每格是否小于等于零。**关键参数 `.any(axis=1)`** 沿行检查，只要当天的开盘、最高、最低、收盘任意一个为非正，这行就需要剔除。脚本还检查数字缺失、无穷大、最高最低价关系和负成交量。**关键方法 `set_index("date")`** 把日期变成行标签，`sort_index()` 再按标签从早到晚排序。

### 4. 用独立交易日表查缺，再展开审计表

```python
received_dates = clean.index.union(rejected_dates)
missing_dates = SESSIONS.difference(received_dates)
report = clean.reindex(AUDIT_DATES)
```

- **`.union()`** 把有效日和收到坏行的日期合到一起，得到所有实际收到过行的日期。
- **`.difference()`** 求日期差集。预期交易日减去实际收到的日期，就剩下交易日缺行。比如副本 6 月 18 日完全缺一行，6 月 19 日有一行但未通过校验。
- **`.reindex()`** 按指定日期展开观察表。没有有效行情的日期留下空值，再根据交易日、上市日和校验结果填入 `status`。这里保留空值。正式回测接入完整交易日历，遇到交易日缺行时再按数据源覆盖范围、标的停牌情况等排查原因。 [pandas 日期索引文档](https://pandas.pydata.org/docs/user_guide/timeseries)

### 5. 运行并核对结果

在 VS Code 打开 `quant-etf-lab`，从项目根目录的 PowerShell 终端运行。实操复跑使用本地快照。

```powershell
& .\.venv\Scripts\python.exe .\day-03\clean_ohlcv.py
```

先确认第一段打印五行真实数据，再确认第二段的重复日是 6 月 17 日、异常日是 6 月 19 日、缺行日是 6 月 18 日。练习时可以在 `audit_dates()` 里分别打印 `SESSIONS`、`received_dates` 和 `missing_dates`，直接观察日期差集是怎样算出来的。

## 两道题 · 45 分钟

打开 [独立练习](practice.py) 完成两个函数，然后用 [题目与带注释的答案](exercises.md) 对照。两道题分别练习集合查找和组合计数。

```powershell
& .\.venv\Scripts\python.exe .\day-03\practice.py
```
