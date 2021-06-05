class CodeWriter:
  def __init__(self, filePath):
    self.f = open(filePath, 'w')
    self.vm = ''
    self.labelNum = 0
    self.jump = ''
    self.writeInit()

  def setFileName(self, fileName):
    self.fileName = fileName.split('/')[-1].replace('vm', '')

  def writeCodes(self, arr):
    self.vm += '\n'.join(arr) + '\n'

  def writeInit(self):
    self.writeCodes(['@256', 'D=A', '@SP', 'M=D']) # SP = 256
    self.writeCall('Sys.init', 0) # call Sys.init

  def writeArithmetric(self, command):
    self.writeCodes(['@SP', 'M=M-1', 'A=M', 'D=M'])
    if command == 'neg':
      self.writeCodes(['M=-M'])
    elif command == 'not':
      self.writeCodes(['M=!M'])
    else: # 以下、引数が2つ必要なもの
      self.writeCodes(['@SP', 'M=M-1', 'A=M'])
      if command == 'add':
        self.writeCodes(['M=M+D'])
      elif command == 'sub':
        self.writeCodes(['M=M-D'])
      elif command == 'and':
        self.writeCodes(['M=D&M'])
      elif command == 'or':
        self.writeCodes(['M=D|M'])
      else: # 以下、分岐が必要なもの
        if command == 'eq':
          self.jump = 'JEQ'
        elif command == 'gt':
          self.jump = 'JGT'
        elif command == 'lt':
          self.jump = 'JLT'
        else:
          raise Exception('writeArithmetric error!!')
        self.writeCodes([
          'D=M-D', '@TRUE'+str(self.labelNum), 'D;'+self.jump, '@SP', 'A=M', 'M=0',\
          '@END'+str(self.labelNum), '0;JMP', '(TRUE{})'.format(str(self.labelNum)),\
          '@SP', 'A=M', 'M=-1', '(END{})'.format(str(self.labelNum))\
        ])
        self.labelNum += 1
    self.writeCodes(['@SP', 'M=M+1'])

  # Dの値をスタックの最上位にプッシュしてポインタを1ずらす
  def writePushFromD(self):
    self.writeCodes(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

  def writePush(self, segment, index):
    if segment == 'constant':
      self.writeCodes(['@'+str(index), 'D=A'])
    elif segment == 'local':
      self.writeCodes(['@'+str(index), 'D=A', '@LCL', 'A=M+D', 'D=M'])
    elif segment == 'argument':
      self.writeCodes(['@'+str(index), 'D=A', '@ARG', 'A=M+D', 'D=M'])
    elif segment == 'this':
      self.writeCodes(['@'+str(index), 'D=A', '@THIS', 'A=M+D', 'D=M'])
    elif segment == 'that':
      self.writeCodes(['@'+str(index), 'D=A', '@THAT', 'A=M+D', 'D=M'])
    elif segment == 'pointer':
      self.writeCodes(['@'+str(3+index), 'D=M'])
    elif segment == 'temp':
      self.writeCodes(['@'+str(5+index), 'D=M'])
    elif segment == 'static':
      self.writeCodes(['@'+self.fileName+str(index), 'D=M'])
    else:
      raise Exception('writePush error!!')
    self.writePushFromD()

  def writePop(self, segment, index):
    self.writeCodes(['@SP', 'M=M-1'])
    if segment == 'local':
      self.writeCodes(['@'+str(index), 'D=A', '@LCL', 'D=M+D', '@R13', 'M=D'])
    elif segment == 'argument':
      self.writeCodes(['@'+str(index), 'D=A', '@ARG', 'D=M+D', '@R13', 'M=D'])
    elif segment == 'this':
      self.writeCodes(['@'+str(index), 'D=A', '@THIS', 'D=M+D', '@R13', 'M=D'])
    elif segment == 'that':
      self.writeCodes(['@'+str(index), 'D=A', '@THAT', 'D=M+D', '@R13', 'M=D'])
    elif segment == 'pointer':
      self.writeCodes(['@'+str(3+index), 'D=A', '@R13', 'M=D'])
    elif segment == 'temp':
      self.writeCodes(['@'+str(5+index), 'D=A', '@R13', 'M=D'])
    elif segment == 'static':
      self.writeCodes(['@'+self.fileName+str(index), 'D=A', '@R13', 'M=D'])
    else:
      raise Exception('writePop error!!')
    self.writeCodes(['@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'])

  def writeLabel(self, label):
    self.writeCodes(['('+label+')'])

  def writeGoto(self, label):
    self.writeCodes(['@'+label, '0;JMP'])

  def writeIf(self, label):
    self.writeCodes(['@SP', 'M=M-1', 'A=M', 'D=M', '@'+label, 'D;JNE'])

  def writeFucntion(self, functionName, numLocals):
    self.writeLabel(functionName) # (f)
    for i in range(numLocals): # repeat k times:
      self.writePush('constant', 0) # push 0

  def writeReturn(self):
    self.writeCodes(['@LCL', 'D=M', '@R13', 'M=D']) # FRAME = LCL ※R13にFRAMEを格納
    self.writeCodes(['@5', 'D=A', '@R13', 'A=M-D', 'D=M', '@R14', 'M=D']) # RET = *(FRAME-5) ※R14にRETを格納
    self.writeCodes(['@SP', 'M=M-1', 'A=M', 'D=M', '@ARG', 'A=M', 'M=D']) # *ARG = pop()
    self.writeCodes(['@ARG', 'D=M+1', '@SP', 'M=D']) # SP = ARG+1
    self.writeCodes(['@R13', 'M=M-1', 'A=M', 'D=M', '@THAT', 'M=D']) # THAT = *(FRAME-1) ※FRAME自体を1ずつ減らしていく
    self.writeCodes(['@R13', 'M=M-1', 'A=M', 'D=M', '@THIS', 'M=D']) # THIS = *(FRAME-2)
    self.writeCodes(['@R13', 'M=M-1', 'A=M', 'D=M', '@ARG', 'M=D']) # ARG = *(FRAME-3)
    self.writeCodes(['@R13', 'M=M-1', 'A=M', 'D=M', '@LCL', 'M=D']) # LCL = *(FRAME-4)
    self.writeCodes(['@R14', 'A=M', '0;JMP']) # goto RET

  def writeCall(self, functionName, numArgs):
    self.writeCodes(['@RETURN_ADDRESS'+str(self.labelNum), 'D=A'])
    self.writePushFromD() # push return-address
    self.writeCodes(['@LCL', 'D=M'])
    self.writePushFromD() # push LCL
    self.writeCodes(['@ARG', 'D=M'])
    self.writePushFromD() # push ARG
    self.writeCodes(['@THIS', 'D=M'])
    self.writePushFromD() # push THIS
    self.writeCodes(['@THAT', 'D=M'])
    self.writePushFromD() # push THAT
    self.writeCodes(['@'+str(5+numArgs), 'D=A', '@SP', 'D=M-D', '@ARG', 'M=D']) # ARG = SP-n-5
    self.writeCodes(['@SP', 'D=M', '@LCL', 'M=D']) # LCL = SP
    self.writeGoto(functionName) # goto f
    self.writeLabel('RETURN_ADDRESS'+str(self.labelNum)) # (return-address)
    self.labelNum += 1

  def close(self):
    self.f.write(self.vm)
    self.f.close()
