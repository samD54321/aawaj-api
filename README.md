# aawaj-api
You will need a CUDA capable device with proper drivers for CUDA and CUDNN installed to run this API with Tensorflow.v1 and PyTorch 1. Follow the following steps to get the API up and running.


1. Clone this repository from GitHub. 

2. Create a conda environment with python 3.7 as: <br/>
	```conda create -n myenv python=3.7```

3. Install Pytorch 1 within 'myenv'. <br/>
	PyTorch official site : https://pytorch.org/get-started/locally/ (remember to install according to your CUDA compute environment version) 

4. Install pip dependencies from requirements.txt as: <br/> 
	```pip install -r requirements.txt```

5. Within aawaj-api, run the following git commands: <br/>
	```git clone -q --recursive https://github.com/NVIDIA/tacotron2.git``` <br/>
	```cd tacotron2/waveglow``` <br/>
	```git checkout 2fd4e63``` <br/>

6. Download the Aawaj model and WaveGlow model from the links given below:
	```https://drive.google.com/file/d/1OyUBTPRYqit7Lv1AapMPSPEOiFwukxoN/view?usp=sharing```
	```https://drive.google.com/file/d/1bVC8XbtPbTyrSgbqddJo6G8zgyZFMmXw/view?usp=sharing```
	
7. Change your model paths within fileapi.py 
	``` tacotron2_pretrained_model= PATH_TO_AAWAJ```
	``` waveglow_pretrained_model=PATH_TO_WAVEGLOW```

8. Run fileapi.py to create an API within your local host visible within your LAN by: <br/>
	```python fileapi.py```

9. Run a query to access TTS functionalities as: <br/>
	```localhost:5000/api?query=YOUR_QUERY_HERE```
