import re

def delete_brackets(s):
  pattern = r'（[^（|^）]*）'
  if re.search(pattern, s):
    return re.sub(pattern, '', s)
  else:
    return s

class JackTokenizer:
  def __init__(self, filePath):
    with open(filePath) as f:
      # コメントアウトを取り除いて1行のテキストに変換
      raw = delete_brackets(' '.join([s.split('//')[0].strip() for s in f.readlines()]).replace('/*', '（').replace('*/', '）')).strip()
    self.tokens = []
    self.cnt = 0
    self.token = ''

    # トークナイズ
    now = ''
    flag = True
    for c in raw:
      if flag:
        if c == ' ':
          self.tokens.append(now)
          now = ''
        elif c == '"':
          self.tokens.append(now)
          now = '"'
          flag = False
        elif c in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']:
          self.tokens.append(now)
          self.tokens.append(c)
          now = ''
        else:
          now += c
      else:
        if c == '"':
          now += c
          self.tokens.append(now)
          now = ''
          flag = True
        else:
          now += c
    self.tokens = [c for c in self.tokens if c != '']

    # XxxT.xmlの出力
    txml = '<tokens>\n'
    while(self.hasMoreTokens()):
      self.advance()
      type = self.tokenType()
      if type == 'keyword':
        token = self.keyword()
      elif type == 'symbol':
        token = self.symbol()
      elif type == 'integerConstant':
        token = self.intVal()
      elif type == 'stringConstant':
        token = self.stringVal()
      else:
        token = self.identifier()
      txml += '<{}> {} </{}>\n'.format(type, token, type)
    txml += '</tokens>\n'
    with open(filePath.replace('.jack', 'T_yuriko.xml'), mode='w') as f:
      f.write(txml)

    self.cnt = 0
    self.token = ''

  def hasMoreTokens(self):
    if self.cnt < len(self.tokens):
      return True
    else:
      return False

  def advance(self):
    self.token = self.tokens[self.cnt]
    self.cnt += 1

  def tokenType(self):
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',\
                'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    if self.token in keywords:
      return 'keyword'
    elif self.token in symbols:
      return 'symbol'
    elif re.match(r'^[0-9]+$', self.token) is not None and 0 <= int(self.token) <= 32767:
      return 'integerConstant'
    elif '"' in self.token:
      return 'stringConstant'
    else:
      return 'identifier'

  def keyword(self):
    if self.tokenType() == 'keyword':
      return self.token
    else:
      raise Exception('Error: "{}" is not <keyword>.'.format(self.token))

  def symbol(self):
    if self.tokenType() == 'symbol':
      return self.token.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    else:
      raise Exception('Error: "{{}}" is not <symbol>.'.format(self.token))

  def intVal(self):
    if self.tokenType() == 'integerConstant':
      return int(self.token)
    else:
      raise Exception('Error: "{}" is not <integerConstant>.'.format(self.token))

  def stringVal(self):
    if self.tokenType() == 'stringConstant':
      return self.token.replace('"', '')
    else:
      raise Exception('Error: "{}" is not <stringConstant>.'.format(self.token))

  def identifier(self):
    if self.tokenType() == 'identifier':
      return self.token
    else:
      raise Exception('Error: "{}" is not <identifier>.'.format(self.token))
