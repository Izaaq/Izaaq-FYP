"""
Izaaq bin Ahmad Izham - k19011071
Final Year Project - LOLCODE Interpreter

LOLCODE originally by Adam Lindsay - http://www.lolcode.org/
Uses SLY library for lexing and parsing - https://sly.readthedocs.io/en/latest/sly.html

LOLCODE Syntax - https://gist.github.com/sharmaeklavya2/8a0e2581baf969be0f64


CAN I HAZ FIRST CLASS?
"""

from sly import Lexer
from sly import Parser
import sys
import types

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

    # Define tokens as regular expressions, stored as raw strings
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

class ParserLOL(Parser):
    # tokens are passed from lexer to parser
    tokens = LexerLOL.tokens
    # setting precedence of binary tokens + unary negative operator
    # precedence = (
    #     ('left', "SUM_OF", "DIFF_OF"),
    #     ('left', "PRODUKT_OF", "QUOSHUNT_OF"),
    #     ('right', 'UMINUS'),
    # )

    def __init__(self):
        self.env = {}

    @_('HAI EOL statement_list KTHXBYE',
       'HAI EOL statement_list KTHXBYE EOL')
    def program(self, p):
        return

    @_('')
    def statement(self, p):
        pass

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('VISIBLE expr')
    def statement(self, p):
        return ('print', p.expr)

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

    @_('O_RLY expr YA_RLY statement OIC',
       'O_RLY expr YA_RLY statement NO_WAI statement OIC')  # update to include EOL tokens + statement list
    def statement(self, p):
        if len(p) == 5:
            return ('if', p.expr, p.statement)
        else:
            return ('elif', p.expr, ('branch', p.statement0, p.statement1))

    @_('IM_IN_YR IDENTIFIER statement IM_OUTTA_YR IDENTIFIER')  # update to include EOL tokens + statement list
    def statement(self, p):
        return ('loop', p.IDENTIFIER0, p.statement, p.IDENTIFIER1)

    @_('GTFO')
    def statement(self, p):
        return ('break')

    @_('HOW_IZ_I IDENTIFIER statement IF_U_SAY_SO')  # update to include EOL tokens + statement list + arg list
    def statement(self, p):
        return ('func_def', p.IDENTIFIER, p.statement)

    @_('I_IZ IDENTIFIER MKAY')
    def statement(self, p):
        return ('func_call', p.IDENTIFIER)

    @_('FOUND_YR expr')
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

    @_('KTHXBYE')
    def statement(self, p):
        sys.exit()

class Break(Exception):
    pass

class Return(Exception):
    pass

class ExecuteLOL:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int) or isinstance(result, float):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

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
                print("node 1 not none - moving")
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'int':
            return node[1]

        if node[0] == 'float':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'print':
            print(self.walkTree(node[1]))

        if node[0] == 'input':
            self.env[node[1]] = input()
            return node[1]

        if node[0] == 'var_def':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var_declare':
            if node[1] not in self.env:
                self.env[node[1]] = None
            else:
                raise Exception("NAEM '%s' ALREDDEH TAKEN YA DUMMEH" % node[1])

        if node[0] == 'assign':
            try:
                self.env[node[1]] = self.walkTree(node[2])
                return self.env[node[1]]
            except LookupError:
                print("WHAT THE HELL IS A '%s'?!?!" % node[1])

        if node[0] == 'convert':
            if node[2] == 'YARN':
                self.env[node[1]] = str(self.env[node[1]])
            elif node[2] == 'NUMBR':
                try:
                    self.env[node[1]] = int(self.env[node[1]])
                except ValueError:
                    print("")

            elif node[2] == 'NUMBAR':
                self.env[node[1]] = float(self.env[node[1]])
            else:
                raise Exception("Cannot convert identifier: %s to type %s" % (node[1], node[2]))

        if node[0] == 'if':
            if self.walkTree(node[1]):
                return self.walkTree(node[2])
        elif node[0] == 'elif':
            if self.walkTree(node[1]):
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'loop':
            try:
                while True:
                    self.walkTree(node[2])
            except Break:
                pass

        if node[0] == 'break':
            raise Break()

        if node[0] == 'func_def':
            if node[1] in self.env:
                print("MAEK A NEW NAEM PLZ !!11")
                return 0
            self.env[node[1]] = node[2]

        if node[0] == 'func_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("NO SUCH THING AS A '%s'" % node[1])

        if node[0] == 'return':
            return self.walkTree(node[1])

        if node[0] == 'not':
            return not self.walkTree(node[1])

        if node[0] == 'bin_op':
            if isinstance(self.walkTree(node[2]), str) or isinstance(self.walkTree(node[3]), str):
                print("UHOH!!!! NO YARN ALLOWED!!!!")
                return 0
            if node[1] == 'SUM OF':
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
            try:
                return self.env[node[1]]
            except LookupError:
                print("WHAT THE HELL IS A '%s'?!?!" % node[1])
                return 0

if __name__ == '__main__':
    lexer = LexerLOL()
    parser = ParserLOL()
    env = {}                # context table

    while True:
        try:
            text = input('LOL > ')
        except EOFError:
            break

        if text:
            lex = lexer.tokenize(text)
            # for token in lex:
            #     print(token)
            tree = parser.parse(lex)
            ExecuteLOL(tree, env)