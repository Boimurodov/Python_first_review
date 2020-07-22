#! /bin/bash

sudo apt-get install python3.8 python3.8-venv

python3.8 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
