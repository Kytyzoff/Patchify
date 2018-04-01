<<<<<<< HEAD
<style> 
#wrapper { 
	width: 100%; 
	overflow: hidden; 
	display: flex; 
	align-items: center; 
	justify-content: center; 
} 
#left { 
	width: 50%; 
	border: 2px solid white;
	float:left; 
} 
#right { 
	width: 50%; 
	border: 2px solid white;
	float: right; 
}
 </style>


<img src="src/p_logo.png" align="center">
Convert you image into a patch collage

# Preliminaries
The script uses the following list of dependencies:

* [Numpy](https://github.com/numpy/numpy)
* [Pillow](https://github.com/python-pillow/Pillow)
* [tqdm](https://github.com/noamraph/tqdm)


We use [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset as a bank of patches. It you want to use other images, please some additional code to load the dataset. In order to make it work, load the dataset as `np.ndarray` of shape `[n_images, height, width, 3]`.

In order to prepare **CIFAR-10**, visit the website, download and unzip the dataset. Or you can use our script

```bash
bash load_data.sh
```

# How to use
Just run 

```bash
python patchify.py --source=image.png --output=output.png
```

```bash
optional arguments:
  -h, --help            show this help message and exit
  --dataset             bank of images to be used
  --source              image to convert
  --scale               rescale factor
  --output              output file path
  --processes           number of threads to be utilized
  --num-images          number of images to use
```

# Results
<div id="wrapper" align="center">
	<div id="left" align="center"><img src="src/panda.jpg"></div>
	<div id="right" align="right"><img src="src/p_panda.png"></div>
</div>

<div id="wrapper" align="center">
	<div id="left" align="center"><img src="src/rick.jpg"></div>
	<div id="right" align="right"><img src="src/p_rick.png"></div>
</div>

<div id="wrapper" align="center">
	<div id="left" align="center"><img src="src/tramp.jpg"></div>
	<div id="right" align="right"><img src="src/p_tramp.png"></div>
</div>

Thanks to [Ivan Sosnovik](https://github.com/ISosnovik) for help.











=======
# Patchify
>>>>>>> 4fc1d2844f6ece1973e5b79e22e087856b30ab92
