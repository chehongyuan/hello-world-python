def main():
    """打印Hello World并展示 `days_between` 的示例。"""
    print("Hello World!")

    # 可选：添加一些额外信息
    print(f"当前时间: {__import__('datetime').datetime.now()}")
    print(f"Python版本: {__import__('sys').version}")
    
    return 0


if __name__ == "__main__":
    main()