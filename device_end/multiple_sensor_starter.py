import multiprocessing
def worker(num):
    """子进程要执行的代码"""
    print(f"子进程 {num} 开始执行")
    # 这里可以执行一些耗时的操作
    print(f"子进程 {num} 执行结束")

if __name__ == '__main__':
    # 创建 3 个子进程
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(i,))
        p.start()