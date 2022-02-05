# LOLCODE Interpreter in Python by Izaaq Ahmad Izham - FYP Project
# Uses SLY (Sly Lex Yacc) lexer and parser: https://sly.readthedocs.io/en/latest/sly.html
# LOLCODE Syntax: https://github.com/justinmeza/lolcode-spec/blob/master/v1.2/lolcode-spec-v1.2.md
# SLY: https://github.com/dabeaz/sly/blob/master/docs/sly.rst

# CAN I HAZ FIRST CLASS?

from sly import Lexer
from sly import Parser
import sys

class LexerLOL(Lexer):
    tokens = {
        NAME,
        NUMBER,
        FLOAT,
        STRING,
        I_HAS_A,        # VAR
        ITZ,            # VAR ASSIGN
        SUM_OF,         # ADD
        DIFF_OF,        # MINUS
        PRODUKT_OF,     # MULTIPLY
        QUOSHUNT_OF,    # DIVIDE
        MOD_OF,         # INTEGER DIVISION (MODULO)
        BIGGR_OF,       # MAX OF TWO NUMBERS
        SMALLR_OF,      # MIN OF TWO NUMBERS
        GTFO,           # BREAK
        NOT,            # UNARY !
        BOTH_SAEM,      # ==
        DIFFRINT,       # !=
        WON_OF,         # POWER OPERATOR
        VISIBLE,        # PRINT
        AN,             # and (not logical binary, just for binary operators)
        DOWN,           # decrement
        UP,             # increment
        DOUBLE_EX,      # !! (for increments and decrements)
        O_RLY,          # if statement
        YA_RLY,         # then (for if)
        MEBBE,          # elif
        NO_WAI,         # else
        OIC,            # end if statement
        IM_IN_YR,       # start of loop
        IM_OUTTA_YR,    # end of loop
        HOW_IZ_I,       # function def
        IF_U_SAY_SO,    # end of function
        I_IZ,           # function call
        MKAY,           # end of function call
        FOUND_YR,       # return
        KTHXBYE,        # ends program
    }

    ignore = ' \t'  # ignore whitespace
    ignore_comment = r'BTW\s[^\n]*'
    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','!' }

    # Define tokens as regular expressions, stored as raw strings
    I_HAS_A         = r'I HAS A'
    ITZ             = r'ITZ'
    STRING          = r'\".*?\"'
    AN              = r'AN'
    SUM_OF          = r'SUM OF'
    DIFF_OF         = r'DIFF OF'
    PRODUKT_OF      = r'PRODUKT OF'
    QUOSHUNT_OF     = r'QUOSHUNT OF'
    MOD_OF          = r'MOD OF'
    BIGGR_OF        = r'BIGGR OF'
    SMALLR_OF       = r'SMALLR OF'
    WON_OF          = r'WON OF'
    NOT             = r'NOT'
    BOTH_SAEM       = r'BOTH SAEM'
    DIFFRINT        = r'DIFFRINT'
    VISIBLE         = r'VISIBLE'
    DOWN            = r'DOWN'
    UP              = r'UP'
    DOUBLE_EX       = r'!!'
    O_RLY           = r'O RLY'
    YA_RLY          = r'YA RLY'
    MEBBE           = r'MEBBE'
    NO_WAI          = r'NO WAI'
    OIC             = r'OIC'
    HOW_IZ_I        = r'HOW IZ I'
    IF_U_SAY_SO     = r'IF U SAY SO'
    FOUND_YR        = r'FOUND YR'
    I_IZ            = r'I IZ'
    MKAY            = r'MKAY'
    GTFO            = r'GTFO'
    KTHXBYE         = r'KTHXBYE'

    NAME            = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Float token
    @_(r'[+-]?\d+\.\d+')
    def FLOAT(self, t):
        # convert into python float
        t.value = float(t.value)
        return t

    # Number token
    @_(r'[+-]?\d+')
    def NUMBER(self, t):
        # convert it into python integer
        t.value = int(t.value)
        return t

    # Comment token
    @_(r'BTW\s[^\n]*')
    def COMMENT(self, t):
        pass

    # Newline token
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

