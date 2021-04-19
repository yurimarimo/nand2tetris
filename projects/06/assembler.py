import sys


def dest_to_binary(dest):
  if dest == '':
    return('000')
  if dest == 'M':
    return('001')
  if dest == 'D':
    return('010')
  if dest == 'MD':
    return('011')
  if dest == 'A':
    return('100')
  if dest == 'AM':
    return('101')
  if dest == 'AD':
    return('110')
  if dest == 'AMD':
    return('111')


def comp_to_binary(comp):
  if comp == '0':
    return('0101010')
  if comp == '1':
    return('0111111')
  if comp == '-1':
    return('0111010')
  if comp == 'D':
    return('0001100')
  if comp == 'A':
    return('0110000')
  if comp == 'M':
    return('1110000')
  if comp == '!D':
    return('0001101')
  if comp == '!A':
    return('0110001')
  if comp == '!M':
    return('1110001')
  if comp == '-D':
    return('0001111')
  if comp == '-A':
    return('0110011')
  if comp == '-M':
    return('1110011')
  if comp == 'D+1':
    return('0011111')
  if comp == 'A+1':
    return('0110111')
  if comp == 'M+1':
    return('1110111')
  if comp == 'D-1':
    return('0001110')
  if comp == 'A-1':
    return('0110010')
  if comp == 'M-1':
    return('1110010')
  if comp == 'D+A':
    return('0000010')
  if comp == 'D+M':
    return('1000010')
  if comp == 'D-A':
    return('0010011')
  if comp == 'D-M':
    return('1010011')
  if comp == 'A-D':
    return('0000111')
  if comp == 'M-D':
    return('1000111')
  if comp == 'D&A':
    return('0000000')
  if comp == 'D&M':
    return('1000000')
  if comp == 'D|A':
    return('0010101')
  if comp == 'D|M':
    return('1010101')

def jump_to_binary(jump):
  if jump == '':
    return('000')
  if jump == 'JGT':
    return('001')
  if jump == 'JEQ':
    return('010')
  if jump == 'JGE':
    return('011')
  if jump == 'JLT':
    return('100')
  if jump == 'JNE':
    return('101')
  if jump == 'JLE':
    return('110')
  if jump == 'JMP':
    return('111')


# 定義済みシンボル
symbol = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, \
          'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, \
          'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, \
          'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, \
          'SCREEN': 16384, 'KBD': 24576}
address = 0
hack = ''


# シンボルテーブルの作成
with open(sys.argv[1]) as f:
  for line in f.readlines(): #  1行ずつ見ていく
    s = line.split('//')[0].strip() # コメントアウト部分,前後の空白,改行を除く
    if len(s) > 0:
      print(s)
      if s[0] == '(': # (Xxx)の形があったら
        value = s[1:-1] # シンボル名を取得
        symbol[value] = address # 辞書に追加
      else: # A命令,C命令なら
        address += 1


# バイナリコードへの変換
with open(sys.argv[1]) as f:
  address = 16
  for line in f.readlines(): # 1行ずつ見ていく
    s = line.split('//')[0].strip() # コメントアウト部分,前後の空白,改行を除く

    if len(s) > 0:
      instruction = ''

      # A命令の場合
      if s[0] == '@':
        # @以降の文字列を取得
        value = s[1:]

        # バイナリに変換
        if value.isdecimal(): # 数字だったら
          instruction += '0' + format(int(value), '#017b')[2:]
        else: # 数字でなかったら
          if symbol.get(value) is not None: # シンボルテーブルにシンボルがあれば
            instruction += '0' + format(symbol[value], '#017b')[2:]
          else: # シンボルテーブルにシンボルがなければ
            instruction += '0' + format(address, '#017b')[2:]
            symbol[value] = address
            address += 1

      # C命令の場合
      elif s[0] != '(':
        instruction += '111'

        # 形を dest=comp;jump に統一
        if '=' not in s:
          s = '=' + s
        if ';' not in s:
          s = s + ';'

        # dest,comp,jump をそれぞれ抽出
        dest = s.split('=')[0]
        comp = (s.split('=')[1]).split(';')[0]
        jump = (s.split('=')[1]).split(';')[1]

        # バイナリに変換
        instruction += comp_to_binary(comp) + dest_to_binary(dest) + jump_to_binary(jump)

      # シンボル定義の場合
      else:
        continue

      hack += instruction + '\n'

# 機械語ファイル(.hack)の出力
with open(sys.argv[1].replace('asm', 'hack'), 'w') as f:
  f.write(hack)
