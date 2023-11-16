run:
	nohup python3 main.py > output1.log 2>&1 &
show:
	ps aux | grep main.py
logs:
	nano output1.log