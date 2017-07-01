import json
import sys, os, optparse
import requests
from termcolor import colored

def func(text):
  params = {
    'client': 'gtx',
    'sl': 'en',
    'tl': 'zh-CN',
    'q': text
  }
  req = requests.get('http://translate.google.cn/translate_a/single?dt=t&dt=at&dt=ss&dt=md', params=params)
  return json.loads(req.content)


def execute(argv=sys.argv):
  '''
  启动函数
  :param argv: 参数列表(默认为sys.argv参数)
  :return: None
  '''
  content = func(argv[1])

  print(colored(content[0][0][0], 'red'))

  sys.exit(0)
