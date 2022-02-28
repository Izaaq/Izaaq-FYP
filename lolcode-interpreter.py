"""
Izaaq bin Ahmad Izham - k19011071
Final Year Project - LOLCODE Interpreter

LOLCODE originally by Adam Lindsay - http://www.lolcode.org/
Uses SLY library for lexing and parsing - https://sly.readthedocs.io/en/latest/sly.html
LOLCODE Syntax - https://gist.github.com/sharmaeklavya2/8a0e2581baf969be0f64

CAN I HAZ FIRST CLASS?

TO-DO:
- implement boolean
- get "FOUND YR"/return to work
- allow functions to take parameters
- maybe "ANY OF", "ALL OF", "EITHER OF", "BOTH OF"
- maybe type casting?
- maybe switch case?
"""

from sly import Lexer
from sly import Parser

"""
Lexer class - Makes tokens using inputs
"""
class LexerLOL(Lexer):
    tokens = {
        IDENTIFIER,
        STRING,
        INTEGER,
        FLOAT,
        BOOLEAN,
        I_HAS_A,
        ITZ,
        R,
        MAEK,
        A,
        IS_NOW_A,
        TYPE,
        VISIBLE,
        GIMMEH,
        SUM_OF,
        DIFF_OF,
        PRODUKT_OF,
        QUOSHUNT_OF,
        MOD_OF,
        BIGGR_OF,
        SMALLR_OF,
        BOTH_OF,
        EITHER_OF,
        WON_OF,
        NOT,
        ALL_OF,
        ANY_OF,
        SMOOSH,
        MKAY,
        BOTH_SAEM,
        DIFFRINT,
        O_RLY,
        YA_RLY,
        NO_WAI,
        IM_IN_YR,
        IM_OUTTA_YR,
        GTFO,
        HAI,
        KTHXBYE,
        HOW_IZ_I,
        I_IZ,
        YR,
        AN,
        FOUND_YR,
        IF_U_SAY_SO,
        OIC,
        EOL,
    }

    ignore = ' \t'  # ignore whitespace and indentation
    ignore_comment = r'BTW\s[^\n]*'   # ignore anything after BTW, comment code
    literals = { '!' }

    # Define regex for tokens to be recognized in input
    I_HAS_A         = r'I\s+HAS\s+A\b'
    ITZ             = r'ITZ\b'
    R               = r'R\b'
    MAEK            = r'MAEK\b'
    IS_NOW_A        = r'IS\s+NOW\s+A\b'
    A               = r'A\b'
    TYPE            = r'((?:NUMBA?R)|(?:YARN)|(?:TROOF)|(?:NOOB))\b'
    VISIBLE         = r'VISIBLE\b'
    GIMMEH          = r'GIMMEH\b'
    SUM_OF          = r'SUM\s+OF\b'
    DIFF_OF         = r'DIFF\s+OF\b'
    PRODUKT_OF      = r'PRODUKT\s+OF\b'
    QUOSHUNT_OF     = r'QUOSHUNT\s+OF\b'
    MOD_OF          = r'MOD\s+OF\b'
    BIGGR_OF        = r'BIGGR\s+OF\b'
    SMALLR_OF       = r'SMALLR\s+OF\b'
    BOTH_OF         = r'BOTH\s+OF\b'
    EITHER_OF       = r'EITHER\s+OF\b'
    WON_OF          = r'WON\s+OF\b'
    NOT             = r'NOT\b'
    ALL_OF          = r'ALL\s+OF\b'
    ANY_OF          = r'ANY\s+OF\b'
    SMOOSH          = r'SMOOSH\s+\b'
    MKAY            = r'MKAY\b'
    BOTH_SAEM       = r'BOTH\s+SAEM\b'
    DIFFRINT        = r'DIFFRINT\b'
    O_RLY           = r'O\s+RLY\b'
    YA_RLY          = r'YA\s+RLY\b'
    NO_WAI          = r'NO\s+WAI\b'
    IM_IN_YR        = r'IM\s+IN\s+YR\b'
    IM_OUTTA_YR     = r'IM\s+OUTTA\s+YR\b'
    GTFO            = r'GTFO\b'
    HAI             = r'HAI\b'
    KTHXBYE         = r'KTHXBYE\b'
    HOW_IZ_I        = r'HOW\s+IZ\s+I\b'
    I_IZ            = r'I\s+IZ\b'
    YR              = r'YR\b'
    AN              = r'AN\b'
    FOUND_YR        = r'FOUND\s+YR\b'
    IF_U_SAY_SO     = r'IF\s+U\s+SAY\s+SO\b'
    OIC             = r'OIC\b'

    IDENTIFIER      = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'[+-]?\d+\.\d+')
    def FLOAT(self, t):
        # convert into python float
        t.value = float(t.value)
        return t

    @_(r'[+-]?\d+')
    def INTEGER(self, t):
        # convert it into python integer
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def STRING(self, t):
        # convert into python string - remove double quotes
        t.value = str(t.value).strip('"')
        return t

    @_(r'(?:WIN)|(?:FAIL)')
    def BOOLEAN(self, t):
        return t

    @_(r'BTW\s[^\n]*')
    def COMMENT(self, t):
        pass

    @_(r',|\n')
    def EOL(self, t):
        if t.value == '\n':
            self.lineno += 1
        t.value = 'EOL'
        return t

    # Newline token
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

