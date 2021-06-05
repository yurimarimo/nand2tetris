import os
import sys
import glob
from parser import Parser
from codeWriter import CodeWriter

def translate(filePath):
  parser = Parser(filePath)
  codeWriter.setFileName(filePath)
  while(parser.hasMoreCommands()):
    parser.advance()
    command = parser.commandType()
    if command != 'C_RETURN':
      arg1 = parser.arg1()
    if command in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
      arg2 = parser.arg2()
    if command == 'C_ARITHMETIC':
      codeWriter.writeArithmetric(arg1)
    elif command == 'C_PUSH':
      codeWriter.writePush(arg1, arg2)
    elif command == 'C_POP':
      codeWriter.writePop(arg1, arg2)
    elif command == 'C_LABEL':
      codeWriter.writeLabel(arg1)
    elif command == 'C_GOTO':
      codeWriter.writeGoto(arg1)
    elif command == 'C_IF':
      codeWriter.writeIf(arg1)
    elif command == 'C_FUNCTION':
      codeWriter.writeFucntion(arg1, arg2)
    elif command == 'C_RETURN':
      codeWriter.writeReturn()
    elif command == 'C_CALL':
      codeWriter.writeCall(arg1, arg2)

path = sys.argv[1]

if os.path.isfile(path):
  codeWriter = CodeWriter(path.replace('vm', 'asm'))
  translate(path)

elif os.path.isdir(path):
  if path[-1] != '/':
    path = path + '/'
  codeWriter = CodeWriter(path + path.split('/')[-2] + '.asm')
  files = glob.glob(path + '*.vm')
  for file in files:
    translate(file)

else:
  raise Exception('path error!!')

codeWriter.close()
