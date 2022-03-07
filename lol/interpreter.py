from lol.lexer import LexerLOL
from lol.parser import ParserLOL
import os

# Meta classes
class Break(Exception):
    pass

class Return(Exception):
    pass

"""
Execute class 
Responsible for functionality
"""
class InterpreterLOL:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if result is not None and isinstance(result, float):
            print(result)
        if result is not None and isinstance(result, bool):
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
            raise Exception(f"DA FAWK IS A '{name}'???")

    # set value of variable
    def setVariable(self, name, value):
        if name in self.env:
            if value == 'WIN':
                self.env[name] = True
            elif value == 'FAIL':
                self.env[name] = False
            else:
                self.env[name] = value
        else:
            raise Exception(f"DA FAWK IS A '{name}'???")

    # make a new variable
    def declareVariable(self, name):
        if name not in self.env:
            self.env[name] = None
        else:
            raise Exception(f"NAEM '{name}' ALREDDEH TAKEN!!")

    def deleteVariable(self, name):
        try:
            self.env.pop(name)
        except KeyError:
            raise Exception("No such variable")

    # recursively walk AST
    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if isinstance(node, float):
            return node
        # if isinstance(node, bool):
        #     return node

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

        elif node[0] == 'int':
            return node[1]

        elif node[0] == 'float':
            return node[1]

        elif node[0] == 'str':
            return node[1]

        elif node[0] == 'bool':
            return node[1]

        elif node[0] == 'print':
            toPrint = self.walkTree(node[1])
            if isinstance(toPrint, bool):
                if toPrint:
                    print("WIN", end='')
                else:
                    print("FAIL", end='')
            else:
                print(toPrint, end='')
        elif node[0] == 'printline':
            toPrint = self.walkTree(node[1])
            if isinstance(toPrint, bool):
                if toPrint:
                    print("WIN")
                else:
                    print("FAIL")
            else:
                print(toPrint)

        elif node[0] == 'input':
            self.env[node[1]] = input()

        elif node[0] == 'var_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], self.walkTree(node[2]))

        elif node[0] == 'var_declare':
            self.declareVariable(node[1])

        elif node[0] == 'assign':
            self.setVariable(node[1], self.walkTree(node[2]))

        elif node[0] == 'convert':
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
                raise Exception(f"Cannot convert identifier '{node[1]}' to type {node[2]}")

        elif node[0] == 'if':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
        elif node[0] == 'if-else':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            else:
                self.executeStatements(node[3])
        elif node[0] == 'if-elif':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            elif self.walkTree(node[3]):
                self.executeStatements(node[4])
        elif node[0] == 'if-elif-else':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            elif self.walkTree(node[3]):
                self.executeStatements(node[4])
            else:
                self.executeStatements(node[5])

        # LOLCODE - loops execute forever until 'GTFO' reached.
        elif node[0] == 'loop':
            try:
                while True:
                    self.executeStatements(node[2])
            except Break:
                pass

        elif node[0] == 'break':
            raise Break()

        elif node[0] == 'func_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], node[2])

        elif node[0] == 'func_call':
            function = self.getVariable(node[1])
            try:
                self.declareVariable('ret')
                self.executeStatements(function)
            except LookupError:
                print(f"NO SUCH THING AS A '{node[1]}'")
            except Break:
                ret = None
            except Return:
                ret = self.getVariable('ret')
            finally:
                self.deleteVariable('ret')
            return ret

        elif node[0] == 'return':
            self.setVariable('ret', self.walkTree(node[1]))
            raise Return()

        elif node[0] == 'not':
            return not self.walkTree(node[1])

        elif node[0] == 'bin_op':
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

        elif node[0] == 'equality_check':
            if node[1] == 'BOTH SAEM':
                return self.walkTree(node[2]) == self.walkTree(node[3])
            elif node[1] == 'DIFFRINT':
                return self.walkTree(node[2]) != self.walkTree(node[3])
            elif node[1] == 'WON OF':
                return self.walkTree(node[2]) ^ self.walkTree(node[3])
            elif node[1] == 'BOTH OF':
                return self.walkTree(node[2]) and self.walkTree(node[3])
            elif node[1] == 'EITHER OF':
                return self.walkTree(node[2]) or self.walkTree(node[3])

        elif node[0] == 'var':
            return self.getVariable(node[1])

        elif node[0] == 'start':
            self.executeStatements(node[1])
