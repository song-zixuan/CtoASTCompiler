def add_tab(text_str: str):
    return '\n'.join([('    ' + line_str) for line_str in str(text_str).split('\n')])


# 空语句处理
class make_empty:
    def __str__(self):
        return {'name': 'EmptyContext', 'token' : ''}
    def printtree(self):
        return {'name': 'EmptyContext', 'token' : 'EmptySpace'}

# 译出整个程序
class make_program:
    def __init__(self, declarations):
        self.declarations = declarations

    def __str__(self):
        return self.declarations.__str__()
    def printtree(self):
        return self.declarations.printtree()

# 译出函数
class make_function:
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6

    # def __str__(self):
    #     return str({'name':'FunctionContext', 'children': [self.name, self.args, self.block] })
    #     # return "def %s(%s):%s" % (self.name, self.args,add_tab(self.block))
    def printtree(self):
        return {'name':'FunctionContext', 'children': [self.p1.printtree(), {'token': self.p2}, {'token': self.p3},self.p4.printtree(), {'token': self.p5} , self.p6.printtree()] }

# 译出函数定义中的参数列表
class make_parameterlist:
    def __init__(self, prev, end):
        self.prev = prev
        self.end = end

    def __str__(self):
        return str({'name' : 'ParameterlistContext', 'children': [self.prev, self.end]})
        #return "%s, %s" % (self.prev, self.end)
    def printtree(self):
        return {'name' : 'ParameterlistContext', 'children': [self.prev.printtree(), self.end.printtree()]}

# 译出声明
class make_statementlist:
    def __init__(self, prev, end):
        self.prev = prev
        self.end = end

    def __str__(self):
        return str({'name' : 'StatementlistContext', 'children' : [self.prev.__str__(), self.end.__str__()]})
        #return "%s\n%s" % (self.prev, self.end)
    def printtree(self):
        return {'name' : 'StatementlistContext', 'children' : [self.prev.printtree(), self.end.printtree()]}

# 译出if块
class make_statement_if_block:
    def __init__(self, expression, statement_if, statement_else):
        self.expression = expression
        self.statement_if = statement_if
        self.statement_else = statement_else

    def __str__(self):
        # res_str = "if %s:%s" % (self.expression, add_tab(self.statement_if))
        # if type(self.statement_else) != make_empty:
        #     res_str = res_str + "\nelse:%s" % (add_tab(self.statement_else))
        
        if type(self.statement_else) != make_empty:
            return str({'name' : 'IfelseBlockContext', 'children' : [self.expression, self.statement_if, self.statement_else]})
        else:
            return str({'name' : 'IfBlockContext', 'children' : [self.expression, self.statement_if]})
        # return res_str
    def printtree(self):
        if type(self.statement_else) != make_empty:
            return {'name' : 'IfelseBlockContext', 'children' : [self.expression.printtree(), self.statement_if.printtree(), self.statement_else.printtree()]}
        else:
            return {'name' : 'IfBlockContext', 'children' : [self.expression.printtree(), self.statement_if.printtree()]}

#译出while块
class make_statement_while:
    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement

    def __str__(self):
        return str({'name': 'WhileBlockContect', 'children' : [self.expression, self.statement]})
        # return "while %s:%s" % (self.expression, add_tab(self.statement))
    def printtree(self):
        return {'name': 'WhileBlockContect', 'children' : [self.expression.printtree(), self.statement.printtree()]}

#译出赋值块
class make_statement_assign:
    def __init__(self, left, opt, right):
        self.left = left
        self.opt = opt
        self.right = right

    def __str__(self):
        return str({'name': 'MakeStatementAssignContext' , 'children': [self.left, self.opt, self.right]})
        #return "%s %s %s" % (self.left, self.opt, self.right)
    def printtree(self):
        return {'name': 'MakeStatementAssignContext' , 'children': [self.left.printtree(), self.opt.printtree(), self.right.printtree()]}

class make_statement_assign_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name' : 'MakeStatementAssignContext', 'children': [self.p1.printtree(),{'token': self.p2}, self.p3.printtree() ]}

# 译出return语句
class make_statement_return:
    def __init__(self, expression_return):
        self.expression_return = expression_return

    def __str__(self):
        return str({'name': 'MakeStatementReturnContext' , 'children': [self.expression_return]})
        #return "return %s" % self.expression_return
    def printtree(self):
        return {'name': 'MakeStatementReturnContext' , 'children': [self.expression_return.printtree()]}

# bool值翻译
class make_expression_bool:
    def __init__(self, bool_value):
        self.bool_value = bool_value

    def __str__(self):
        if self.bool_value == 'true':
            return str({'name' : 'BoolExpression', 'token' : 'True'})
            #return 'True'
        else:
            return str({'name' : 'BoolExpression', 'token' : 'False'})
            # return 'False'
    def printtree(self):
        return {'token' : self.bool_value}

