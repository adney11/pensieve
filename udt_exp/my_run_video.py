import os
import sys
import signal
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
from time import sleep

import logging
logging.basicConfig(filename='logs/my_run_video.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)



# TO RUN: download https://pypi.python.org/packages/source/s/selenium/selenium-2.39.0.tar.gz
# run sudo apt-get install python-setuptools
# run sudo apt-get install xvfb
# after untar, run sudo python setup.py install
# follow directions here: https://pypi.python.org/pypi/PyVirtualDisplay to install pyvirtualdisplay

# For chrome, need chrome driver: https://code.google.com/p/selenium/wiki/ChromeDriver
# chromedriver variable should be path to the chromedriver
# the default location for firefox is /usr/bin/firefox and chrome binary is /usr/bin/google-chrome
# if they are at those locations, don't need to specify


def dp(msg):
	#dbg = os.getenv('DEBUG_MODE')
	#if dbg:
	#	print("DEBUG: " + msg)
	LOG.debug(msg)


def timeout_handler(signum, frame):
	LOG.error("run_video script timed out")
	raise Exception("Timeout")

ip = '10.10.1.1'
abr_algo = 'RL'
run_time = 320
process_id = '69'
trace_file = 'udt_trace'
	

	
# generate url
url = 'http://' + ip + '/' + 'myindex_' + abr_algo + '.html'

# timeout signal
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(run_time + 30)
	
try:
	# copy over the chrome user dir
	dp("copy over the chrome user dir...")
	default_chrome_user_dir = '../abr_browser_dir/chrome_data_dir'
	chrome_user_dir = '/tmp/chrome_user_dir_id_' + process_id
	os.system('rm -r ' + chrome_user_dir)
	os.system('cp -r ' + default_chrome_user_dir + ' ' + chrome_user_dir)
	os.system('sudo chown -R acardoza ' + chrome_user_dir)
	
	# start abr algorithm server
	dp("start abr algorithm server...")
	if abr_algo == 'RL':
		command = 'exec /usr/bin/python3.6 ../rl_server/rl_server_no_training.py ' + trace_file
	elif abr_algo == 'fastMPC':
		command = 'exec /usr/bin/python3.6 ../rl_server/mpc_server.py ' + trace_file
	elif abr_algo == 'robustMPC':
		command = 'exec /usr/bin/python3.6 ../rl_server/robust_mpc_server.py ' + trace_file
	else:
		command = 'exec /usr/bin/python3.6 ../rl_server/simple_server.py ' + abr_algo + ' ' + trace_file
	
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	sleep(2)
	
	# to not display the page in browser
	dp("starting display...")
	display = Display(visible=0, size=(800,600))
	display.start()
	dp("display started...")

	# initialize chrome driver
	dp("initialize chrome driver")
	#options=Options()
	options=webdriver.ChromeOptions()
	chrome_driver = '../abr_browser_dir/chromedriver'
	options.add_argument('--user-data-dir=' + chrome_user_dir)
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--disable-web-security')
	options.add_argument('--autoplay-policy=no-user-gesture-required')
	driver=webdriver.Chrome(chrome_driver, chrome_options=options)
	#chromeservice=Service(executable_path=chrome_driver)
	#driver=webdriver.Chrome(service=chromeservice, options=options)
	dp("chrome driver initialized...")

	# run chrome
	driver.set_page_load_timeout(10)
	dp("page parameters set")
	driver.get(url)
	dp("got url")
	dp(f"sleeping for {run_time} seconds")
	sleep(run_time)
	#input("press enter to end")
	
	driver.quit()
	display.stop()
	
	dp("stopped chrome driver")

	# kill abr algorithm server
	proc.send_signal(signal.SIGINT)
	# proc.kill()
	
	print('done')
	
except Exception as e:
	try: 
		display.stop()
	except:
		pass
	try:
		driver.quit()
	except:
		pass
	try:
		proc.send_signal(signal.SIGINT)
	except:
		pass
	
	print(e)

