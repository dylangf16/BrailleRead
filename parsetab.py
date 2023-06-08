
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADDSUBleftMULDIVADD ALTER ALTERB ARROBA BOOL BREAK CALL CASE COMA COMMENT DIFFERENT DIV ELSE EQUAL ID INTEGER ISTRUE LPARENT MAQ MAQEQUAL MASTER MEQ MEQEQUAL MUL NEW PLUS PRINTVALUES PROC REPEAT RPARENT SEMICOLON SIGNAL STRING SUB THEN TYPE UNTIL VALUES VIEWSIGNAL WHEN WHILEstart : master\n            | master procedures\n            | master master_vars procedures\n            | master_vars master\n            | master_vars master master_vars\n            | master_vars master master_vars procedures\n            | master_vars master master_vars procedures master_vars\n            | master_vars master procedures\n            | master_vars master procedures master_vars declare_procedure : PROC IDprocedures : procedure\n                    | procedures procedureprocedure : declare_procedure LPARENT sentences RPARENT SEMICOLONmaster : MASTER LPARENT master_sentences RPARENT SEMICOLONmaster_sentences : master_sentence\n                        | master_sentences master_sentencemaster_sentence : master_var\n                       | values\n                       | case\n                       | call\n                       | print_values\n                       | alter\n                       | alterB\n                       | comparisson_maq\n                       | comparisson_meq\n                       | comparisson_equal\n                       | comparisson_dif\n                       | comparisson_meqequal\n                       | comparisson_maqequal\n                       | isTrue\n                       | signal\n                       | viewsignal\n                       | emptymaster_vars : master_var\n                    | master_vars master_varmaster_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON\n                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLONsentences : sentence\n                 | sentences sentencesentence : local_variable\n                | values\n                | case\n                | call\n                | print_values\n                | alter\n                | alterB\n                | comparisson_maq\n                | comparisson_meq\n                | comparisson_equal\n                | comparisson_dif\n                | comparisson_meqequal\n                | comparisson_maqequal\n                | isTrue\n                | signal\n                | viewsignal\n                | emptyreturn_statement : isTrue\n                        | comparisson_maqequal\n                        | comparisson_meqequal\n                        | comparisson_dif\n                        | comparisson_equal\n                        | comparisson_meq\n                        | comparisson_maq\n                        | alterB\n                        | alterlocal_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON\n                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLONvalues : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON\n                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON\n                 | VALUES LPARENT ID COMA return_statement RPARENT SEMICOLONcall : CALL LPARENT ID RPARENT SEMICOLONprint_values : PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLONprintable_sentences : printable_sentence_var\n                | printable_sentence_string\n                | printable_sentence_var COMA printable_sentence_var\n                | printable_sentence_string COMA printable_sentence_string\n                | printable_sentence_var COMA printable_sentence_string\n                | printable_sentence_string COMA printable_sentence_var\n                | printable_sentences COMA printable_sentence_var\n                | printable_sentences COMA printable_sentence_string\n                | COMA printable_sentences COMA printable_sentence_var\n                | COMA printable_sentences COMA printable_sentence_stringprintable_sentence_var : ID printable_sentence_string : STRING alter : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLONalterB : ALTERB LPARENT ID RPARENT SEMICOLONcomparisson_maq : ID MAQ INTEGERcomparisson_meq : ID MEQ INTEGERcomparisson_equal : ID EQUAL INTEGERcomparisson_dif : ID DIFFERENT INTEGERcomparisson_meqequal : ID MEQEQUAL INTEGERcomparisson_maqequal : ID MAQEQUAL INTEGERisTrue : ISTRUE LPARENT ID RPARENT SEMICOLONcase : CASE expression recursive_conditions SEMICOLONelse_condition : LPARENT sentences RPARENTrecursive_conditions : recursive_condition\n                            | recursive_conditions recursive_conditionrecursive_condition :  condition LPARENT sentences RPARENTexpression : IDcondition : WHEN INTEGER THEN signal : SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON\n            | SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLONviewsignal : VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLONempty :'
    
