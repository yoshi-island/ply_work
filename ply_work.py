# Python 3.5.0

# -----------------------------------------------------------------------------
# 日本語でプログラミング
# -----------------------------------------------------------------------------

tokens = (
#    'NAME','NUMBER',
#    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
#    'LPAREN','RPAREN',
    'EXIT',
    'HELP',
    'INPUT',
    'OUTPUT',
    'NUMBER',
    'VAR',
    'DICT',
    )

# Tokens

#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
#t_EQUALS  = r'='
#t_LPAREN  = r'\('
#t_RPAREN  = r'\)'
#t_NAME  = r'[A-Za-z一-龥ぁ-んァ-ン_][A-Za-z一-龥ぁ-んァ-ン0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

t_VAR = r'[A-Za-z一-龥ぁ-んァ-ン_][A-Za-z一-龥ぁ-んァ-ン0-9_]*'

# Ignored characters
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

def t_EXIT(t):
    r'退出|exit'
    return t

def t_HELP(t):
    r'ヘルプ|help'
    return t

def t_INPUT(t):
    r'入力|input'
    return t

def t_OUTPUT(t):
    r'出力|output'
    return t

def t_DICT(t):
    r'メモリ|辞書|dict|mem'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    

# Build the lexer
import ply.lex as lex
lexer = lex.lex()


# Parsing rules

#precedence = (
#    ('left','PLUS','MINUS'),
#    ('left','TIMES','DIVIDE'),
#    ('right','UMINUS'),
#    )

# dictionary of names
names = { }

#def p_statement_assign(t):
#    'statement : NAME EQUALS expression'
#    names[t[1]] = t[3]
#
#def p_statement_expr(t):
#    'statement : expression'
#    print(t[1])
#
#def p_expression_binop(t):
#    '''expression : expression PLUS expression
#                  | expression MINUS expression
#                  | expression TIMES expression
#                  | expression DIVIDE expression'''
#    if t[2] == '+'  : t[0] = t[1] + t[3]
#    elif t[2] == '-': t[0] = t[1] - t[3]
#    elif t[2] == '*': t[0] = t[1] * t[3]
#    elif t[2] == '/': t[0] = t[1] / t[3]
#
#def p_expression_uminus(t):
#    'expression : MINUS expression %prec UMINUS'
#    t[0] = -t[2]
#
#def p_expression_group(t):
#    'expression : LPAREN expression RPAREN'
#    t[0] = t[2]
#
#def p_expression_number(t):
#    'expression : NUMBER'
#    t[0] = t[1]
#
#def p_expression_name(t):
#    'expression : NAME'
#    try:
#        t[0] = names[t[1]]
#    except LookupError:
#        print("Undefined name '%s'" % t[1])
#        t[0] = 0

#def p_expression_order(t):
#    #'expression : ORDER expression'
#    'expression : ORDER EXPRE'
#    try:
#        names[t[1]] = t[1]
#    except LookupError:
#        print('Undefine expression %s' % t)
#        t[0] = 0


def p_help(t):
    'expression : HELP'
    print( """
         「退出」と入力すれば終了します
         「入力 <文字列>」と入力すると文字列を記憶します、10個まで記憶できます
         「辞書」と入力すると記憶した文字列を表示します
         「出力 <数字>」と入力すると記憶した文字列を表示します
    """ )

flag = 0
def p_input(t):
    'expression : INPUT VAR'
    names.update({flag:t[2]})
    global flag
    flag += 1

def p_output(t):
    'expression : OUTPUT NUMBER'
    print(names[t[2]])

def p_dict(t):
    'expression : DICT'
    print(names)

import sys
def p_exit(t):
    'expression : EXIT'
    print('また来てください')
    sys.exit()

def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

print("""==========================
「ヘルプ」と入力して「Enter」を押すと使い方が表示されます
==========================""")
while True:
    try:
        s = input('何か入力して「Enter」を押してください→ ')   # Use raw_input on Python 2
    except EOFError:
        break
    if not s: # ignore blank input
        continue
    #print("s is " + s)
    parser.parse(s)
