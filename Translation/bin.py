import json
import sys
import re
import requests
from termcolor import colored

MAP = {
  '名词': 'n.',
  '动词': 'vt.',
  '形容词': 'adj.',
  '副词': 'adv.',
  '介词': 'prep.'
}


def isChinese(text):
  if u'\u4e00' <= text <= u'\u9fff':
    return True
  return False


def translate(text):
  params = {
    'client': 'gtx',
    'sl': 'en',
    'tl': 'zh-CN',
    'q': text,
    'ie': 'UTF-8'
    # 'format': 'text',
    # 'model': 'base',
    # 'target': 'zh-CN',
    # 'key': ''
  }
  if isChinese(text) == True:
    params['sl'] = 'zh-CN'
    params['tl'] = 'en'
  # t - 源text的翻译
  # at - 会额外返回一些近义词
  # ex - examples
  # ss - 如果翻译的是单个词，会返回与该词相关的动词、形容词、名词
  # md - 如果翻译的是单个词，返回该词的定义
  # rw - 组词
  # bd - 词义
  # rm - 发音
  req = requests.get('http://translate.google.cn/translate_a/single?dt=t&dt=rm&dt=bd&dt=rw&dt=ex', params=params)
  # req = requests.post('https://translation.googleapis.com/language/translate/v2', params=params)
  content = json.loads(req.content)
  leng = len(content)
  # print(content)

  target = ''
  source = ''
  phonetic = ''
  word = []
  phrase = []
  example = []

  try:
    if 1 < leng and content[1]:
      for w in content[1]:
        ww = {
          'type': '...',
          'text': '；'.join(w[1])
        }
        if w[0] in MAP:
          ww['type'] = MAP[w[0]]
        word.append(ww)

    if 14 < leng and content[14] and content[14][0]:
      phrase = [ph for ph in content[14][0]]

    if 13 < leng and content[13] and content[13][0]:
      example = [ex[0] for ex in content[13][0]]

    target = content[0][0][0]
    source = content[0][0][1]
    phonetic = content[0][1][3]

  except IndexError as e:
    print(e)
    pass

  result = {
    'target': target,
    'source': source,
    'phonetic': phonetic,
    'word': word,
    'phrase': phrase,
    'example': example
  }

  return result


def execute(argv=sys.argv):
  '''
  启动函数
  :param argv: 参数列表(默认为sys.argv参数)
  :return: None
  '''

  content = translate(' '.join(argv[1:]))
  print(
  colored(content['source'], 'red') + colored(' [' + content['phonetic'] + '] ' + content['target'], 'green') + '\n')
  for w in content['word']:
    print(colored(w['type'], 'cyan') + ' ' + colored(w['text'], 'red'))

  print('\n' + colored('词组：', 'cyan') + colored('[' + '] ['.join(content['phrase']) + ']', 'yellow') + '\n')

  leng = len(content['example'])
  if leng > 5:
    leng = 5
  for i in range(leng):
    ex = content['example'][i]
    w = re.sub(r'^(.*)<b>(.+)</b>(.*)$', lambda a: a[1] + colored(a[2], 'red') + a[3], ex)
    print(colored('ex：', 'cyan') + ' ' + w)

  sys.exit(0)