_lr_action_items = {'MASTER':([0,3,5,13,204,205,],[4,4,-34,-35,-36,-37,]),'NEW':([0,2,3,5,8,9,12,13,14,16,18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,75,94,96,97,98,99,100,101,102,103,123,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[6,6,6,-34,6,-11,6,-35,6,-12,71,6,6,6,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,71,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,6,6,-16,-39,6,-14,-90,-91,-92,-93,-94,-95,-13,-97,71,71,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'$end':([1,2,5,7,9,12,13,16,17,20,21,72,73,96,97,123,204,205,],[0,-1,-34,-2,-11,-4,-35,-12,-3,-5,-8,-6,-9,-7,-14,-13,-36,-37,]),'PROC':([2,5,7,8,9,12,13,16,17,20,21,72,97,123,204,205,],[11,-34,11,11,-11,11,-35,-12,11,11,11,11,-14,-13,-36,-37,]),'LPARENT':([4,10,19,42,44,45,46,47,48,49,50,51,107,124,158,],[14,18,-10,82,85,86,87,88,89,90,91,92,128,143,-103,]),'ID':([6,11,14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,43,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,75,82,85,86,87,88,89,90,94,98,99,100,101,102,103,113,125,126,128,132,133,134,157,159,160,167,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[15,19,41,41,41,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,84,41,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,95,-16,104,109,114,116,117,118,120,-39,-90,-91,-92,-93,-94,-95,114,144,-97,41,114,114,114,41,-71,-72,114,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'VALUES':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[42,42,42,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,42,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,42,42,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'CASE':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[43,43,43,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,43,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,43,43,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'CALL':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[44,44,44,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,44,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,44,44,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'PRINTVALUES':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[45,45,45,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,45,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,45,45,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'ALTER':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,125,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[46,46,46,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,46,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,46,-97,46,46,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'ALTERB':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,125,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[47,47,47,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,47,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,47,-97,47,47,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'ISTRUE':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,125,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[48,48,48,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,48,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,48,-97,48,48,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'SIGNAL':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[49,49,49,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,49,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,49,49,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'VIEWSIGNAL':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,126,128,157,159,160,172,173,176,195,196,197,202,203,204,205,214,215,216,217,218,219,],[50,50,50,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,50,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,-97,50,50,-71,-72,-89,-96,-106,-68,-69,-70,-104,-105,-36,-37,-85,-86,-87,-88,-66,-67,]),'RPARENT':([14,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,94,98,99,100,101,102,103,109,110,111,112,114,115,117,118,121,126,128,145,146,147,148,149,150,151,152,153,154,155,156,157,159,160,161,162,163,164,165,166,172,173,174,175,176,177,178,184,185,195,196,197,198,199,200,201,202,203,204,205,206,207,214,215,216,217,218,219,],[-107,-107,74,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,93,-38,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-16,-39,-90,-91,-92,-93,-94,-95,130,131,-73,-74,-83,-84,137,138,141,-97,-107,180,181,182,-57,-58,-59,-60,-61,-62,-63,-64,-65,183,-71,-72,-79,-80,-75,-77,-76,-78,-89,-96,190,191,-106,192,193,-81,-82,-68,-69,-70,208,209,210,211,-104,-105,-36,-37,212,213,-85,-86,-87,-88,-66,-67,]),'COMA':([15,86,95,104,110,111,112,113,114,115,116,119,120,122,135,161,162,163,164,165,166,168,169,170,171,179,184,185,],[51,113,124,125,132,133,134,113,-83,-84,136,139,140,142,167,-79,-80,-75,-77,-76,-78,186,187,188,189,194,-79,-80,]),'MAQ':([41,144,],[76,76,]),'MEQ':([41,144,],[77,77,]),'EQUAL':([41,144,],[78,78,]),'DIFFERENT':([41,144,],[79,79,]),'MEQEQUAL':([41,144,],[80,80,]),'MAQEQUAL':([41,144,],[81,81,]),'SEMICOLON':([74,93,105,106,127,130,131,137,138,141,180,181,182,183,190,191,192,193,208,209,210,211,212,213,],[97,123,126,-99,-100,159,160,172,173,176,195,196,197,-101,202,203,204,205,214,215,216,217,218,219,]),'INTEGER':([76,77,78,79,80,81,90,91,108,125,139,140,142,186,187,188,189,194,],[98,99,100,101,102,103,119,121,129,145,174,175,177,198,199,200,201,206,]),'WHEN':([83,84,105,106,127,183,],[108,-102,108,-99,-100,-101,]),'STRING':([86,113,132,133,134,167,],[115,115,115,115,115,115,]),'TYPE':([92,143,],[122,179,]),'BOOL':([125,142,194,],[146,178,207,]),'THEN':([129,],[158,]),'ADD':([136,],[168,]),'SUB':([136,],[169,]),'MUL':([136,],[170,]),'DIV':([136,],[171,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'master':([0,3,],[2,12,]),'master_vars':([0,2,12,21,72,],[3,8,20,73,96,]),'master_var':([0,2,3,8,12,14,20,21,22,72,73,96,],[5,5,13,13,5,24,13,5,24,5,13,13,]),'procedures':([2,8,12,20,],[7,17,21,72,]),'procedure':([2,7,8,12,17,20,21,72,],[9,16,9,9,16,9,16,16,]),'declare_procedure':([2,7,8,12,17,20,21,72,],[10,10,10,10,10,10,10,10,]),'master_sentences':([14,],[22,]),'master_sentence':([14,22,],[23,75,]),'values':([14,18,22,52,128,157,],[25,55,25,55,55,55,]),'case':([14,18,22,52,128,157,],[26,56,26,56,56,56,]),'call':([14,18,22,52,128,157,],[27,57,27,57,57,57,]),'print_values':([14,18,22,52,128,157,],[28,58,28,58,58,58,]),'alter':([14,18,22,52,125,128,157,],[29,59,29,59,156,59,59,]),'alterB':([14,18,22,52,125,128,157,],[30,60,30,60,155,60,60,]),'comparisson_maq':([14,18,22,52,125,128,157,],[31,61,31,61,154,61,61,]),'comparisson_meq':([14,18,22,52,125,128,157,],[32,62,32,62,153,62,62,]),'comparisson_equal':([14,18,22,52,125,128,157,],[33,63,33,63,152,63,63,]),'comparisson_dif':([14,18,22,52,125,128,157,],[34,64,34,64,151,64,64,]),'comparisson_meqequal':([14,18,22,52,125,128,157,],[35,65,35,65,150,65,65,]),'comparisson_maqequal':([14,18,22,52,125,128,157,],[36,66,36,66,149,66,66,]),'isTrue':([14,18,22,52,125,128,157,],[37,67,37,67,148,67,67,]),'signal':([14,18,22,52,128,157,],[38,68,38,68,68,68,]),'viewsignal':([14,18,22,52,128,157,],[39,69,39,69,69,69,]),'empty':([14,18,22,52,128,157,],[40,70,40,70,70,70,]),'sentences':([18,128,],[52,157,]),'sentence':([18,52,128,157,],[53,94,53,94,]),'local_variable':([18,52,128,157,],[54,54,54,54,]),'expression':([43,],[83,]),'recursive_conditions':([83,],[105,]),'recursive_condition':([83,105,],[106,127,]),'condition':([83,105,],[107,107,]),'printable_sentences':([86,113,],[110,135,]),'printable_sentence_var':([86,113,132,133,134,167,],[111,111,161,163,166,184,]),'printable_sentence_string':([86,113,132,133,134,167,],[112,112,162,164,165,185,]),'return_statement':([125,],[147,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> master','start',1,'p_start','Yacc.py',148),
  ('start -> master procedures','start',2,'p_start','Yacc.py',149),
  ('start -> master master_vars procedures','start',3,'p_start','Yacc.py',150),
  ('start -> master_vars master','start',2,'p_start','Yacc.py',151),
  ('start -> master_vars master master_vars','start',3,'p_start','Yacc.py',152),
  ('start -> master_vars master master_vars procedures','start',4,'p_start','Yacc.py',153),
  ('start -> master_vars master master_vars procedures master_vars','start',5,'p_start','Yacc.py',154),
  ('start -> master_vars master procedures','start',3,'p_start','Yacc.py',155),
  ('start -> master_vars master procedures master_vars','start',4,'p_start','Yacc.py',156),
  ('declare_procedure -> PROC ID','declare_procedure',2,'p_declare_procedure','Yacc.py',161),
  ('procedures -> procedure','procedures',1,'p_procedures','Yacc.py',172),
  ('procedures -> procedures procedure','procedures',2,'p_procedures','Yacc.py',173),
  ('procedure -> declare_procedure LPARENT sentences RPARENT SEMICOLON','procedure',5,'p_procedure','Yacc.py',177),
  ('master -> MASTER LPARENT master_sentences RPARENT SEMICOLON','master',5,'p_master','Yacc.py',187),
  ('master_sentences -> master_sentence','master_sentences',1,'p_master_sentences','Yacc.py',199),
  ('master_sentences -> master_sentences master_sentence','master_sentences',2,'p_master_sentences','Yacc.py',200),
  ('master_sentence -> master_var','master_sentence',1,'p_master_sentence','Yacc.py',208),
  ('master_sentence -> values','master_sentence',1,'p_master_sentence','Yacc.py',209),
  ('master_sentence -> case','master_sentence',1,'p_master_sentence','Yacc.py',210),
  ('master_sentence -> call','master_sentence',1,'p_master_sentence','Yacc.py',211),
  ('master_sentence -> print_values','master_sentence',1,'p_master_sentence','Yacc.py',212),
  ('master_sentence -> alter','master_sentence',1,'p_master_sentence','Yacc.py',213),
  ('master_sentence -> alterB','master_sentence',1,'p_master_sentence','Yacc.py',214),
  ('master_sentence -> comparisson_maq','master_sentence',1,'p_master_sentence','Yacc.py',215),
  ('master_sentence -> comparisson_meq','master_sentence',1,'p_master_sentence','Yacc.py',216),
  ('master_sentence -> comparisson_equal','master_sentence',1,'p_master_sentence','Yacc.py',217),
  ('master_sentence -> comparisson_dif','master_sentence',1,'p_master_sentence','Yacc.py',218),
  ('master_sentence -> comparisson_meqequal','master_sentence',1,'p_master_sentence','Yacc.py',219),
  ('master_sentence -> comparisson_maqequal','master_sentence',1,'p_master_sentence','Yacc.py',220),
  ('master_sentence -> isTrue','master_sentence',1,'p_master_sentence','Yacc.py',221),
  ('master_sentence -> signal','master_sentence',1,'p_master_sentence','Yacc.py',222),
  ('master_sentence -> viewsignal','master_sentence',1,'p_master_sentence','Yacc.py',223),
  ('master_sentence -> empty','master_sentence',1,'p_master_sentence','Yacc.py',224),
  ('master_vars -> master_var','master_vars',1,'p_master_vars','Yacc.py',229),
  ('master_vars -> master_vars master_var','master_vars',2,'p_master_vars','Yacc.py',230),
  ('master_var -> NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON','master_var',9,'p_master_var','Yacc.py',234),
  ('master_var -> NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON','master_var',9,'p_master_var','Yacc.py',235),
  ('sentences -> sentence','sentences',1,'p_sentences','Yacc.py',252),
  ('sentences -> sentences sentence','sentences',2,'p_sentences','Yacc.py',253),
  ('sentence -> local_variable','sentence',1,'p_sentence','Yacc.py',259),
  ('sentence -> values','sentence',1,'p_sentence','Yacc.py',260),
  ('sentence -> case','sentence',1,'p_sentence','Yacc.py',261),
  ('sentence -> call','sentence',1,'p_sentence','Yacc.py',262),
  ('sentence -> print_values','sentence',1,'p_sentence','Yacc.py',263),
  ('sentence -> alter','sentence',1,'p_sentence','Yacc.py',264),
  ('sentence -> alterB','sentence',1,'p_sentence','Yacc.py',265),
  ('sentence -> comparisson_maq','sentence',1,'p_sentence','Yacc.py',266),
  ('sentence -> comparisson_meq','sentence',1,'p_sentence','Yacc.py',267),
  ('sentence -> comparisson_equal','sentence',1,'p_sentence','Yacc.py',268),
  ('sentence -> comparisson_dif','sentence',1,'p_sentence','Yacc.py',269),
  ('sentence -> comparisson_meqequal','sentence',1,'p_sentence','Yacc.py',270),
  ('sentence -> comparisson_maqequal','sentence',1,'p_sentence','Yacc.py',271),
  ('sentence -> isTrue','sentence',1,'p_sentence','Yacc.py',272),
  ('sentence -> signal','sentence',1,'p_sentence','Yacc.py',273),
  ('sentence -> viewsignal','sentence',1,'p_sentence','Yacc.py',274),
  ('sentence -> empty','sentence',1,'p_sentence','Yacc.py',275),
  ('return_statement -> isTrue','return_statement',1,'p_return_statement','Yacc.py',280),
  ('return_statement -> comparisson_maqequal','return_statement',1,'p_return_statement','Yacc.py',281),
  ('return_statement -> comparisson_meqequal','return_statement',1,'p_return_statement','Yacc.py',282),
  ('return_statement -> comparisson_dif','return_statement',1,'p_return_statement','Yacc.py',283),
  ('return_statement -> comparisson_equal','return_statement',1,'p_return_statement','Yacc.py',284),
  ('return_statement -> comparisson_meq','return_statement',1,'p_return_statement','Yacc.py',285),
  ('return_statement -> comparisson_maq','return_statement',1,'p_return_statement','Yacc.py',286),
  ('return_statement -> alterB','return_statement',1,'p_return_statement','Yacc.py',287),
  ('return_statement -> alter','return_statement',1,'p_return_statement','Yacc.py',288),
  ('local_variable -> NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON','local_variable',9,'p_local_variable','Yacc.py',293),
  ('local_variable -> NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON','local_variable',9,'p_local_variable','Yacc.py',294),
  ('values -> VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON','values',7,'p_values','Yacc.py',311),
  ('values -> VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON','values',7,'p_values','Yacc.py',312),
  ('values -> VALUES LPARENT ID COMA return_statement RPARENT SEMICOLON','values',7,'p_values','Yacc.py',313),
  ('call -> CALL LPARENT ID RPARENT SEMICOLON','call',5,'p_call','Yacc.py',340),
  ('print_values -> PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLON','print_values',5,'p_print_values','Yacc.py',361),
  ('printable_sentences -> printable_sentence_var','printable_sentences',1,'p_printable_sentences','Yacc.py',367),
  ('printable_sentences -> printable_sentence_string','printable_sentences',1,'p_printable_sentences','Yacc.py',368),
  ('printable_sentences -> printable_sentence_var COMA printable_sentence_var','printable_sentences',3,'p_printable_sentences','Yacc.py',369),
  ('printable_sentences -> printable_sentence_string COMA printable_sentence_string','printable_sentences',3,'p_printable_sentences','Yacc.py',370),
  ('printable_sentences -> printable_sentence_var COMA printable_sentence_string','printable_sentences',3,'p_printable_sentences','Yacc.py',371),
  ('printable_sentences -> printable_sentence_string COMA printable_sentence_var','printable_sentences',3,'p_printable_sentences','Yacc.py',372),
  ('printable_sentences -> printable_sentences COMA printable_sentence_var','printable_sentences',3,'p_printable_sentences','Yacc.py',373),
  ('printable_sentences -> printable_sentences COMA printable_sentence_string','printable_sentences',3,'p_printable_sentences','Yacc.py',374),
  ('printable_sentences -> COMA printable_sentences COMA printable_sentence_var','printable_sentences',4,'p_printable_sentences','Yacc.py',375),
  ('printable_sentences -> COMA printable_sentences COMA printable_sentence_string','printable_sentences',4,'p_printable_sentences','Yacc.py',376),
  ('printable_sentence_var -> ID','printable_sentence_var',1,'p_printable_sentence_var','Yacc.py',380),
  ('printable_sentence_string -> STRING','printable_sentence_string',1,'p_printable_sentence_string','Yacc.py',391),
  ('alter -> ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',398),
  ('alter -> ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',399),
  ('alter -> ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',400),
  ('alter -> ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',401),
  ('alterB -> ALTERB LPARENT ID RPARENT SEMICOLON','alterB',5,'p_alterB','Yacc.py',514),
  ('comparisson_maq -> ID MAQ INTEGER','comparisson_maq',3,'p_comparisson_maq','Yacc.py',558),
  ('comparisson_meq -> ID MEQ INTEGER','comparisson_meq',3,'p_comparisson_meq','Yacc.py',595),
  ('comparisson_equal -> ID EQUAL INTEGER','comparisson_equal',3,'p_comparisson_equal','Yacc.py',632),
  ('comparisson_dif -> ID DIFFERENT INTEGER','comparisson_dif',3,'p_comparisson_dif','Yacc.py',669),
  ('comparisson_meqequal -> ID MEQEQUAL INTEGER','comparisson_meqequal',3,'p_comparisson_meqequal','Yacc.py',706),
  ('comparisson_maqequal -> ID MAQEQUAL INTEGER','comparisson_maqequal',3,'p_comparisson_maqequal','Yacc.py',743),
  ('isTrue -> ISTRUE LPARENT ID RPARENT SEMICOLON','isTrue',5,'p_isTrue','Yacc.py',780),
  ('case -> CASE expression recursive_conditions SEMICOLON','case',4,'p_case','Yacc.py',813),
  ('else_condition -> LPARENT sentences RPARENT','else_condition',3,'p_else_condition','Yacc.py',818),
  ('recursive_conditions -> recursive_condition','recursive_conditions',1,'p_recursive_conditions','Yacc.py',828),
  ('recursive_conditions -> recursive_conditions recursive_condition','recursive_conditions',2,'p_recursive_conditions','Yacc.py',829),
  ('recursive_condition -> condition LPARENT sentences RPARENT','recursive_condition',4,'p_recursive_condition','Yacc.py',834),
  ('expression -> ID','expression',1,'p_expression','Yacc.py',839),
  ('condition -> WHEN INTEGER THEN','condition',3,'p_condition','Yacc.py',847),
  ('signal -> SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON','signal',7,'p_signal','Yacc.py',864),
  ('signal -> SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLON','signal',7,'p_signal','Yacc.py',865),
  ('viewsignal -> VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLON','viewsignal',5,'p_viewsignal','Yacc.py',898),
  ('empty -> <empty>','empty',0,'p_empty','Yacc.py',904),
]
