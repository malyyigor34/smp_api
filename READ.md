SYSTEM:
python 3.8
OS Ubuntu 20

1. Configuration:
	Open smp_api/smp_api/CONFIG.py:
		Insert access key and secret acess key in fields. Set bucket name for storing images and videos.
		Change CHACHE_LIFETIME if it need. 
		Update API keys if need
	Open smp_api/settings.py:
	On line #10 change "DEBUG = True" on "DEBUG = False".

2. Connect to VPS server:
	Execute commands:
		apt install chromium-chromedriver
        python3 python3-pip git screen

	download .zip with source on server via SCP or github and unzip it.
	Execute commands:
		cd smp_api
		python3 -m pip install -r requirements.txt
		screen -dmS api python3 manage.py runserver 0.0.0.0:22 (22 - port. if you have ssl run it on port 433)

You can access via IP adress or server domain name. Admin panel is avaible on url <your_domain>/admin. Login and password from admin panel is qwerty .You can change it in settings. For getting information use url <your_domain>?domain=<URL_FOR_PARSING>&format=json
