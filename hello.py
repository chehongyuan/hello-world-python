def main():
    """打印Hello World"""
    print("Hello World!")
    
    # 可选：添加一些额外信息
    print(f"当前时间: {__import__('datetime').datetime.now()}")
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