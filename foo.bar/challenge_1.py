def answer(x, y):
    for v in x:
        if v not in y:
            return v

    for v in y:
        if v not in x:
            return v


if __name__ == '__main__':
    x = [14, 27, 1, 4, 2, 50, 3, 1]
    y = [2, 4, -4, 3, 1, 1, 14, 27, 50]

    print answer(x, y)
