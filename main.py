import src.util as util
import src.parser as parser
import os
import matplotlib.pyplot as plt

times = []

for filename in os.listdir("data/"):
    values = parser.read_from_file("data/"+filename)
    time = values["time"]
    tgf = values["TgF"]
    time, std_y = util.movstd(time, tgf, 0.4)
    time, std_y2 = util.movstd(time, std_y, 0.05)
    i1, i2 = util.find_fall_time_std(time, tgf, window_size=0.4, start=1.2, end=2.1)
    plt.plot(time, tgf)
    plt.plot(time, std_y)
    plt.plot(time, std_y2)
    plt.axvline(time[i1])
    plt.axvline(time[i2])
    plt.show()