"""
Parser class - Define grammar 
"""
class ParserLOL(Parser):
    # tokens are passed from lexer to parser
    tokens = LexerLOL.tokens

    def __init__(self):
        self.env = {}

    # define grammar

    # programs must start with 'HAI' and end with 'KTHXBYE'
    @_('HAI EOL statement_list KTHXBYE',
       'HAI EOL statement_list KTHXBYE EOL')
    def program(self, p):
        return ('start', p.statement_list)

    @_('statement_list statement EOL',
       'statement EOL')
    def statement_list(self, p):
        if len(p) == 3:
            return (p[0] + [p[1]])
        else:
            return ([p[0]])

    @_('')
    def statement(self, p):
        pass

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('VISIBLE expr "!"',
       'VISIBLE expr')
    def statement(self, p):
        if len(p) == 3:
            return ('print', p.expr)
        return ('printline', p.expr)

    @_('GIMMEH IDENTIFIER')
    def statement(self, p):
        return ('input', p.IDENTIFIER)

    @_('I_HAS_A IDENTIFIER ITZ expr',
       'I_HAS_A IDENTIFIER')
    def statement(self, p):
        if len(p) == 4:
            return ('var_def', p.IDENTIFIER, p.expr)
        return ('var_declare', p.IDENTIFIER)

    @_('IDENTIFIER R expr')
    def statement(self, p):
        return ('assign', p.IDENTIFIER, p.expr)

    @_('IDENTIFIER IS_NOW_A TYPE')
    def statement(self, p):
        return ('convert', p.IDENTIFIER, p.TYPE)

    @_('O_RLY expr EOL YA_RLY EOL statement_list OIC',
       'O_RLY expr EOL YA_RLY EOL statement_list NO_WAI EOL statement_list OIC')
    def statement(self, p):
        if len(p) == 7:
            return ('if', p.expr, p.statement_list)
        else:
            return ('if-else', p.expr, ('branch', p.statement_list0, p.statement_list1))

    @_('IM_IN_YR IDENTIFIER EOL statement_list IM_OUTTA_YR IDENTIFIER')
    def statement(self, p):
        return ('loop', p.IDENTIFIER0, p.statement_list, p.IDENTIFIER1)

    @_('GTFO')
    def statement(self, p):
        return ('break', p[0])

    @_('HOW_IZ_I IDENTIFIER EOL statement_list IF_U_SAY_SO')  # update to include arg list
    def statement(self, p):
        return ('func_def', p.IDENTIFIER, p.statement_list)

    @_('I_IZ IDENTIFIER MKAY')
    def statement(self, p):
        return ('func_call', p.IDENTIFIER)

    @_('FOUND_YR expr')  # update for working functionality
    def statement(self, p):
        return ('return', p.expr)

    @_('NOT expr')
    def expr(self, p):
        return ('not', p.expr)

    @_('SUM_OF expr AN expr',
       'DIFF_OF expr AN expr',
       'PRODUKT_OF expr AN expr',
       'QUOSHUNT_OF expr AN expr',
       'MOD_OF expr AN expr',
       'BIGGR_OF expr AN expr',
       'SMALLR_OF expr AN expr',
       'WON_OF expr AN expr')
    def expr(self, p):
        return ('bin_op', p[0], p.expr0, p.expr1)

    @_('BOTH_SAEM expr AN expr',
       'DIFFRINT expr AN expr')
    def expr(self, p):
        return ('equality_check', p[0], p.expr0, p.expr1)

    @_('FLOAT')
    def expr(self, p):
        return ('float', p.FLOAT)

    @_('INTEGER')
    def expr(self, p):
        return ('int', p.INTEGER)

    @_('STRING')                    # update to include SMOOSH
    def expr(self, p):
        return ('str', p.STRING)

    @_('IDENTIFIER')
    def expr(self, p):
        return ('var', p.IDENTIFIER)

class Break(Exception):
    pass

class Return(Exception):
    pass

