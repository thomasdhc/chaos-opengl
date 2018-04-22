import fire
import numpy as np
import matplotlib.pyplot as plt


def main():
    value_arr = []
    r = 1.5
    old_x = 0.01
    end_rng = 20

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, end_rng, 1.))
    ax.set_yticks(np.arange(0, 1., 0.1))

    for _ in range(0, end_rng):
        new_x = r * old_x * (1 - old_x)
        old_x = new_x
        value_arr.append(new_x)
    
    plt.plot(value_arr)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    fire.Fire(main) 