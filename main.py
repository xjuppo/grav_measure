import src.util as util
import src.parser as parser
import os
import matplotlib.pyplot as plt

times = []

for filename in os.listdir("data/"):
    values = parser.read_from_file("data/"+filename)
    time = values["time"]
    tgf = values["TgF"]
    i1, i2 = util.find_fall_time(time, tgf, window_size=0.4, start=0.24, end=-0.1)
    plt.plot(time, tgf)
    plt.axvline(time[i1])
    plt.axvline(time[i2])
    plt.show()