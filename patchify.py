from __future__ import division, print_function

from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
try:
    import cPickle as pickle
except ImportError:
    import pickle

from PIL import Image
import numpy as np
from tqdm import tqdm


CIFAR10_PATH = 'cifar-100-python/train'


# Utility functions
def load_cifar(path=CIFAR10_PATH):
    with open(path, 'rb') as fo:
        try:
            dict_ = pickle.load(fo, encoding='bytes')
        except:
            dict_ = pickle.load(fo)
    images = dict_[b'data'].reshape([-1, 3, 32, 32])
    images = images.transpose([0, 2, 3, 1])
    return images 


def give_best_image(patch, images):
    patch = patch.mean((0, 1))
    images_mean = images.mean((1, 2))
    # TODO: find better function
    diff = np.abs(images_mean - patch) 
    diff = diff.sum(-1)

    args = diff.argsort(-1)
    args = args[:10]
    argmin = np.random.choice(args)
    best_image = images[argmin]
    return best_image


def patchify(source_path, output_path, bank, scale, n_processes=None):
    n_images, bank_h, bank_w, _ = bank.shape

    # source load and resize
    source = Image.open(source_path)
    source = source.convert('RGB')
    W, H = source.size
    W = int(W * scale)
    H = int(H * scale)
    source = source.resize([W, H], Image.ANTIALIAS)
    n_patches_h = H // bank_h
    n_patches_w = W // bank_w
    W_new = bank_w * n_patches_w
    H_new = bank_h * n_patches_h
    source = source.crop([0, 0, W_new, H_new])
    source = np.array(source)

    # extract patches
    patches = []
    for i in range(n_patches_h):
        for j in range(n_patches_w):
            patch = source[i*bank_h: (i+1)*bank_h, j*bank_w: (j+1)*bank_w]
            patches.append(patch)


    # process patches
    process_func = partial(give_best_image, images=bank)

    pool = ThreadPool(processes=n_processes)
    best_images = []
    for img in tqdm(pool.imap_unordered(process_func, patches), total=len(patches)):
        best_images.append(img)
        
    pool.close()
    pool.join()

    # assemble output
    canvas = 255 * np.ones_like(source)
    for i in range(n_patches_h):
        for j in range(n_patches_w):
            img_ = best_images[i * n_patches_w + j]
            canvas[i*bank_h:(i+1)*bank_h, j*bank_w:(j+1)*bank_w] = img_

    # save output
    output = Image.fromarray(canvas)
    output.save(output_path)




if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--dataset', type=str, dest='dataset', 
                        help='bank of images to be used', 
                        required=False, default='cifar10')

    parser.add_argument('--source', type=str, dest='source', 
                        help='image to convert', required=True)

    parser.add_argument('--scale', type=float, dest='scale', 
                        help='rescale factor', default=1.0)

    parser.add_argument('--output', type=str, dest='output', 
                        help='output file path', required=True)

    parser.add_argument('--processes', type=int, dest='processes', 
                        help='number of threads to be utilized', 
                        default=None)

    parser.add_argument('--num-images', type=int, dest='num_images', 
                        help='number of images to use', 
                        default=-1)

    options = parser.parse_args()

    if options.dataset == 'cifar10':
        bank = load_cifar()[:options.num_images]
    else:
        raise NotImplementedError('The implementation for other datasets is not provided')

    patchify(source_path=options.source, 
             output_path=options.output, 
             bank=bank, 
             scale=options.scale,
             n_processes=options.processes)


















