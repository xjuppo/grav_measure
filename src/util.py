import math

def mean(data: list[float]) -> float:
    """
        Evaluates mean value from a list of float values
    """
    return float(sum(data))/float(max(1, len(data)))

def std(data: list[float]) -> float:
    """
        Evaluates standard deviation from a list of float values
    """
    mval = mean(data)
    dev = [(e-mval)**2 for e in data]
    return math.sqrt(float(sum(dev))/float(max(1, len(data))))

def movstd(x: list[float], y: list[float], window_size: float = 0.4) -> tuple[list[float]]:
    """
        Evaluates the standard deviation of a 2-dimensional space with a moving window of size window_size
        returns:
         - the input x
         - the output y
    """
    res_y: list(float) = []
    for i in range(len(x)):
        window_values = []
        j = 0
        # Add all values contained in the window into the list
        while (x[i+j]-x[i]) < window_size:
            window_values.append(y[i+j])
            j += 1
            if i+j >= len(x):
                break
        # Caculate std
        res_y.append(std(window_values))
    return x, res_y

def derivative(x: list[float], y: list[float]) -> tuple[list[float]]:
    """
        Evaluates first-order derivative of a 2-dimensional space
    """
    der_y: list[float] = []
    for i in range(len(x)-1):
        dy = (y[i+1] - y[i])
        der_y.append(dy)
    der_y.append(y[-1])
    return x, der_y

def find_closest_between(values, first: float, second: float):
    i1 = 0
    i2 = len(values)-1
    i = 0
    j = len(values)-1
    while i < len(values):
        if first >= 0:
            if values[i] > first:
                i1 = i
        else:
            if values[i] < first:
                i1 = i
        i += 1

    while j > i1:
        if second >= 0:
            if values[j] > second:
                i2 = j
        else:
            if values[j] < second:
                i2 = j
        j -= 1

    return i1, i2

def find_fall_time(time: list[float], values: list[float], window_size = 0.4, start = 0.25, end = -0.12) -> tuple[int]:
    """
        Find fall time from input time and values
        The approach is based on the following steps:
        - Evaluate moving-window std of input values (movstd)
        - Evaluate first-order discrete derivate of the movstd output
        - Find closest range between two values (start, end)

        Customizable parameters:
        - window_size: size of window used during movstd function, default = 0.4
        - start: start of the falling interval (positive -> increasing std, happens when the fall starts)
        - end: end of the falling interval (negative -> decreasing std, happens when peak is reached)

        returns:
        - indices of start and end index in the time list
    """
    time, std_y = movstd(time, values, window_size=window_size)
    time, stdder_y = derivative(time, std_y)
    i1, i2 = find_closest_between(stdder_y, start, end)
    return i1, i2