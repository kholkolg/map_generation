import matplotlib.image as img
import numpy as np

from proc_model.additional_stuff.Singleton import Singleton



def make_rgb_tiles(size):
    colors = [np.array([255, 0, 0], dtype=np.uint8),
              np.array([0, 255, 0], dtype=np.uint8),]
              # np.array([0, 0, 255], dtype=np.uint8)]

    tiles = [np.tile(col, (size, size)).reshape((size, size, 3)) for col in colors]
    return tiles


def make_picture(color_map, tiles):
    rows = [np.concatenate([tiles[c] for c in r], axis=1) for r in color_map]
    pic = np.concatenate(rows, axis=0)
    return pic


def generate_images(height, length, tile, path):
    return


#TODO probabilities
def make_rule_image(height, length, tile, filename=None):
    """

    :param height:
    :param length:
    :param tile:
    :param filename:
    :return:
    """

    rows = height//tile+1
    cols = length//tile+1

    color_map = np.random.choice([0, 1], size=(rows, cols), replace=True) #p=(0.35, 0.3, 0.35)
    # print(color_map)

    tiles = make_rgb_tiles(tile)
    pic = make_picture(color_map, tiles)
    # print(pic.shape)
    pic = pic.reshape((rows * tile, cols * tile, 3))
    # print(pic.shape)
    if filename:
        img.imsave(filename, pic)
    return pic

def make_bw_tiles(size):
    # shades = [np.array([255, 0, 0], dtype=np.uint8),
    #           np.array([0, 255, 0], dtype=np.uint8),
    #           np.array([0, 0, 255], dtype=np.uint8)]
    #
    # shades = [[0, 0, 0], [25,25,25], [50, 50, 50] ...., [250,250, 250]]
    # print(size)
    shades = np.array([[i for _ in range(3)] for i in range(10)], dtype=np.uint8)
    # print(shades)
    tiles = [np.tile(col, (size, size)).reshape((size, size, 3)) for col in shades]

    return tiles


def make_dens_image(height, length, tile, filename=None):
    """

    :param height:
    :param length:
    :param tile:
    :param filename:
    :return:
    """

    rows = height//tile+1
    cols = length//tile+1

    color_map = np.random.choice(range(10), size=(rows, cols), replace=True)
    # print(color_map)

    tiles = make_bw_tiles(tile)
    pic = make_picture(color_map, tiles)
    # print(pic.shape)
    pic = pic.reshape((rows * tile, cols * tile, 3))
    # print(pic.shape)
    if filename:
        img.imsave(filename, pic)
    return pic


if __name__ == '__main__':
    #TODO input args (size, granularity, probabilities or prevailing type (grid, radial, organic)
    make_rule_image(1000, 1000, 100,'tiles_large.png')