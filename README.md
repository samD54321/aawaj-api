# aawaj-api

1. Create a conda environment with python 3.7 as: <br/>
	conda create -n myenv python=3.7

2. Install Pytorch 1 within 'myenv'.

3. Install pip dependenvies from requirements.txt as: <br/> 
	pip install -r requirements.txt
	
4. Run fileapi.py to create an API within your local host visible within your LAN by: <br/>
	python fileapi.py

5. Run a query to access TTS functionalities as: <br/>
	localhost:5000/api?query=YOUR_QUERY_HERE
