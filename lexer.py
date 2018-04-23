import re
import sys
from token import Token

regexExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'Entier\b', 'ENTIER'),
    (r'Flottant\b', 'FLOTTANT'),
    (r'Caractere\b', 'CARACTERE'),
    (r'Renvoie\b', 'RENVOIE'),
    (r'Structure\b', 'STRUCTURE'),
    (r'Definition\b', 'DEFINITION'),
    (r'Pour\b', 'POUR'),
    (r'Tantque\b', 'TANTQUE'),
    (r'taille\b', 'TAILLE'),
    (r'EnFonctionDe\b', 'ENFONCTIONDE'),
    (r'cas\b', 'CAS'),
    (r'ParDefaut\b', 'PARDEFAUT'),
    (r'Faire\b', 'FAIRE'),
    (r'2Be3\b', '2BE3'),
    (r'Sinon\b', 'SINON'),
    (r'Si\b', 'SI'),
    (r'si\b', 'SI'),
    (r'please\b', 'PLEASE'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\;', 'POINTVIRGULE'),
    (r'\:', 'DEUXPOINTS'),
    (r'\,', 'VIRGULE'),
    (r'\/\=\=\>', 'LCOMMENT'),
    (r'\<\=\=\/', 'RCOMMENT'),
    (r'\.', 'POINT'),
    (r'estil\b', 'EQ'),
    (r'est\b', 'ASSIGN'),
    (r'plusun\b', 'ADDADD'),
    (r'plus\b', 'ADDEQ'),
    (r'\+', 'ADD'),
    (r'moinsun\b', 'SUBSUB'),
    (r'moins\b', 'SUBEQ'),
    (r'\-', 'SUB'),
    (r'\*', 'MUL'),
    (r'\/', 'DIV'),
    (r'different\b', 'NEQ'),
    (r'ou\b', 'OU'),
    (r'sppq\b', 'SPPQ'),
    (r'ppq\b', 'PPQ'),
    (r'spgq\b', 'SPGQ'),
    (r'pgq\b', 'PGQ'),
    (r'et\b', 'ET'),
    (r'[a-zA-Z]\w*', 'IDENTIFIER'),
    (r'\d+\,\d+', 'FLOTTANT_LIT'),
    (r'\d+', 'ENTIER_LIT'),
    (r'\"[^\"]*\"', 'CHAINE_LIT'),
    (r'\'[^\"]*\'', 'CARACTERE_LIT')
]


class Lexer:

    def __init__(self):
        self.tokens = []

    # inputText = open("testFile.c").readlines()
    def lex(self, inputText):

        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                        break
                if not match:
                    print(line[position])
                    print("no match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("lexer: analysis successful!")
        return self.tokens
