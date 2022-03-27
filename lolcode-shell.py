"""
LOLCODE shell - To be run for code to work.
Izaaq bin Ahmad Izham - k19011071
"""
from lol.lexer import LexerLOL
from lol.parser import ParserLOL
from lol.interpreter import InterpreterLOL
import os
import time

"""
LOLCODE file reader - file must exist in 'tests' directory and end in '.lol'.
"""
if __name__ == '__main__':
    lexer = LexerLOL()
    parser = ParserLOL()
    env = {}  # context table

    # filter out invalid files in 'tests' directory
    files = os.listdir('tests')
    for file in files[:]:
        if not file.endswith('.lol'):
            files.remove(file)

    while True:
        print("Valid files:")
        print(files)
        file = input("Enter file name (don't include .lol): ")
        file = file + ".lol"
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
        InterpreterLOL(tree, env)

    ##### Used for performance results
    # if lines:
    #     startTime = time.perf_counter()
    #     lex = lexer.tokenize(''.join(lines))
    #     tree = parser.parse(lex)
    #     InterpreterLOL(tree, env)
    #     endTime = time.perf_counter()
    #     print(f"Time taken: {endTime - startTime} seconds.")        # to measure time