"""
Execute class 
Responsible for functionality
"""
class ExecuteLOL:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if result is not None and isinstance(result, float):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    # execute every statement in statement list
    def executeStatements(self, statements):
        if statements:
            try:
                for statement in statements:
                    self.walkTree(statement)
            except Break:
                raise Break
            except Return:
                raise Return
            except Exception as e:
                raise e

    # return value of variable
    def getVariable(self, name):
        try:
            return self.env[name]
        except KeyError:
            raise Exception("DA FAWK IS A '%s'???" % name)

    # set value of variable
    def setVariable(self, name, value):
        if name in self.env:
            self.env[name] = value
        else:
            raise Exception("DA FAWK IS A '%s'???" % name)

    # make a new variable
    def declareVariable(self, name):
        if name not in self.env:
            self.env[name] = None
        else:
            raise Exception("NAEM '%s' ALREDDEH TAKEN!!" % name)

    # recursively walk AST
    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if isinstance(node, float):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] is None:
                print("node 1 is none")
                self.walkTree(node[2])
            else:
                print("node 1 not none")
                print(node[1])
                print(node[2])
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'int':
            return node[1]

        if node[0] == 'float':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'print':
            print(self.walkTree(node[1]), end='')
        elif node[0] == 'printline':
            print(self.walkTree(node[1]))

        if node[0] == 'input':
            self.env[node[1]] = input("GIB INPUT!!!11: ")

        if node[0] == 'var_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], self.walkTree(node[2]))

        if node[0] == 'var_declare':
            self.declareVariable(node[1])

        if node[0] == 'assign':
            self.setVariable(node[1], self.walkTree(node[2]))

        if node[0] == 'convert':
            if node[2] == 'YARN':
                self.setVariable(node[1], str(self.getVariable(node[1])))
            elif node[2] == 'NUMBR':
                try:
                    self.setVariable(node[1], int(self.getVariable(node[1])))
                except ValueError:
                    raise Exception("YARN IS NOT A NUMBR!!11")
            elif node[2] == 'NUMBAR':
                try:
                    self.setVariable(node[1], float(self.getVariable(node[1])))
                except ValueError:
                    raise Exception("YARN IS NOT A NUMBAR!!11.1")
            else:
                raise Exception("Cannot convert identifier '%s' to type %s" % (node[1], node[2]))

        if node[0] == 'if':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
        elif node[0] == 'if-else':
            if self.walkTree(node[1]):
                self.executeStatements(node[2][1])
            else:
                self.executeStatements(node[2][2])

        # LOLCODE - loops execute forever until 'GTFO' reached.
        if node[0] == 'loop':
            try:
                while True:
                    self.executeStatements(node[2])
            except Break:
                pass

        if node[0] == 'break':
            raise Break()

        if node[0] == 'func_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], node[2])

        if node[0] == 'func_call':
            try:
                self.executeStatements(self.env[node[1]])
            except LookupError:
                print("NO SUCH THING AS A '%s'" % node[1])

        if node[0] == 'return':
            return self.walkTree(node[1])

        if node[0] == 'not':
            return not self.walkTree(node[1])

        if node[0] == 'bin_op':
            if isinstance(self.walkTree(node[2]), str) or isinstance(self.walkTree(node[3]), str):
                raise Exception("UHOH!!!! NO YARN ALLOWED!!!!")
            elif node[1] == 'SUM OF':
                return self.walkTree(node[2]) + self.walkTree(node[3])
            elif node[1] == 'DIFF OF':
                return self.walkTree(node[2]) - self.walkTree(node[3])
            elif node[1] == 'PRODUKT OF':
                return self.walkTree(node[2]) * self.walkTree(node[3])
            elif node[1] == 'QUOSHUNT OF':
                return self.walkTree(node[2]) / self.walkTree(node[3])
            elif node[1] == 'MOD OF':
                return self.walkTree(node[2]) % self.walkTree(node[3])
            elif node[1] == 'WON OF':
                return self.walkTree(node[2]) ** self.walkTree(node[3])

        if node[0] == 'equality_check':
            if node[1] == 'BOTH SAEM':
                return self.walkTree(node[2]) == self.walkTree(node[3])
            elif node[1] == 'DIFFRINT':
                return self.walkTree(node[2]) != self.walkTree(node[3])

        if node[0] == 'var':
            return self.getVariable(node[1])

        if node[0] == 'start':
            self.executeStatements(node[1])

"""
LOLCODE file reader - file must exist in same directory 
"""
if __name__ == '__main__':
    lexer = LexerLOL()
    parser = ParserLOL()
    env = {}

    try:
        with open('fib.lolcode') as f:
            lines = f.readlines()
    except EOFError:
        raise Exception("EOF error")

    if lines:
        lex = lexer.tokenize(''.join(lines))
        tree = parser.parse(lex)
        ExecuteLOL(tree, env)

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
#             # for token in lex:
#             #     print(token)
#             tree = parser.parse(lex)
#             print("tree")
#             print(tree)
#             print("environment")
#             print(env)
#             ExecuteLOL(tree, env)