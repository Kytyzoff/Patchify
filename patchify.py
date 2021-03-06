from __future__ import division, print_function

from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

from PIL import Image
import numpy as np
from tqdm import tqdm



def load_cifar_100():
    path = os.path.join(os.getcwd(), 'cifar100')

    with open(path, 'rb') as fo:
        try:
            dict_ = pickle.load(fo, encoding='bytes')
        except:
            dict_ = pickle.load(fo)
    images = dict_[b'data'].reshape([-1, 3, 32, 32])
    images = images.transpose([0, 2, 3, 1])
    return images 


def give_best_image(patch, images, diversity):
    patch = patch.mean((0, 1))
    images_mean = images.mean((1, 2))
    # TODO: find better function
    diff = np.abs(images_mean - patch) 
    diff = diff.sum(-1)

    args = diff.argsort(-1)
    args = args[:diversity]
    argmin = np.random.choice(args)
    best_image = images[argmin]
    return best_image


def patchify(source_path, output_path, bank, scale=1, n_processes=None, diversity=10):
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
    process_func = partial(give_best_image, images=bank, diversity=diversity)

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

    parser.add_argument('--source', type=str, required=True, 
                        help='Image to convert')

    parser.add_argument('--output', type=str, required=True, 
                        help='Output file path')

    parser.add_argument('--dataset', type=str, default='cifar100',
                        help='Dataset of images to be used. Default '
                             'is "cifar100".')

    parser.add_argument('--scale', type=float, default=1.0, 
                        help='Rescale factor. The size of the image '
                             'will be `scale` times bigger than the '
                             'original one. Default is "1".')

    parser.add_argument('--processes', type=int, default=None,
                        help='Number of threads to be utilized. '
                             'By default the maximum number of '
                             'threads would be utilizaed.')

    parser.add_argument('--num-images', type=int, default=None, 
                        help='Number of images to use. The images '
                             'will be chosen randomly from the '
                             'provided dataset. By default all the '
                             'images are used.')

    parser.add_argument('--diversity', type=int, default=10,
                        help='Number of the most related images from '
                             'which the best will be chose randomly. '
                             'Default is 10. If `diversity` is 1 then '
                             'the most related image will always be '
                             'chosen. The growth of `diversity` '
                             'increases the "expressive power" of the '
                             'resulting collage but degrades the '
                             'approximation.')

    options = parser.parse_args()

    # load images
    if options.dataset == 'cifar100':
        bank = load_cifar_100()
    else:
        raise NotImplementedError('The implementation for other datasets is not provided')

    if options.num_images:
        indices = np.arange(len(bank))
        indices = np.random.choice(indices, options.num_images, replace=False)
        bank = bank[indices]

    patchify(source_path=options.source, 
             output_path=options.output, 
             bank=bank, 
             scale=options.scale,
             n_processes=options.processes, 
             diversity=options.diversity)
