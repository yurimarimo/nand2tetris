class CodeWriter:
  def __init__(self, fileName):
    self.f = open(fileName, 'w')
    self.fileName = fileName.split('/')[-1].replace('asm', '')
    self.vm = ''
    self.label = 0
    self.jump = ''

  def writeArithmetric(self, command):
    self.vm += '\n'.join(['@SP', 'M=M-1', 'A=M', 'D=M']) + '\n'
    # yのみ使用するもの
    if command == 'neg':
      self.vm += 'M=-M'
    elif command == 'not':
      self.vm += 'M=!M'
    # x,y両方使用するもの
    else:
      self.vm += '\n'.join(['@SP', 'M=M-1', 'A=M']) + '\n'
      if command == 'add':
        self.vm += 'M=M+D'
      elif command == 'sub':
        self.vm += 'M=M-D'
      elif command == 'and':
        self.vm += 'M=D&M'
      elif command == 'or':
        self.vm += 'M=D|M'
      # 比較演算をするもの
      else:
        if command == 'eq':
          self.jump = 'JEQ'
        elif command == 'gt':
          self.jump = 'JGT'
        elif command == 'lt':
          self.jump = 'JLT'
        self.vm += '\n'.join(['D=M-D', '@TRUE'+str(self.label), 'D;'+self.jump, '@SP', 'A=M', 'M=0', '@END'+str(self.label), '0;JMP',\
                              '(TRUE{})'.format(str(self.label)), '@SP', 'A=M', 'M=-1', '(END{})'.format(str(self.label))])
        self.label += 1
    self.vm += '\n' + '\n'.join(['@SP', 'M=M+1']) + '\n'

  def writePushPop(self, command, segment, index):
    if command == 'C_PUSH':
      if segment == 'constant':
        self.vm += '\n'.join(['@'+str(index), 'D=A'])
      elif segment == 'local':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@LCL', 'A=M+D', 'D=M'])
      elif segment == 'argument':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@ARG', 'A=M+D', 'D=M'])
      elif segment == 'this':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@THIS', 'A=M+D', 'D=M'])
      elif segment == 'that':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@THAT', 'A=M+D', 'D=M'])
      elif segment == 'pointer':
        self.vm += '\n'.join(['@'+str(3+index), 'D=M'])
      elif segment == 'temp':
        self.vm += '\n'.join(['@'+str(5+index), 'D=M'])
      elif segment == 'static':
        self.vm += '\n'.join(['@'+self.fileName+str(index), 'D=M'])
      self.vm += '\n' + '\n'.join(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']) + '\n'
    else: # command == 'C_POP'
      self.vm += '\n'.join(['@SP', 'M=M-1'])  + '\n'
      if segment == 'local':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@LCL', 'D=M+D', '@R13', 'M=D'])
      elif segment == 'argument':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@ARG', 'D=M+D', '@R13', 'M=D'])
      elif segment == 'this':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@THIS', 'D=M+D', '@R13', 'M=D'])
      elif segment == 'that':
        self.vm += '\n'.join(['@'+str(index), 'D=A', '@THAT', 'D=M+D', '@R13', 'M=D'])
      elif segment == 'pointer':
        self.vm += '\n'.join(['@'+str(3+index), 'D=A', '@R13', 'M=D'])
      elif segment == 'temp':
        self.vm += '\n'.join(['@'+str(5+index), 'D=A', '@R13', 'M=D'])
      elif segment == 'static':
        self.vm += '\n'.join(['@'+self.fileName+str(index), 'D=A', '@R13', 'M=D'])
      self.vm += '\n' + '\n'.join(['@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D']) + '\n'

  def close(self):
    self.f.write(self.vm)
    self.f.close()
