#!/bin/bash
echo "Downloading cifar-100..."
wget -q --show-progress  https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz
tar -xvzf cifar-100-python.tar.gz
echo "Removing unrelated files..."
rm cifar-100-python.tar.gz
mv cifar-100-python/train cifar100
rm -rf cifar-100-python
