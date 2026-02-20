from datetime import date, datetime

"""内部助手："""
def _to_date(d):
    """内部助手：将输入转换为 `datetime.date`。

    支持：
    - `datetime.date`
    - `datetime.datetime`
    - ISO 格式字符串（例如 '2026-01-11' 或 '2026-01-11T15:30:00'）
    """
    if isinstance(d, date) and not isinstance(d, datetime):
        return d
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, str):
        try:
            return date.fromisoformat(d)
        except Exception:
            try:
                return datetime.fromisoformat(d).date()
            except Exception:
                raise ValueError("不支持的日期字符串格式，请使用 'YYYY-MM-DD' 或 ISO datetime")
    raise TypeError("输入必须是 date、datetime 或 ISO 格式的字符串")


def days_between(date1, date2):
    """返回两个日期之间的绝对天数（整数）。

    参数可以是 `datetime.date`、`datetime.datetime`，或 ISO 格式字符串。
    例子：`days_between('2026-01-01', '2026-01-11')` -> 10
    """
    d1 = _to_date(date1)
    d2 = _to_date(date2)
    return abs((d2 - d1).days)


def main():
    """打印Hello World并展示 `days_between` 的示例。"""
    print("Hello World!")

    # 可选：添加一些额外信息
    print(f"当前时间: {datetime.now()}")
    print(f"Python版本: {__import__('sys').version}")
    print(f"操作系统: {__import__('platform').platform()}")
    # 打印“谢谢！”
    print("谢谢！")
    # 打印电脑配置信息
    print("电脑配置信息：")
    print(f"  CPU: {__import__('platform').processor()}")
    # print(f"  内存: {__import__('psutil').virtual_memory().total / (1024**3):.2f} GB")  
    # 结束时返回0表示成功
    return 0


if __name__ == "__main__":
    main()

    # 示例：计算两个日期之间的天数
    print('\n示例:')
    print("days_between('2026-01-01', '2026-01-11') ->", days_between('2026-01-01', '2026-01-11'))
    # 也可以传入 datetime 对象
    print("days_between(datetime.now(), datetime.now()) ->", days_between(datetime.now(), datetime.now()))