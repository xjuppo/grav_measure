import parser, util
import matplotlib.pyplot as plt

def plot_csv(path: str):
    # Read values from csv file and plot values
    values: dict = parser.read_from_file(path)
    x = values["time"]
    time, std_y = util.movstd(x, values["TgF"])
    
    plt.plot(x, values["TgF"], label="TgF")
    plt.plot(time, std_y)

    i1, i2 = util.find_fall_time(x, values["TgF"])
    plt.axvline(x[i1], color = "r")
    plt.axvline(x[i2], color = "r")

    plt.show()