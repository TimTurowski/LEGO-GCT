import multiprocessing
from multiprocessing import Process


def funcA(n, m):
    result = 0
    for i in range(1, n):
        result = result + i
    m.value = result
    print("A:", result)


def funcB():
    print("B:", 10)


if __name__ == "__main__":
    data = multiprocessing.Value("i", 0)
    p = Process(target=funcA, args=(100, data,))
    p.start()
    p.join()

    print(data.value)

    print("p is alive", p.is_alive())
    """join bewirkt das solange gewartet wird bis die der Prozess beendigt ist ohne Join kann es Vorkommen das
    funcB früher Fertig ist"""
    p.join()
    print("p is alive", p.is_alive())

    p = Process(target=funcB)
    p.start()
    p.join()
