import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from random import randint

x = np.arange(0, 2*np.pi, 0.1)
y = np.sin(x)

fig, axes = plt.subplots(nrows=6)

styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']


def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]


lines = [plot(ax, style) for ax, style in zip(axes, styles)]


def animate(i):
    k = randint(1, 100)
    for j, line in enumerate(lines, start=1):
        line.set_ydata(np.sin(j*x + k/10.0))
    return lines


# We'd normally specify a reasonable "interval" here...
ani = animation.FuncAnimation(fig, animate, range(1, 200000),
                              interval=10, blit=True)
plt.show()
