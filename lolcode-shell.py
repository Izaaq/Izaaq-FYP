"""
LOLCODE shell - To be run for code to work.

Izaaq bin Ahmad Izham - k19011071
"""

from lol.lexer import LexerLOL
from lol.parser import ParserLOL
from lol.interpreter import InterpreterLOL
import os

"""
LOLCODE file reader - file must exist in 'tests' directory and end in '.lolcode'.
"""
if __name__ == '__main__':
    lexer = LexerLOL()
    parser = ParserLOL()
    env = {}  # context table

    files = os.listdir('tests')
    for file in files[:]:
        if not file.endswith('.lolcode'):
            files.remove(file)

    while True:
        print("Valid files:")
        print(files)
        file = input("Enter file name (don't include .lolcode): ")
        file = file + ".lolcode"
        if file not in files:
            print("No such file found")
        else:
            break

    try:
        with open("tests\\" + file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise Exception("Error - File not found")
    except EOFError:
        raise Exception("EOF error")

    if lines:
        lex = lexer.tokenize(''.join(lines))
        tree = parser.parse(lex)
        # for token in lex:       # debugging
        #     print(token)
        # print(tree)
        InterpreterLOL(tree, env)
        # print(env)
