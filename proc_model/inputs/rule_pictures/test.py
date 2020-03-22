import matplotlib.image as img
import random
import numpy as np

S=10


def make_tiles(size):

    colors = [np.array([255, 0, 0], dtype=np.uint8),
              np.array([0, 255, 0], dtype=np.uint8),
              np.array([0, 0, 255], dtype=np.uint8)]

    tiles = [np.tile(col, (size, size)).reshape((size, size, 3)) for col in colors]
    return tiles


# print(dens.shape)

def make_rule_image(height, length, tile):

    rows = height//tile + 1
    cols = length//tile + 1

    color_map = np.random.choice([0, 1, 2], size=(rows, cols), replace=True, p=(0.35, 0.3, 0.35))
    print(color_map)

    tiles = make_tiles(tile)
    pic = np.array([[tiles[c] for c in r] for r in color_map])
    pic = pic.reshape((rows * tile * cols * tile, 3))
    # print(pic1.shape)
    pic = pic.reshape((rows * tile, cols * tile, 3))
    # print(pic.shape)
    #
    img.imsave('tiles_large.png', pic)

    # print(red.dtype)

make_rule_image(4000, 4000, 100)