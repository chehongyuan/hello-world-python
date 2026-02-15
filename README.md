# Hello World Python 程序

这是一个简单的Python程序，演示如何用VSCode和GitHub进行版本控制。

## 功能
- 打印"Hello World!"
- 显示当前时间
- 显示Python版本
- 获取东京实时天气
- 提供纳斯达克指数双均线（20/100）金叉死叉策略示例脚本

## 运行方法

### 1) 运行原示例
```bash
python hello.py
```

### 2) 运行纳斯达克量化策略
```bash
pip install -r requirements.txt
python nasdaq_strategy.py --symbol ^IXIC --start 2015-01-01 --end 2026-01-01
```

策略规则：
- 20日均线上穿100日均线（金叉）时买入。
- 20日均线下穿100日均线（死叉）时卖出。
