# Quant ETF 学习项目

用一只宽基 ETF 练习行情处理、收益核算和回测设计。

## 学习记录

每次练习把题意、提示、参考答案、逐步讲解和易错点放在一起。算法题附代码、自测与复杂度，概率题附假设和推导。

- [第 1 天 · 标的核对和五行研究设计](day-01/README.md)
- [第 1 天 · 力扣和绿皮书题目与参考答案](day-01/exercises.md)
- [第 1 天 · Python 练习和自测](day-01/practice.py)
- [第 2 天 · ETF 历史行情与复权讲义](day-02/README.md)
- [第 2 天 · 力扣和贝叶斯题目与参考答案](day-02/exercises.md)
- [第 2 天 · Python 练习和自测](day-02/practice.py)
- [第 3 天 · 日期索引与行情清洗讲义](day-03/README.md)
- [第 3 天 · 力扣和组合计数题目与参考答案](day-03/exercises.md)
- [第 3 天 · Python 练习和自测](day-03/practice.py)

## 运行第 1 天代码

使用 Python 3.15。在仓库根目录打开 Windows PowerShell，有 `py` 命令时可按以下步骤运行。已创建 `.venv` 时，从最后一行运行即可。

```powershell
py -3.15 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe day-01\return_demo.py
```

如果 Python 启动器不可用，用本机 Python 3.15 的 `python.exe` 路径执行 `-m venv .venv`。示例价格是为了复现手算而设定的模拟数据。

## 自测练习

在 `day-01/practice.py` 中填写 `two_sum` 和 `coin_game_counts`。从仓库根目录运行下面的命令。空白题会显示「待完成」，答案正确会显示「自测通过」。

```powershell
& .\.venv\Scripts\python.exe day-01\practice.py
```
