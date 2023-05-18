
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BOOL CALL COMMA COMPARISON_OP ID LPAREN NEW NUM OPERATOR PROC RPAREN SEMICOLONprogram : variable_definitions procedure_definitionsvariable_definitions : variable_definitions variable_definition\n                            | variable_definitionvariable_definition : NEW ID SEMICOLON\n                           | NEW ID COMMA LPAREN type COMMA value RPAREN SEMICOLONtype : IDvalue : IDprocedure_definitions : procedure_definitions procedure_definition\n                            | procedure_definitionprocedure_definition : PROC ID LPAREN statements RPAREN SEMICOLONstatements : statements statement\n                  | statementstatement : ID\n                 | call_statementcall_statement : CALL LPAREN ID RPAREN SEMICOLON'
    
_lr_action_items = {'NEW':([0,2,3,6,12,34,],[4,4,-3,-2,-4,-5,]),'$end':([1,5,7,10,27,],[0,-1,-9,-8,-10,]),'PROC':([2,3,5,6,7,10,12,27,34,],[8,-3,8,-2,-9,-8,-4,-10,-5,]),'ID':([4,8,14,15,16,17,18,19,24,25,26,33,],[9,11,16,21,-13,16,-12,-14,-11,28,29,-15,]),'SEMICOLON':([9,23,31,32,],[12,27,33,34,]),'COMMA':([9,21,22,],[13,-6,26,]),'LPAREN':([11,13,20,],[14,15,25,]),'CALL':([14,16,17,18,19,24,33,],[20,-13,20,-12,-14,-11,-15,]),'RPAREN':([16,17,18,19,24,28,29,30,33,],[-13,23,-12,-14,-11,31,-7,32,-15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'variable_definitions':([0,],[2,]),'variable_definition':([0,2,],[3,6,]),'procedure_definitions':([2,],[5,]),'procedure_definition':([2,5,],[7,10,]),'statements':([14,],[17,]),'statement':([14,17,],[18,24,]),'call_statement':([14,17,],[19,19,]),'type':([15,],[22,]),'value':([26,],[30,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> variable_definitions procedure_definitions','program',2,'p_program','Yacc.py',25),
  ('variable_definitions -> variable_definitions variable_definition','variable_definitions',2,'p_variable_definitions','Yacc.py',29),
  ('variable_definitions -> variable_definition','variable_definitions',1,'p_variable_definitions','Yacc.py',30),
  ('variable_definition -> NEW ID SEMICOLON','variable_definition',3,'p_variable_definition','Yacc.py',34),
  ('variable_definition -> NEW ID COMMA LPAREN type COMMA value RPAREN SEMICOLON','variable_definition',9,'p_variable_definition','Yacc.py',35),
  ('type -> ID','type',1,'p_type','Yacc.py',47),
  ('value -> ID','value',1,'p_value','Yacc.py',51),
  ('procedure_definitions -> procedure_definitions procedure_definition','procedure_definitions',2,'p_procedure_definitions','Yacc.py',59),
  ('procedure_definitions -> procedure_definition','procedure_definitions',1,'p_procedure_definitions','Yacc.py',60),
  ('procedure_definition -> PROC ID LPAREN statements RPAREN SEMICOLON','procedure_definition',6,'p_procedure_definition','Yacc.py',64),
  ('statements -> statements statement','statements',2,'p_statements','Yacc.py',68),
  ('statements -> statement','statements',1,'p_statements','Yacc.py',69),
  ('statement -> ID','statement',1,'p_statement','Yacc.py',73),
  ('statement -> call_statement','statement',1,'p_statement','Yacc.py',74),
  ('call_statement -> CALL LPAREN ID RPAREN SEMICOLON','call_statement',5,'p_call_statement','Yacc.py',78),
]
