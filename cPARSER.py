
from makePy import *
import ply.lex as lex
# List of token names
tokens = (
    'INT',
    'CHAR',
    'INT_STAR',
    'CHAR_STAR',
    'STRING',
    'VOID',
    'BOOLEAN',
    'IF',
    'ELSE',
    'WHILE',
    'RETURN',
    'NUM',
    'ID',
    'GE',
    'LE',
    'EE',
    'NE',
    'ANNOTATION'
)
literals = ['=', '+', '-', '*', '/',
            '(', ')', ';', '<', '>', '{', '}', ',', '[', ']']
t_INT = r'int'
t_CHAR = r'char'
t_CHAR_STAR = r'char\*'
t_INT_STAR = r'int\*'
t_VOID = r'void'
t_BOOLEAN = r'true|false'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_RETURN = r'return'
t_ID = r'(?!true|false|int|char|void|if|else|while|return)[a-zA-Z_][a-zA-Z0-9_]*'
t_NUM = r'[0-9]+'
t_GE = r'>='
t_LE = r'<='
t_EE = r'=='
t_NE = r'!='

t_ignore = " \t\r"  # ignore ' ', '\t', '\r'

# A regular expression rule with some action code


def t_ANNOTATION_1(t):
    r'/\*([a-zA-Z0-9 _]|\r|\n|\t|\s)*\*/'  # regular expression 1
    t.lexer.lineno += t.value.count('\n')  # number of lines
    pass  # ignore this token as annotation


def t_ANNOTATION_2(t):
    r'//([a-zA-Z0-9 _]|\r|\n|\t|\s)*'  # regular expression 2
    t.lexer.lineno += t.value.count('\n')  # number of lines
    pass  # ignore this token as annotation

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print("(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
    t.lexer.skip(1)


def t_STRING(t):
    r"""("(\\.|[^"])*")|('(\\.|[^'])*')"""
    return t


lex.lex()# 调用Lex模块，构建词法分析器

#==============================================================================
#语法分析部分
#产生式production
#==============================================================================
start = 'start'

# start到声明
def p_start(p):
    '''start : declaration_list'''
    p[0] =make_program(p[1])

# 声明自增
def p_declaration_list_1(p):
    '''declaration_list : declaration_list declaration'''
    p[0] =make_statementlist(p[1],p[2])
def p_declaration_list_2(p):
    '''declaration_list : declaration'''
    p[0] = declaration_list_2(p[1])

# 两种声明
def p_declaration_1(p):
    '''declaration : var_declaration'''
    p[0] = declaration(p[1])
def p_declaration_2(p):
    '''declaration : fun_declaration'''
    p[0]= declaration(p[1])

# 变量声明
def p_var_declaration_1(p):
    '''var_declaration : type_specifier ID ';' '''
    p[0]= var_declaration_1(p[1], p[2], p[3])
def p_var_declaration_2(p):
    '''var_declaration : type_specifier ID '[' NUM ']' '=' '{' numlist '}' ';' '''
    p[0] = var_declaration_2(p[1], p[2],p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])
    #p[0]=p[2]+p[6]+'['+p[8]+']'
def p_var_declaration_3(p):
    '''var_declaration : type_specifier ID '[' NUM ']' '=' STRING ';' '''
    p[0] = var_declaration_3(p[1], p[2],p[3],p[4], p[5], p[6], p[7], p[8])
    #p[0]=p[2]+p[6]+p[7]

#类型符到具体类型
def p_type_specifier_int(p):
    '''type_specifier : INT'''
    p[0] = make_token(p[1])
    #p[0]=p[1]
def p_type_specifier_void(p):
    '''type_specifier : VOID'''
    p[0] = make_token(p[1])
    #p[0]=p[1]
def p_type_specifier_char(p):
    '''type_specifier : CHAR'''
    p[0] = make_token(p[1])
    #p[0]=p[1]
def p_type_specifier_char_star(p):
    '''type_specifier : CHAR_STAR'''
    p[0] = make_token(p[1])
    #p[0]=p[1]
