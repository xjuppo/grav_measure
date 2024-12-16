import parser, util
import matplotlib.pyplot as plt

def plot_csv(path: str):
    # Read values from csv file and plot values
    values: dict = parser.read_from_file(path)
    x = values["time"]
    gFx, = plt.plot(x, values["gFx"], label="gFx")
    gFy, = plt.plot(x, values["gFy"], label="gFy")
    gFz, = plt.plot(x, values["gFz"], label="gFz")
    tgF, = plt.plot(x, values["TgF"], label="TgF")
    plt.legend([gFx, gFy, gFz, tgF], ["gFx", "gFy", "gFz", "TgF"])
    plt.show()

plot_csv("samples/1.csv")