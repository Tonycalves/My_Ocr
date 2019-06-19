import gzip
import os
import struct
from array import array
import random

class Algo(object):
    def __init__(self, path='.', return_type='lists', gz=False):
        self.path = path
        self._return_type = return_type
        self.test_img_fname = 't10k-images-idx3-ubyte'
        self.test_lbl_fname = 't10k-labels-idx1-ubyte'
        self.gz = gz
        self.test_images = []
        self.test_labels = []

    @property
    def return_type(self):
        return self._return_type


    def load_picture_labels(self):
        ims, labels = self.load(os.path.join(self.path, self.test_img_fname),
                                os.path.join(self.path, self.test_lbl_fname))

        self.test_images = ims
        self.test_labels = labels

        return self.test_images, self.test_labels

    #Open the .gz with picture/labels
    def opener(self, path_fn, *args, **kwargs):
        if self.gz:
            return gzip.open(path_fn + '.gz', *args, **kwargs)
        else:
            return open(path_fn, *args, **kwargs)

    def load(self, path_img, path_label, batch=None):
        if batch is not None:
            if type(batch) is not list or len(batch) is not 2:
                raise ValueError('batch should be a 1-D list'
                                 '(start_point, batch_size)')

        with self.opener(path_label, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049,'
                                 'got {}'.format(magic))

            labels = array("B", file.read())

        with self.opener(path_img, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051,'
                                 'got {}'.format(magic))

            image_data = array("B", file.read())

        if batch is not None:
            image_data = image_data[batch[0] * rows * cols:\
                                    (batch[0] + batch[1]) * rows * cols]
            labels = labels[batch[0]: batch[0] + batch[1]]
            size = batch[1]

        images = []
        for i in range(size):
            images.append([0] * rows * cols)

        for i in range(size):
            images[i][:] = image_data[i * rows * cols:(i + 1) * rows * cols]

        return images, labels

    # Class Display for displaying the number with "@" and ".".
    # The number is representing with all the "@"
    @classmethod
    def displaying_picture_to_shell(cls, img, width=28, threshold=200):
        render = ''
        for i in range(len(img)):
            if i % width == 0:
                render += '\n'
            if img[i] > threshold:
                render += '\033[35m\033[0m'
            else:
                render += '\033[30m*\033[0m'
        return render


    @classmethod
    def itisdone(self):
        number = random.randrange(0,10)
        if number == 1:
            return True
        if number == 7:
            return True
        else:
            return False