def p_type_specifier_int_star(p):
    '''type_specifier : INT_STAR'''
    p[0] = make_token(p[1])
    #p[0]=p[1]

# 函数声明
def p_fun_declaration_1(p):
    '''fun_declaration : type_specifier ID '(' params ')' statement_block'''
    p[0] = make_function(p[1],p[2], p[3],p[4],p[5], p[6])
def p_fun_declaration_2(p):
    '''fun_declaration : statement_block'''
    p[0] = fun_declaration_2(p[1])
    #p[0]=p[1]

# 函数参数
def p_params_1(p):
    '''params : param_list'''
    p[0] = params_1(p[1])
    #p[0] = p[1]
def p_params_2(p):
    '''params : VOID'''
    p[0] = make_token(p[1])
    #p[0]=p[1]
def p_params_empty(p):
    '''params : '''
    p[0]=make_empty()

def p_param_list_1(p):
    '''param_list : param_list ',' param'''
    p[0] = make_parameterlist(p[1], p[3])
def p_param_list_2(p):
    '''param_list : param'''
    p[0] = params_1(p[1])
    #p[0]=p[1]

def p_param_1(p):
    '''param : type_specifier ID'''
    p[0] = param_1(p[1], p[2])
    #p[0]=p[2]
def p_param_2(p):
    '''param : type_specifier ID '[' ']' '''
    p[0] = param_2(p[1], p[2], p[3], p[4])
    #p[0]=p[2]

# 函数声明block
def p_statement_block_1(p):
    '''statement_block : '{' statement_list '}' '''
    p[0] = statement_block_1(p[1], p[2], p[3])
    #p[0]=p[2]

# 函数语句自增
def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
    p[0] = make_statementlist(p[1], p[2])
        
def p_statement_list_empty(p):
    '''statement_list : '''
    p[0] = make_empty()

# 函数语句分类
def p_statement_1(p):
    '''statement : expression_statement'''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_statement_2(p):
    '''statement : statement_block'''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_statement_3(p):
    '''statement : if_else_statements'''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_statement_4(p):
    '''statement : while_statments'''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_statement_5(p):
    '''statement : return_statements'''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_statement_6(p):
    '''statement : var_declaration'''
    p[0] = statement(p[1])
    #p[0]=p[1]

# expression
def p_expression_statement_1(p):
    '''expression_statement : expression ';' '''
    p[0] = statement(p[1])
    #p[0]=p[1]
def p_expression_statement_2(p):
    '''expression_statement : ';' '''
    p[0]=make_empty()

# if_else分支 block
def p_if_else_statements_1(p):
    '''if_else_statements : IF '(' expression ')' statement'''
    p[0]=make_statement_if_block(p[3],p[5],make_empty())
def p_if_else_statements_2(p):
    '''if_else_statements : IF '(' expression ')' statement ELSE statement'''
    p[0] = make_statementlist( make_statement_if_block(p[3], p[5], make_empty()),make_statement_else_block(p[7]))

# while循环block
def p_while_statments_1(p):
    '''while_statments : WHILE '(' expression ')' statement'''
    p[0] = make_statement_while(p[3], p[5])

#return语句
def p_return_statements_1(p):
    '''return_statements : RETURN ';' '''
    p[0] = make_statement_return(make_empty())
def p_return_statements_2(p):
    '''return_statements : RETURN expression ';' '''
    p[0] = make_statement_return(p[2])


# 赋值语句
def p_expression_1(p):
    '''expression : var '=' expression'''
    p[0] = make_statement_assign_1(p[1],p[2],p[3])

def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = expression_2(p[1])
    #p[0] = p[1]

# 定义+赋值
def p_expression_3(p):
    '''expression : type_specifier var '=' expression'''
    p[0] = make_statement_assign_1(p[2],p[3],p[4])

# 字符串和数组
def p_expression_4(p):
    '''expression : STRING '''
    p[0] = make_token(p[1])
    #p[0] = p[1]
