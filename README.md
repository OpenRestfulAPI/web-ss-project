# Web Screenshot Project

### Aim
not needing the use of an api key but to self host an instance and use it as it is on the go


### One-Click Heroku Deploy:
click the button below to host the application on the go

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/OpenRestfulAPI/web-ss-project.git)

### Initializing and Explanation Step-by-Step

- open up a virtual environment:
```
python -m venv venv

On Windows: venv\Scripts\activate.bat
On Linux/MacOS: source venv/bin/activate

```

- install requiremnts:
```
pip install -r requirements.txt
```

- Configs are saved in `config.ini` file. you can change it if you want.

- run the webserver: `python -m webss`

- to view a screenshot of a page visit: `host:port/?site=website` in this format


## Special Credits
- [Tiangolo](https://github.com/tiangolo) - for providing us with FastAPI
- [Miyakogi](https://github.com/miyakogi) - Providing useful headless chromium based browser for python