import sys
from parser import Parser
from codeWriter import CodeWriter

parser = Parser(sys.argv[1])
codeWriter = CodeWriter(sys.argv[1].replace('vm', 'asm'))

while(parser.hasMoreCommands()):
  parser.advance()
  command = parser.commandType()
  if command != 'C_RETURN':
    arg1 = parser.arg1()
  if command in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
    arg2 = parser.arg2()
  if command == 'C_ARITHMETIC':
    codeWriter.writeArithmetric(arg1)
  if command in ['C_PUSH', 'C_POP']:
    codeWriter.writePushPop(command, arg1, arg2)

codeWriter.close()
