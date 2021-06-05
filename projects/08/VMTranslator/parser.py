class Parser:
  def __init__(self, filePath):
    with open(filePath) as f:
      self.lines = [s.split('//')[0].strip() for s in f.readlines() if s.split('//')[0].strip() != '']
    self.cnt = 0
    self.command = ''

  def hasMoreCommands(self):
    if self.cnt < len(self.lines):
      return True
    else:
      return False

  def advance(self):
    self.command = self.lines[self.cnt]
    self.cnt += 1

  def commandType(self):
    self.kind = self.command.split()[0]
    if self.kind == 'push':
      return 'C_PUSH'
    elif self.kind == 'pop':
      return 'C_POP'
    elif self.kind == 'label':
      return 'C_LABEL'
    elif self.kind == 'goto':
      return 'C_GOTO'
    elif self.kind == 'if-goto':
      return 'C_IF'
    elif self.kind == 'function':
      return 'C_FUNCTION'
    elif self.kind == 'return':
      return 'C_RETURN'
    elif self.kind == 'call':
      return 'C_CALL'
    else:
      return 'C_ARITHMETIC'

  def arg1(self):
    if self.commandType() == 'C_ARITHMETIC':
      return self.command.split()[0]
    else:
      return self.command.split()[1]

  def arg2(self):
    return int(self.command.split()[2])
