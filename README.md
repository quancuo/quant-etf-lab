# Quant ETF 学习项目

用一只宽基 ETF 练习行情处理、收益核算和回测设计。

## 学习记录

- [第 1 天 · 标的核对和五行研究设计](day-01/README.md)
- [第 1 天 · 力扣和绿皮书题目与参考答案](day-01/exercises.md)

## 运行第 1 天代码

使用 Python 3.15。在仓库根目录打开 Windows PowerShell，有 `py` 命令时可按以下步骤运行。已创建 `.venv` 时，从最后一行运行即可。

```powershell
py -3.15 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe day-01\return_demo.py
```

如果 Python 启动器不可用，用本机 Python 3.15 的 `python.exe` 路径执行 `-m venv .venv`。示例价格是为了复现手算而设定的模拟数据。
