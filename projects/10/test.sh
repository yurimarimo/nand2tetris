python3 JackAnalyzer/main.py ./ArrayTest/
python3 JackAnalyzer/main.py ./ExpressionLessSquare/
python3 JackAnalyzer/main.py ./Square/
sh ~/nand2tetris/tools/TextComparer.sh ./ArrayTest/Main.xml ./ArrayTest/Main_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./ExpressionLessSquare/Main.xml ./ExpressionLessSquare/Main_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./ExpressionLessSquare/Square.xml ./ExpressionLessSquare/Square_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./ExpressionLessSquare/SquareGame.xml ./ExpressionLessSquare/SquareGame_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./Square/Main.xml ./Square/Main_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./Square/Square.xml ./Square/Square_yuriko.xml
sh ~/nand2tetris/tools/TextComparer.sh ./Square/SquareGame.xml ./Square/SquareGame_yuriko.xml
