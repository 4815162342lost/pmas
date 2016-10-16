#!/usr/bin/python3
import os
import glob
import gzip
import datetime
import subprocess
import time
import psutil

os.chdir(os.path.dirname(os.path.realpath(__file__)))
txt_file_list = sorted(glob.glob("*.txt"), key=os.path.getmtime, reverse=True)
gzip_file_list = sorted(glob.glob("*.gz"), key=os.path.getmtime, reverse=True)

if len(txt_file_list) > 1:
	print("old log files found")
	for current_txt_file in txt_file_list[1:]:
		cur_txt_file = open(current_txt_file, "rb")
		with gzip.open(current_txt_file + ".gz", "wb", compresslevel=9) as gzip_file:
			gzip_file.writelines(cur_txt_file)
		cur_txt_file.close()
		os.remove(current_txt_file)

if len(gzip_file_list) > 9:
	print("old archive files found")
	for current_gzip_file in gzip_file_list[9:]:
		os.remove(current_gzip_file)

with open(str(datetime.datetime.now().date()) + ".txt", "a+") as log_output:
	subprocess.call(["/home/vodka/scripts/python/steam_gifts/sg.py"], stdout=log_output, stderr=log_output)
	while True:
		process_alive=False
		pr=psutil.process_iter()
		for i in pr:
			if i.name()=="sg.py":
				print("process alive")
				process_alive=True
				break
		if not process_alive:
			subprocess.call(["/home/vodka/scripts/python/steam_gifts/sg.py"], stdout=log_output)
			print("dead")
			subprocess.call(["beep", "-l 2000", "-f 1900", "-r 3"])
		time.sleep(10)