def p_numlist_1(p):
    '''numlist : numlist ',' NUM '''
    p[0] = numlist_1(p[1], p[2], p[3])
    #p[0] =p[1]+p[2]+p[3]
def p_numlist_2(p):
    '''numlist : NUM  '''
    p[0] = make_token(p[1])
    #p[0] =p[1]

# 变量
def p_var_1(p):
    ''' var : ID'''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_var_2(p):
    ''' var : ID '[' expression ']' '''
    p[0] = var_2(p[1], p[2], p[3], p[4])
    #p[0]=p[1]+p[2]+p[3]+p[4]


def p_simple_expression_1(p):
    '''simple_expression : addsub_object relational_operator addsub_object'''
    p[0] = make_expression_logic(p[1], p[2], p[3])
def p_simple_expression_2(p):
    '''simple_expression : addsub_object'''
    p[0] = expression_2(p[1])
    #p[0]=p[1]

#关系运算符
def p_relational_operator_1(p):
    '''relational_operator : LE'''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_relational_operator_2(p):
    '''relational_operator : '<' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_relational_operator_3(p):
    '''relational_operator : '>' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_relational_operator_4(p):
    '''relational_operator : GE'''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_relational_operator_5(p):
    '''relational_operator : EE'''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_relational_operator_6(p):
    '''relational_operator : NE'''
    p[0] = make_token(p[1])
    #p[0] =p[1]

# 算术运算符
# 加减和乘除优先级分开
def p_addsub_object_1(p):
    '''addsub_object : addsub_object add_sub muldiv_object'''
    p[0] = make_statement_assign(p[1],p[2],p[3])
def p_addsub_object_2(p):
    '''addsub_object : muldiv_object'''
    p[0] = make_compute(p[1])
    #p[0]=p[1]

def p_muldiv_object_1(p):
    '''muldiv_object : muldiv_object mul_div object'''
    p[0]=make_statement_assign(p[1],p[2],p[3])
def p_muldiv_object_2(p):
    '''muldiv_object : object'''
    p[0] = make_compute(p[1])
    #p[0]=p[1]

# 四种运算符
def p_add_sub_1(p):
    '''add_sub : '+' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_add_sub_2(p):
    '''add_sub : '-' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_mul_div_1(p): 
    ''' mul_div : '*' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_mul_div_2(p):
    ''' mul_div : '/' '''
    p[0] = make_token(p[1])
    #p[0] =p[1]

# 基本运算数分类
def p_object_1(p):
    '''object : '(' expression ')' '''
    p[0] = object_1(p[1], p[2], p[3])
    # p[0]=p[1]+p[2]+p[3]
def p_object_2(p):
    '''object : var'''
    p[0] = make_compute(p[1])
    #p[0]=p[1]
def p_object_3(p):
    '''object : fun_value'''
    p[0] = make_compute(p[1])
    #p[0]=p[1]
def p_object_4(p):
    '''object : NUM'''
    p[0] = make_token(p[1])
    #p[0] =p[1]
def p_object_5(p):
    '''object : BOOLEAN'''
    p[0]=make_expression_bool(p[1])
    

# 函数返回值作运算数
def p_fun_value_1(p):
    ''' fun_value : ID '(' args ')' '''
    p[0] = fun_value_1(p[1], p[2], p[3], p[4])
    # p[0]=p[1]+p[2]+p[3]+p[4]

def p_args_1(p):
    '''args : arg_list'''
    p[0] = args(p[1])
    #p[0]=p[1]
def p_args_empty(p):
    '''args : '''
    p[0]=make_empty()

def p_arg_list_1(p):
    ''' arg_list : arg_list ',' expression'''
    p[0] = arg_list_1(p[1], p[2], p[3])
    #p[0]=p[1]+p[2]+p[3]
def p_arg_list_2(p):
    ''' arg_list : expression'''
    p[0] = args(p[1])
    #p[0]=p[1]

#错误处理，输出错误所在单词
def p_error(p):
    if p:
        print("Syntax error at '%s'" %p.value," line:%d"%p.lexer.lineno)

    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()