# 译出表达式
class make_expression_logic:
    def __init__(self, left, opt, right):
        self.left = left
        self.opt = opt
        self.right = right

    # def __str__(self):
    #     opt_str = str(self.opt)
    #     opt_str = {'||': 'or', '&&': 'and', '!': 'not'}.get(opt_str, opt_str)
    #     return str({'name': 'ExpressionLogicContext', 'children' : [{'name': 'OperationContext', 'token' : opt_str}, self.left, self.right]})
    #     #return "%s %s %s" % (self.left, opt_str, self.right)
    def printtree(self):
        return {'name': 'ExpressionLogicContext', 'children' : [self.opt.printtree(), self.left.printtree(), self.right.printtree()]}

# 译出else块
class make_statement_else_block:
    def __init__(self, statement_else):
        self.statement_else = statement_else

    def __str__(self):
        return str({'name': 'StatementElseBlockContext', 'children' : [self.statement_else.__str__()]})
        # res_str = "else:%s" % (add_tab(self.statement_else))
        # return res_str
    def printtree(self):
        return {'name': 'StatementElseBlockContext', 'children' : [self.statement_else.printtree()]}

# added cPARSER

class declaration_list_2:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'DeclarationListContext', 'children': [self.p.printtree()]}

class declaration:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'DeclarationContext', 'children': [self.p.printtree()]}

class var_declaration_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name': 'VarDeclaration', 'children': [self.p1.printtree(), {'token' : self.p2}, {'token' : self.p3}]}

class var_declaration_2:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9
        self.p10 = p10

    def printtree(self):
        return {'name': 'VarDeclaration', 'children': [self.p1.printtree(), {'token': self.p2}, {'token': self.p3},{'token': self.p4},{'token': self.p5}, {'token': self.p6}, {'token': self.p7}, self.p8.printtree(),{'token': self.p9},{'token': self.p10} ]}

class var_declaration_3:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8

    def printtree(self):
        return {
            'name' : 'VarDeclaration',
            'children' : [self.p1.printtree(), {'token': self.p2}, {'token': self.p3},{'token': self.p4},{'token': self.p5}, {'token': self.p6}, {'token': self.p7}, {'token': self.p8}]
        }

# class type_specifier:
#     def __init__(self, p):
#         self.p = p
#     def printtree(self):
#         return {'name' : 'Typespecifier', 'token' : str(self.p)}

class fun_declaration_2:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name' : 'FunctionContext', 'children' : [self.p.printtree()]}

class params_1:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name' : 'ParamListContext', 'children' : [self.p.printtree()]}

# class params_2:
#     def __init__(self, p):
#         self.p = p
#     def printtree(self):
#         return {'name' : 'ParamContext', 'token' : str(self.p)}

class param_1:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def printtree(self):
        return {'name' : 'ParamContext', 'children' : [self.p1.printtree(), {'token' : self.p2}]}

class param_2:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
    def printtree(self):
        return {'name' : 'ParamContext', 'children' : [self.p1.printtree(), {'token': self.p2}, {'token': self.p3}, {'token' : self.p4}]}

class statement_block_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name' : 'StatementblockContext', 'children' : [{'token': self.p1}, self.p2.printtree(), {'token' : self.p3}]}
    
class statement:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'StatementContext', 'children': [self.p.printtree()]}

class expression_2:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'ExpressionContext', 'children': [self.p.printtree()]}

class make_token:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'token' : self.p}

class numlist_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name': 'NumlistContext', 'children': [self.p1.printtree(), {'token' : self.p2}, {'token': self.p3}]}

class var_2:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def printtree(self):
        return {'name': 'VariableContext', 'children': [{'token' : self.p1}, {'token' : self.p2}, self.p3.printtree(), {'token' : self.p4}]}

class make_compute:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'ComputatonContext', 'children': [self.p.printtree()]}

class object_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name': 'ComputatonContext', 'children': [{'token' : self.p1}, self.p2.printtree(), {'token' : self.p3}]}

class fun_value_1:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def printtree(self):
        return {'name': 'FunctionContext', 'children': [{'token' : self.p1}, {'token' : self.p2}, self.p3.printtree(), {'token' : self.p4}]}

class args:
    def __init__(self, p):
        self.p = p
    def printtree(self):
        return {'name': 'ArgsContext', 'children': [self.p.printtree()]}

class arg_list_1:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def printtree(self):
        return {'name': 'ArgsContext', 'children': [self.p1.printtree(), {'token' : self.p2}, self.p3.printtree()]}
  
