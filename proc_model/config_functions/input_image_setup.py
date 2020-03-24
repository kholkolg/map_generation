import matplotlib.image as mpimg
import proc_model
import os
import matplotlib.pyplot as plt


def input_image_setup(rule_image_name, density_image_name):
    '''
    Loads the rule-image and population-density-image from the filesystem.
    Saves the density image in /temp/ folder so that it could be ensured.

    Parameters
    ----------
    rule_image_name: String
        Name of the rule_image specified in Parameters
    density_image_name: String
        Name of the density_image specified in Parameters

    Returns
    --------
    rule_img: np.ndarray
        Rule-image as numpy array
    density_img: np.ndarray
        Density-image as numpy array
    '''

    #TODO: Document

    path=os.path.dirname(proc_model.__file__)
    print('input_image_setup')
    rule_img = mpimg.imread(path+"/inputs/rule_pictures/"+rule_image_name)
    density_img = mpimg.imread(path+"/inputs/density_pictures/"+density_image_name)
    # print(density_image_name, density_img)

    plt.imsave(path+"/temp/"+density_image_name.split(".")[0]+"diffused.png", density_img, cmap='gray')


    rule_img*=255
    density_img*=255
    return rule_img, density_img
