// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// 初期化
  @color
  M=0   // color=0
  @8192
  D=A
  @pixels
  M=D   // pixels=8192

// 無限ループ
(LOOP)
  @i
  M=1  // i=1
  @KBD
  D=M   // D=0or1(キーボード入力)
  @BLACK
  D;JNE // もしD!=0なら、キーボードが押されているのでBLACKへ移動
  @WHITE
  D;JEQ // もしD=0なら、キーボードが押されていないのでWHITEへ移動

// 画面を一色に描画する
(PAINT)
  @i
  D=M   // D=i
  @pixels
  D=D-M // D=i-pixels
  @LOOP
  D;JGT // もし(i-pixels)>0ならLOOPへ移動
  @SCREEN
  D=A-1 // D=16383(i=1スタートなので)
  @i
  D=D+M // D=16383+i
  @position
  M=D   // position=16383+i
  @color
  D=M   // D=color
  @position
  A=M   // @position
  M=D   // 白or黒にペイント
  @i
  M=M+1 // i=i+1
  @PAINT
  0;JMP // PAINTへ移動

// color=1にする
(BLACK)
  @color
  M=-1   // color=111111111111111
  @PAINT
  0;JMP // PAINTへ移動

// color＝0にする
(WHITE)
  @color
  M=0   // color=0000000000000000
  @PAINT
  0;JMP // PAINTへ移動
