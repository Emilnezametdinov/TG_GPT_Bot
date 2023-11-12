from flask import Flask
from threading import Thread
import random

app = Flask('')

@app.route('/')
def home():
  return 'Бот живой'

def run():
  app.run(host='0.0.0.0', port=random.randint(2000, 9000))

def keep_alive():
  t = Thread(target=run)
  t.start()


'''
from flask import Flask
from flask import request
from threading import Thread
import time
import requests

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  t = Thread(target=run)
  t.start()
'''
