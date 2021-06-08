from jackTokenizer import JackTokenizer

class CompilationEngine:
  def __init__(self, inputFilePath, outputFilePath):
    self.jackTokenizer = JackTokenizer(inputFilePath)
    self.jackTokenizer.advance()
    self.xml = ''
    self.indent = 0
    self.compileClass()
    self.f = open(outputFilePath, 'w')
    self.f.write(self.xml)
    print('finish!!')

  def writeTerminal(self, token, candidates=[]):
    type = self.jackTokenizer.tokenType()
    if type in ['keyword', 'symbol']:
      if len(candidates) == 0:
        raise Exception('Error: Candidates must be set.')
      elif self.jackTokenizer.token not in candidates:
        raise Exception('Error: "{}" is an unsuitable {}.'.format(str(token), type))
    self.xml += ' ' * self.indent + '<{}> {} </{}>\n'.format(type, str(token), type)
    if self.jackTokenizer.hasMoreTokens():
      self.jackTokenizer.advance()

  def writeNonTerminalStart(self, kind):
    self.xml += ' ' * self.indent + '<{}>\n'.format(kind)
    self.indent += 2

  def writeNonTerminalEnd(self, kind):
    self.indent -= 2
    self.xml += ' ' * self.indent + '</{}>\n'.format(kind)

  def compileClass(self):
    self.writeNonTerminalStart('class')
    self.writeTerminal(self.jackTokenizer.keyword(), ['class'])
    self.writeTerminal(self.jackTokenizer.identifier())
    self.writeTerminal(self.jackTokenizer.symbol(), ['{'])
    while self.jackTokenizer.token in ['static', 'field']:
      self.compileClassVarDec()
    while self.jackTokenizer.token in ['constructor', 'function', 'method']:
      self.compileSubroutineDec()
    self.writeTerminal(self.jackTokenizer.symbol(), ['}'])
    self.writeNonTerminalEnd('class')

  def compileClassVarDec(self):
    self.writeNonTerminalStart('classVarDec')
    self.writeTerminal(self.jackTokenizer.keyword(), ['static', 'field'])
    self.compileType()
    self.writeTerminal(self.jackTokenizer.identifier())
    while self.jackTokenizer.token == ',':
      self.writeTerminal(self.jackTokenizer.symbol(), [','])
      self.writeTerminal(self.jackTokenizer.identifier())
    self.writeTerminal(self.jackTokenizer.symbol(), [';'])
    self.writeNonTerminalEnd('classVarDec')

  def compileType(self):
    if self.jackTokenizer.token in ['int', 'char', 'boolean']:
      self.writeTerminal(self.jackTokenizer.keyword(), ['int', 'char', 'boolean'])
    else:
      self.writeTerminal(self.jackTokenizer.identifier())

  def compileSubroutineDec(self):
    self.writeNonTerminalStart('subroutineDec')
    self.writeTerminal(self.jackTokenizer.keyword(), ['constructor', 'function', 'method'])
    if self.jackTokenizer.token == 'void':
      self.writeTerminal(self.jackTokenizer.keyword(), ['void'])
    else:
      self.compileType()
    self.writeTerminal(self.jackTokenizer.identifier())
    self.writeTerminal(self.jackTokenizer.symbol(), ['('])
    self.compileParameterList()
    self.writeTerminal(self.jackTokenizer.symbol(), [')'])
    self.compileSubroutineBody()
    self.writeNonTerminalEnd('subroutineDec')

  def compileParameterList(self):
    self.writeNonTerminalStart('parameterList')
    while self.jackTokenizer.token != ')':
      if self.jackTokenizer.token == ',':
        self.writeTerminal(self.jackTokenizer.symbol(), [','])
      self.compileType()
      self.writeTerminal(self.jackTokenizer.identifier())
    self.writeNonTerminalEnd('parameterList')

  def compileSubroutineBody(self):
    self.writeNonTerminalStart('subroutineBody')
    self.writeTerminal(self.jackTokenizer.symbol(), ['{'])
    while self.jackTokenizer.token == 'var':
      self.compileVarDec()
    self.compileStatements()
    self.writeTerminal(self.jackTokenizer.symbol(), ['}'])
    self.writeNonTerminalEnd('subroutineBody')

  def compileVarDec(self):
    self.writeNonTerminalStart('varDec')
    self.writeTerminal(self.jackTokenizer.keyword(), ['var'])
    self.compileType()
    self.writeTerminal(self.jackTokenizer.identifier())
    while self.jackTokenizer.token == ',':
      self.writeTerminal(self.jackTokenizer.symbol(), [','])
      self.writeTerminal(self.jackTokenizer.identifier())
    self.writeTerminal(self.jackTokenizer.symbol(), [';'])
    self.writeNonTerminalEnd('varDec')

  def compileStatements(self):
    self.writeNonTerminalStart('statements')
    while self.jackTokenizer.token in ['let', 'if', 'while', 'do', 'return']:
      if self.jackTokenizer.token == 'let':
        self.compileLet()
      elif self.jackTokenizer.token == 'if':
        self.compileIf()
      elif self.jackTokenizer.token == 'while':
        self.compileWhile()
      elif self.jackTokenizer.token == 'do':
        self.compileDo()
      else:
        self.compileReturn()
    self.writeNonTerminalEnd('statements')

  def compileLet(self):
    self.writeNonTerminalStart('letStatement')
    self.writeTerminal(self.jackTokenizer.keyword(), ['let'])
    self.writeTerminal(self.jackTokenizer.identifier())
    if self.jackTokenizer.token == '[':
      self.writeTerminal(self.jackTokenizer.symbol(), ['['])
      self.compileExpression()
      self.writeTerminal(self.jackTokenizer.symbol(), [']'])
    self.writeTerminal(self.jackTokenizer.symbol(), ['='])
    self.compileExpression()
    self.writeTerminal(self.jackTokenizer.symbol(), [';'])
    self.writeNonTerminalEnd('letStatement')

  def compileIf(self):
    self.writeNonTerminalStart('ifStatement')
    self.writeTerminal(self.jackTokenizer.keyword(), ['if'])
    self.writeTerminal(self.jackTokenizer.symbol(), ['('])
    self.compileExpression()
    self.writeTerminal(self.jackTokenizer.symbol(), [')'])
    self.writeTerminal(self.jackTokenizer.symbol(), ['{'])
    self.compileStatements()
    self.writeTerminal(self.jackTokenizer.symbol(), ['}'])
    if self.jackTokenizer.token == 'else':
      self.writeTerminal(self.jackTokenizer.keyword(), ['else'])
      self.writeTerminal(self.jackTokenizer.symbol(), ['{'])
      self.compileStatements()
      self.writeTerminal(self.jackTokenizer.symbol(), ['}'])
    self.writeNonTerminalEnd('ifStatement')

  def compileWhile(self):
    self.writeNonTerminalStart('whileStatement')
    self.writeTerminal(self.jackTokenizer.keyword(), ['while'])
    self.writeTerminal(self.jackTokenizer.symbol(), ['('])
    self.compileExpression()
    self.writeTerminal(self.jackTokenizer.symbol(), [')'])
    self.writeTerminal(self.jackTokenizer.symbol(), ['{'])
    self.compileStatements()
    self.writeTerminal(self.jackTokenizer.symbol(), ['}'])
    self.writeNonTerminalEnd('whileStatement')

  def compileDo(self):
    self.writeNonTerminalStart('doStatement')
    self.writeTerminal(self.jackTokenizer.keyword(), ['do'])
    self.writeTerminal(self.jackTokenizer.identifier())
    self.compileSubroutineCall()
    self.writeTerminal(self.jackTokenizer.symbol(), [';'])
    self.writeNonTerminalEnd('doStatement')

  def compileReturn(self):
    self.writeNonTerminalStart('returnStatement')
    self.writeTerminal(self.jackTokenizer.keyword(), ['return'])
    if self.jackTokenizer.token != ';':
      self.compileExpression()
    self.writeTerminal(self.jackTokenizer.symbol(), [';'])
    self.writeNonTerminalEnd('returnStatement')

  def compileExpression(self):
    self.writeNonTerminalStart('expression')
    self.compileTerm()
    while self.jackTokenizer.token in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
      self.writeTerminal(self.jackTokenizer.symbol(), ['+', '-', '*', '/', '&', '|', '<', '>', '='])
      self.compileTerm()
    self.writeNonTerminalEnd('expression')

  def compileTerm(self):
    self.writeNonTerminalStart('term')
    if self.jackTokenizer.tokenType() == 'integerConstant':
      self.writeTerminal(self.jackTokenizer.intVal())
    elif self.jackTokenizer.tokenType() == 'stringConstant':
      self.writeTerminal(self.jackTokenizer.stringVal())
    elif self.jackTokenizer.tokenType() == 'keyword':
      self.writeTerminal(self.jackTokenizer.keyword(), ['true', 'false', 'null', 'this'])
    elif self.jackTokenizer.token == '(':
      self.writeTerminal(self.jackTokenizer.symbol(), ['('])
      self.compileExpression()
      self.writeTerminal(self.jackTokenizer.symbol(), [')'])
    elif self.jackTokenizer.token in ['-', '~']:
      self.writeTerminal(self.jackTokenizer.symbol(), ['-', '~'])
      self.compileTerm()
    else:
      self.writeTerminal(self.jackTokenizer.identifier())
      if self.jackTokenizer.token == '[':
        self.writeTerminal(self.jackTokenizer.symbol(), ['['])
        self.compileExpression()
        self.writeTerminal(self.jackTokenizer.symbol(), [']'])
      elif self.jackTokenizer.token in ['(', '.']:
        self.compileSubroutineCall()
    self.writeNonTerminalEnd('term')

  def compileSubroutineCall(self): # 最初のidentifier以外
    if self.jackTokenizer.token == '.':
      self.writeTerminal(self.jackTokenizer.symbol(), ['.'])
      self.writeTerminal(self.jackTokenizer.identifier())
    self.writeTerminal(self.jackTokenizer.symbol(), ['('])
    self.compileExpressionList()
    self.writeTerminal(self.jackTokenizer.symbol(), [')'])

  def compileExpressionList(self):
    self.writeNonTerminalStart('expressionList')
    while self.jackTokenizer.token != ')':
      if self.jackTokenizer.token == ',':
        self.writeTerminal(self.jackTokenizer.symbol(), [','])
      self.compileExpression()
    self.writeNonTerminalEnd('expressionList')