class ParserLOL(Parser):
    # tokens are passed from lexer to parser
    tokens = LexerLOL.tokens
    # setting precedence of binary tokens + unary negative operator
    precedence = (
        ('left', "SUM_OF", "DIFF_OF"),
        ('left', "PRODUKT_OF", "QUOSHUNT_OF"),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    # @_('FOR var_assign TO expr THEN statement')
    # def statement(self, p):
    #     return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('O_RLY expr YA_RLY statement NO_WAI statement OIC')
    def statement(self, p):
        return ('if_else_stmt', p.expr, ('branch', p.statement0, p.statement1))

    @_('O_RLY expr YA_RLY statement OIC')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statement)

    @_('O_RLY expr YA_RLY statement MEBBE expr statement NO_WAI statement OIC')
    def statement(self, p):
        return ('if_elif_stmt', p.expr0, p.statement0, p.expr1, p.statement1, p.statement2)

    @_('HOW_IZ_I NAME statement IF_U_SAY_SO')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('I_IZ NAME MKAY')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('BOTH_SAEM expr AN expr')
    def expr(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('DIFFRINT expr AN expr')
    def expr(self, p):
        return ('condition_neq', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('I_HAS_A NAME ITZ expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('I_HAS_A NAME ITZ STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('SUM_OF expr AN expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('DIFF_OF expr AN expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('PRODUKT_OF expr AN expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('QUOSHUNT_OF expr AN expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('MOD_OF expr AN expr')
    def expr(self, p):
        return ('mod', p.expr0, p.expr1)

    @_('SMALLR_OF expr AN expr')
    def expr(self, p):
        return ('min', p.expr0, p.expr1)

    @_('BIGGR_OF expr AN expr')
    def expr(self, p):
        return ('max', p.expr0, p.expr1)

    @_('WON_OF expr AN expr')
    def expr(self, p):
        return ('power', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('DOWN NAME DOUBLE_EX expr')
    def statement(self, p):
        return ('decrement_var', p.NAME, p.expr)

    @_('DOWN expr DOUBLE_EX expr')
    def statement(self, p):
        return ('decrement_int', p.expr0, p.expr1)

    @_('UP NAME DOUBLE_EX expr')
    def statement(self, p):
        return ('increment_var', p.NAME, p.expr)

    @_('UP expr DOUBLE_EX expr')
    def statement(self, p):
        return ('increment_int', p.expr0, p.expr1)

    @_('VISIBLE expr')
    def statement(self, p):
        return ('print', p.expr)

    @_('VISIBLE STRING')
    def statement(self, p):
        return ('print', p.STRING)

    @_('VISIBLE NAME')
    def statement(self, p):
        return ('print_var', p.NAME)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('FLOAT')
    def expr(self, p):
        return ('float', p.FLOAT)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('GTFO')
    def statement(self, p):
        return ('break', p.GTFO)

    @_('FOUND_YR expr')
    def expr(self, p):
        return ('ret', p.expr)

    @_('KTHXBYE')
    def expr(self, p):
        return ('end')

class ExecuteLOL:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'float':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        elif node[0] == 'condition_neq':
            return self.walkTree(node[1]) != self.walkTree(node[2])

        if node[0] == 'if_else_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])
        elif node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2])
        elif node[0] == 'if_elif_stmt':
            result1 = self.walkTree(node[1])
            if result1:
                return self.walkTree(node[2])
            else:
                result2 = self.walkTree(node[3])
                if result2:
                    return self.walkTree(node[4])
            return self.walkTree(node[5])

        if node[0] == 'print':
            print(self.walkTree(node[1]))
        elif node[0] == 'print_var':
            try:
                print(self.env[node[1]])
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'mod':
            return self.walkTree(node[1]) % self.walkTree(node[2])

        if node[0] == 'min':
            return min(self.walkTree(node[1]), self.walkTree(node[2]))
        elif node[0] == 'max':
            return max(self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'decrement_int':
            number = self.walkTree(node[1])
            decrement = self.walkTree(node[2])
            toReturn = number - decrement
            return toReturn
        elif node[0] == 'decrement_var':
            try:
                number = self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0
            decrement = self.walkTree(node[2])
            toReturn = number - decrement
            return toReturn

        if node[0] == 'increment_int':
            number = self.walkTree(node[1])
            decrement = self.walkTree(node[2])
            toReturn = number + decrement
            return toReturn
        elif node[0] == 'increment_var':
            try:
                number = self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0
            decrement = self.walkTree(node[2])
            toReturn = number + decrement
            return toReturn

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'ret':
            return (self.walkTree(node[1]))

        if node[0] == 'end':
            print("end")
            sys.exit()

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
            for token in lex:
                print(token)
            tree = parser.parse(lexer.tokenize(text))
            ExecuteLOL(tree, env)
