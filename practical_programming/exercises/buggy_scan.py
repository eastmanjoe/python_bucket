def double_preceding(values):
    for i in range(len(values)):
        print i, values[i]

    if values == []:
        pass  # do nothing to the empty list
    else:
        temp = values[0]
        values[0] = 0
        for i in range(1, len(values)):
            values[i] = 2 * temp
            temp = values[i]

    for i in range(len(values)):
        print i, values[i]
