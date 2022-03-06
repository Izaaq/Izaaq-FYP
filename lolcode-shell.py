from lexer import LexerLOL
from parser import ParserLOL
from interpreter import ExecuteLOL
import os

"""
LOLCODE file reader - file must exist in same directory 
"""
if __name__ == '__main__':
    lexer = LexerLOL()
    parser = ParserLOL()
    env = {}  # context table

    files = os.listdir()
    for file in files[:]:
        if not file.endswith('.lolcode'):
            files.remove(file)

    while True:
        print("Here are valid files: ")
        print(files)
        file = input("Enter file name (must include .lolcode): ")
        if file not in files:
            print("No such file found.")
        else:
            break

    try:
        with open(file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise Exception("Error - File not found")
    except EOFError:
        raise Exception("EOF error")

    if lines:
        lex = lexer.tokenize(''.join(lines))
        tree = parser.parse(lex)
        execute = ExecuteLOL(tree, env)

"""
LOLCODE console - only one line, so must use ',' as EOL token
"""
# if __name__ == '__main__':
#     lexer = LexerLOL()
#     parser = ParserLOL()
#     env = {}                # context table
#
#     while True:
#         try:
#             text = input('LOL > ')
#         except EOFError:
#             break
#
#         if text:
#             lex = lexer.tokenize(text)
#             tree = parser.parse(lex)
#             # print(tree)
#             # print(env)
#             ExecuteLOL(tree, env)