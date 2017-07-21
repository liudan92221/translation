import os, json, sys, re, random, time
import requests, inquirer
from jinja2 import Template
from termcolor import colored

root = os.path.dirname(os.path.realpath(__file__))

JSON_FILE = root + '/json.json'
ARR_FILE = root + '/arr.json'

MAP = {
  '名词': 'n.',
  '动词': 'vt.',
  '形容词': 'adj.',
  '副词': 'adv.',
  '介词': 'prep.',
  '代词': 'pron.'
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
          'type': w[0],
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

def cmdText(content):
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


def saveWord(content):
  leng = len(content['word'])
  if isChinese(content['source']) == True or leng == 0:
    return

  word = content['source']
  saveFile([word])

def saveFile(words):
  with open(JSON_FILE, 'r') as f:
    j = json.load(f)

  with open(ARR_FILE, 'r') as f:
    a = json.load(f)

  for word in words:
    if word in j:
      break
    else:
      j[word] = True
      a.append(word)

  with open(JSON_FILE, 'w') as f:
    json.dump(j, f)

  with open(ARR_FILE, 'w') as f:
    json.dump(a, f)

def getWord(num=50):
  with open(ARR_FILE, 'r') as f:
    a = json.load(f)

  if len(a) < num:
    num = len(a)

  words = []
  tmpJson = {}

  def getRandomWord():
    index = random.randint(0, num - 1)
    word = a[index]
    if word in tmpJson:
      return getRandomWord()
    words.append(word)
    tmpJson[word] = True
    return word

  for index in range(num):
    getRandomWord()

  return words


def getWordData(arr):
  contents = [translate(word) for word in arr]
  return contents


def makeWordList(argv=sys.argv):
  num = 50
  if len(argv) >= 2:
    num = int(argv[1])

  str = ''
  with open(root + '/_index.html', 'r') as f:
    str = f.read()

  firstTime = time.time()
  data = getWordData(getWord(num))
  temp = Template(str)
  htmlStr = temp.render({"data": data})

  fileName = 'words_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.html'
  with open(os.getcwd() + '/' + fileName, 'w') as f:
    f.write(htmlStr)

  lastTime = time.time()
  print(lastTime - firstTime)
  print('make html: ' + fileName)
  sys.exit(0)

def copyWords(argv=sys.argv):
  fileName = 'copy.json'
  if len(argv) >= 2:
    fileName = argv[1]

  with open(ARR_FILE, 'r') as f:
    a = json.load(f)

  with open(os.getcwd() + '/' + fileName, 'w') as f:
    json.dump(a, f)

  print('make json: ' + fileName)
  sys.exit(0)

def joinWords(argv=sys.argv):
  fileName = 'join.json'
  if len(argv) >= 2:
    fileName = argv[1]

  with open(os.getcwd() + '/' + fileName, 'r') as f:
    a = json.load(f)

  if isinstance(a, list) == False:
    print(fileName+' is error')
    return

  saveFile(a)
  print('copy json: ' + fileName)
  sys.exit(0)

def removeWord():
  message = ''
  questions = [
    inquirer.Text('ask', message=message)
  ]
  answers = inquirer.prompt(questions)
  try:
    word = answers['ask']
  except Exception:
    sys.exit(1)

  print(word)
  sys.exit(0)

def execute(argv=sys.argv):
  '''
  启动函数
  :param argv: 参数列表(默认为sys.argv参数)
  :return: None
  '''
  content = translate(' '.join(argv[1:]))
  cmdText(content)
  saveWord(content)
  sys.exit(0)
