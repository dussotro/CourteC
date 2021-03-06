# coding: utf-8

import sys
from indent import Indent
from random import *

TYPE = ['ENTIER', 'CARACTERE', 'FLOTTANT']
FUNCTYPE =  ['ENTIER', 'CARACTERE', 'FLOTTANT', '2BE3']
STATEMENT_STARTERS = ['POUR', 'TANTQUE', 'ENFONCTIONDE', 'SI', 'SINON', 'CAS', 'PARDEFAUT']
REL_OP = ['ESTIL', 'DIFFERENT', 'PPQ', 'SPPQ', 'SPGQ', 'SPPQ']
OP = ['PLUSUN', 'MOINSUN', 'PLUS', 'MOINS', 'AJOUT', 'ENLEVE']
ASSIGN = ['EST']
LITERAL = ['ENTIER_LIT', 'FLOTTANT_LIT', 'CARACTERE_LIT']
PAREN = ['LPAREN', 'RPAREN']
MORE = ['STRUCTURE', 'DEFINITION', 'TAILLE', 'ET', 'OU']
BREAKER = ['RENVOIE']

class Parser:

    def __init__(self, verbose=False):
        self.indentator = Indent(verbose)
        self.tokens = []
        self.errors = 0


    def show_next(self, n=1):
        try:
            return self.tokens[n - 1]
        except IndexError:
            print('ERROR: no more tokens left!')
            sys.exit(1)

    def generate_error(self):
        chaine_ret = "Erreur :"
        for i in range(0,85):
            chaine_ret += chr(randint(33,126))
        print(chaine_ret)
        sys.exit(1)


    def expect(self, kind):
        if type(kind) == list:
            actualToken = self.show_next()
            actualKind = actualToken.kind
            if actualKind in kind:
                return self.accept_it()
            else:
                self.generate_error()
        else:
            actualToken = self.show_next()
            actualKind = actualToken.kind
            if actualKind == kind:
                return self.accept_it()
            else:
                self.generate_error()

    # same as expect() but no error if not correct kind
    def maybe(self, kind):
        if self.show_next().kind == kind:
            return self.accept_it()

    def accept_it(self):
        token = self.show_next()
        output = str(token.kind) + ' ' + token.value
        self.indentator.say(output)
        return self.tokens.pop(0)

    def remove_comments(self):
        result = []
        in_comment = False
        for token in self.tokens:
            if token.kind == 'COMMENT':
                pass
            elif token.kind == 'LCOMMENT':
                in_comment = True
            elif token.kind == 'RCOMMENT':
                in_comment = False
            else:
                if not in_comment:
                    result.append(token)
        return result

    #PARSE GLOBAL
    def parse(self, tokens):
        self.tokens = tokens
        self.tokens = self.remove_comments()
        self.calcul_politesse(tokens)
        self.parse_program()

    def calcul_politesse(self, tokens):
        nombrePlease = 0
        for i in tokens:
            if(i=="please"):
                nombrePlease+=1
        ratio = nombrePlease / len(tokens)
        if(ratio < 0.05 or ratio > 0.2):
            #self.generate_error()
            pass


    #PARSE DU PROGRAMME
    def parse_program(self):
        self.indentator.indent('Parsing Program')

        self.parse_typedefs()
        self.parse_structures()
        self.parse_functions()
        ###

        #réservé au main
        self.expect('ENTIER')
        self.expect('IDENTIFIER')
        self.expect('LPAREN')
        self.expect('RPAREN')
        self.expect('LPAREN')
        #print(self.show_next())
        if (self.show_next().kind=='VIRGULE'):
            self.accept_it()
            self.expect('PLEASE')
        self.expect('POINT')
        #print(self.show_next())


        self.parse_declarations()

        self.parse_statements()

        self.expect('RPAREN')
        self.expect('POINT')
        self.indentator.dedent()
        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

    #PARSE ENSEMBLE DE DECLARATIONS
    def parse_declarations(self):
        self.indentator.indent('Parsing Declarations')
        while (self.show_next().kind in TYPE):
            self.parse_declaration()
            #self.expect('POINT')
        self.indentator.dedent()

    #PARSE UNE DECLARATION
    def parse_declaration(self):
        self.indentator.indent('Parsing Declaration')
        self.expect(TYPE)
        self.expect('IDENTIFIER')
        if self.show_next().kind == 'LPAREN':
            self.accept_it()
            self.expect('ENTIER_LIT')
            self.expect('RPAREN')
        while self.show_next().kind == 'POINTVIRGULE':
            self.accept_it()
            self.expect('IDENTIFIER')
            if self.show_next().kind == 'LPAREN':
                self.accept_it()
                self.expect('ENTIER_LIT')
                self.expect('RPAREN')
        self.expect('POINT')
        self.indentator.dedent()

    #PARSE UN ENSEMBLE DE STATEMENTS
    def parse_statements(self):
        while (self.show_next().kind in STATEMENT_STARTERS or self.show_next().kind in BREAKER or self.show_next().kind == 'VIRGULE'):
            self.indentator.indent('Parsing statements')
            self.parse_statement()
            self.indentator.dedent()
            #print("==>", self.show_next().kind)

    #PARSE UN STATEMENT
    def parse_statement(self):
        self.indentator.indent('Parsing Statement')

        if(self.show_next().kind == 'POINT'):
            self.accept_it()
        if(self.show_next().kind == 'RPAREN'):
            self.accept_it()
            self.expect('POINT')
        if(self.show_next().kind == 'VIRGULE'):
            self.accept_it()
            self.expect('PLEASE')
            self.expect('POINT')
        elif(self.show_next().kind == 'LPAREN'):
            self.accept_it()
            self.parse_block()

        elif(self.show_next().kind == 'IDENTIFIER'):
            self.accept_it()
            self.parse_assignement()

        elif(self.show_next().kind in BREAKER):
            self.parse_breaker()

        elif(self.show_next().kind == 'SI'):
            self.parse_if()
            while(self.show_next().kind in STATEMENT_STARTERS or self.show_next().kind in BREAKER or self.show_next().kind == 'IDENTIFIER' or self.show_next().kind == 'POINT'):
                self.parse_statement()
            self.expect('RPAREN')
            self.expect('POINT')
            if(self.show_next().kind == 'SINON'):
                self.accept_it()
                if(self.show_next().kind == 'LPAREN'):
                    self.accept_it()
                    while(self.show_next().kind in STATEMENT_STARTERS):
                        self.parse_statement()
                elif(self.show_next().kind == 'SI'):
                    self.parse_if()
                    while(self.show_next().kind in STATEMENT_STARTERS):
                        self.parse_statement()

        elif(self.show_next().kind == 'TANTQUE'):
            self.parse_while()
            while(self.show_next().kind in STATEMENT_STARTERS or self.show_next().kind=='IDENTIFIER'):
                self.parse_statement()
            #print('===|>', self.show_next())
            self.expect('RPAREN')
            self.expect('POINT')
            #print(self.show_next())

        else:
            print('Error parse statement')
            sys.exit(1)
        """
        print("---")
        print(self.show_next())
        print(self.show_next(2))
        print("---")
        """
        self.indentator.dedent()

    #PARSE UN BLOCK
    def parse_block(self):
        self.indentator.indent('Parsing block')
        self.expect('LPAREN')
        self.parse_statements()
        self.expect('RPAREN')
        self.indentator.dedent()

    #PARSE CONDITION IF
    def parse_if(self):
        self.indentator.indent('Parsing if')
        self.accept_it()
        self.expect('LPAREN')
        self.parse_expressions()
        self.expect('RPAREN')
        self.expect('LPAREN')
        self.expect('POINT')
        self.indentator.dedent()

    #PARSE BOUCLE WHILE
    def parse_while(self):
        self.indentator.indent('Parsing while')
        self.accept_it()
        self.expect('LPAREN')
        self.parse_expressions()
        self.expect('RPAREN')
        self.expect('LPAREN')
        self.expect('POINT')
        self.indentator.dedent()

    def parse_expressions(self):
        self.indentator.indent('Parsing expressions')
        self.parse_expression()
        while (self.show_next().kind in MORE):
            self.accept_it()
            self.parse_expression()
        self.indentator.dedent()

    #PARSE UNE EXPRESSION DE CONDITION (ex : dans une condition de if)
    def parse_expression(self):
        self.indentator.indent('Parsing expression')
        if(self.show_next().kind in LITERAL):
            val = self.show_next().kind
            self.accept_it()
            if(self.show_next().kind in REL_OP or self.show_next().kind in MUL_OP):
                self.accept_it()
                if(self.show_next().kind == val):
                    self.accept_it()
                elif(self.show_next().kind == 'IDENTIFIER'):
                    self.accept_it()
                else:
                    self.generate_error()
            else :
                self.generate_error()
        elif(self.show_next().kind == 'IDENTIFIER'):
            self.accept_it()
            if(self.show_next().kind in REL_OP):
                self.accept_it()
                if(self.show_next().kind in LITERAL):
                    self.accept_it()
                elif(self.show_next().kind == 'IDENTIFIER'):
                    self.accept_it()
                else:
                    self.generate_error()
        else:
            self.generate_error()
        self.indentator.dedent()

    #PARSE UNE ASSIGNATION (ex : a = a * 2)
    def parse_assignement(self):
        self.indentator.indent('Parsing assignement')
        cpt_parentheses = 0 #compteur qui va nous servir a detecter un "unbalanced parenthesis"
        while (self.show_next().kind in OP or self.show_next().kind in LITERAL or self.show_next().kind in PAREN or self.show_next().kind == 'IDENTIFIER'):
            if(self.show_next().kind == 'LPAREN'):
                cpt_parentheses += 1
            elif(self.show_next().kind == 'RPAREN'):
                cpt_parentheses -= 1
            self.accept_it()
        if self.show_next().kind=='VIRGULE':
            self.accept_it()
            self.expect('PLEASE')
        self.expect('POINT')
        if(cpt_parentheses != 0):
            self.generate_error()
        self.indentator.dedent()

    def parse_structures(self):
        self.indentator.indent('Parsing structures')
        while (self.show_next().kind == 'STRUCTURE'):
            self.expect('STRUCTURE')
            self.expect('IDENTIFIER')
            self.expect('LPAREN')
            self.parse_declarations()
            self.expect('RPAREN')
            self.expect('POINT')
        self.indentator.dedent()

    def parse_typedefs(self):
        self.indentator.indent('Parsing typedefs')
        while (self.show_next().kind == 'TYPEDEF'):
            self.expect('TYPEDEF')
            for i in range(2):
                if self.show_next().kind in TYPE or self.show_next().kind == 'IDENTIFIER' or self.show_next().kind == 'UNSIGNED':
                    if self.show_next().kind == 'UNSIGNED':
                        self.accept_it()
                        if self.show_next().kind in TYPE or self.show_next().kind == 'IDENTIFIER':
                            self.accept_it()
                        else:
                            self.generate_error()
                    else:
                        self.accept_it()
            self.expect('SEMICOLON')
        self.indentator.dedent()

    def parse_breaker(self):
        self.indentator.indent('Parsing breaker')
        self.accept_it()
        self.expect('SEMICOLON')
        self.indentator.dedent()

    def parse_functions(self):
        while self.show_next(2).value != 'main' and self.show_next(2).kind == 'IDENTIFIER' and self.show_next(3).kind == 'LPAREN':
            if self.show_next().kind in TYPE: self.accept_it()
            self.expect('IDENTIFIER')
            self.expect('LPAREN')
            if self.show_next().kind in TYPE:
                self.accept_it()
                self.expect('IDENTIFIER')
            while self.show_next().kind == 'COMMA':
                self.accept_it()
                #if self.show_next().kind in TYPE: self.accept_it()
                self.expect(TYPE)
                self.expect('IDENTIFIER')
            self.expect('RPAREN')
            self.expect('LBRACE')

            self.parse_declarations()
            self.parse_statements()

            self.expect('RBRACE')
