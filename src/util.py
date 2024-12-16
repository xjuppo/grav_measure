import math

def mean(data: list[float]) -> float:
    '''
    Calculates mean of a list of values. If the list is empty
    the number of values is considered as 1

    Args:
        data (list[float]): list of values
    
    Returns:
        float: mean value
    '''
    return float(sum(data))/float(max(1, len(data)))

def std(data: list[float]) -> float:
    '''
        Calculates standard deviation of a list of values. If the list is empty
        the number of values is considered as 1

        Args:
            data (list[float]): list of values
        
        Returns:
            float: standard deviation
    '''
    mval = mean(data)
    variance = float(sum([(e-mval)**2 for e in data]))/float(max(1, len(data)))
    return math.sqrt(variance)

def movstd(x: list[float], y: list[float], window_size: float = 0.4) -> tuple[list[float]]:
    '''
        Calculates the standard deviation of a sliding window for each value of y.
        The sliding window is calculated from the value of x[i] to the index with value
        x[i] + window_size

        Args:
            x (list[float]): x-axis values
            y (list[float]): y-axis values
        
        Optional Args:
            window_size: the size of the window (calculated on the x-axis values), default: 0.4
        
        Returns:
            list[float], list[float]: returns the x list given as input and the calculated values
    '''
    res_y: list[float] = []
    for i in range(len(x)):
        window_values = []
        j = 0
        # Set values into the window based on the window_size parameter
        while (x[i+j]-x[i]) < window_size:
            window_values.append(y[i+j])
            j += 1
            if i+j >= len(x):
                break
        # Caculate std
        res_y.append(std(window_values))
    return x, res_y

def derivative(x: list[float], y: list[float]) -> tuple[list[float]]:
    '''
    Calculates the discrete first-order derivative of the y values

    Args:
        x (list[float]): x-axis values
        y (list[float]): y-axis values
    
    Returns:
        list[float], list[float]: returns the x list given as input and the calculated values
    '''
    der_y: list[float] = []
    for i in range(len(x)-1):
        dy = (y[i+1] - y[i])
        der_y.append(dy)
    der_y.append(y[-1])
    return x, der_y

def find_interval(values: list[float], first: float, second: float, first_falling=False, second_falling=False):
    i1 = 0
    i2 = 0
    found = False
    for i in range(len(values)):
        if not found:
            i1 = i
        i2 = i
        if not found:
            if first_falling and values[i] <= first and values[i-1] >= first:
                found = True
            if not first_falling and values[i] >= first and values[i-1] <= first:
                found = True
        if found:
            if second_falling and values[i] <= second and values[i-1] >= second:
                break
            if not second_falling and values[i] >= second and values[i-1] <= second:
                break
    return i1, i2

def find_closest_between(values: list[float], first: float, second: float) -> tuple[int]:
    '''
    Finds the closest interval between two threshold values from the input list

    Args:
        values (list[float]): input values
        first (float): the first threshold
        second (float): the second threshold

    Returns:
        int, int: returns the first and last index of the found interval 
    '''
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

def find_fall_time_dstd(time: list[float], values: list[float], window_size = 0.4, start = 0.25, end = -0.12) -> tuple[int]:
    '''
        Finds the fall time from the given x-axis values and y-axis values
        The approach is based on the following steps:
        - Calculate movstd of input values (movstd)
        - Calculate first-order discrete derivative of the movstd output
        - Find closest range between two values (start, end)

        Args:
            time (list[float]): time-axis values
            values (list[float]): y-axis values

        Optional Args:
            window_size (float): size of window used for movstd function, default = 0.4
            start (float): start of the falling interval (positive -> increasing std), default = 0.25
            end (float): end of the falling interval (negative -> decreasing std), default = -0.12

        returns:
            int, int: start and end indices of the falling interval 
    '''
    time, std_y = movstd(time, values, window_size=window_size)
    time, stdder_y = derivative(time, std_y)
    i1, i2 = find_closest_between(stdder_y, start, end)
    return i1, i2

def find_fall_time_std(time: list[float], y: list[float], window_size: float = 0.4, start: float = 2.5, end: float = 2.5):
    time, std_y = movstd(time, y, window_size=window_size)
    found_start = False
    i1 = 0
    i2 = 0
    for i in range(len(time)):
        if not found_start:
            i1 = i
        i2 = i
        if std_y[i] >= start and std_y[i-1] <= start and not found_start:
            found_start = True
        if std_y[i] <= end and std_y[i-1] >= end and found_start:
            break
    return i1, i2