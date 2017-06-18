ImgSlack
========

This application provides an endpoint for slack to push messages to for the file.shared event, download the image to a location, then notify the channel that the image is available for downloading free of Slack's rediculous front-end.

Dependencies
------------
This sofware is developed against python 3.5 (3.5.3, specifically), and has two components: a flask web frontend (for queue status and accepting the slack events), and a worker, for processing the queue.

- python 3.5
- beanstalk queue (https://kr.github.io/beanstalkd/)

### Libraries
* certifi
* chardet
* click
* daemonize
* Flask
* Greenstalk
* idna
* itsdangerous
* Jinja2
* MarkupSafe
* pyaml
* PyYAML
* requests
* urllib3
* Werkzeug

Installation
------------

`TODO`

Usage
-----

`TODO`

Notes
-----

`TODO`
