
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADDSUBleftMULDIVADD ALTER ALTERB ARROBA BOOL BREAK CALL CASE COMA COMMENT DIFFERENT DIV ELSE EQUAL ID INTEGER ISTRUE LPARENT MAQ MAQEQUAL MASTER MEQ MEQEQUAL MUL NEW NEWLINE PLUS PRINTVALUES PROC REPEAT RPARENT SEMICOLON SIGNAL STRING SUB THEN TYPE UNTIL VALUES VIEWSIGNAL WHEN WHILEstart : master procedures\n            | masterdeclare_procedure : PROC IDprocedures : procedure\n                    | procedures procedureprocedure : declare_procedure LPARENT sentences RPARENT SEMICOLONmaster : MASTER LPARENT master_sentences RPARENT SEMICOLONmaster_sentences : master_sentence\n                        | master_sentences master_sentencemaster_sentence : master_var\n                       | values\n                       | case\n                       | call\n                       | print_values\n                       | alter\n                       | alterB\n                       | signal\n                       | viewsignal\n                       | sentence7\n                       | sentence8\n                       | sentence9\n                       | sentence10\n                       | sentence11\n                       | sentence12\n                       | isTrue\n                       | sentence14\n                       | sentence15\n                       | emptymaster_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON\n                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLONsentences : sentence\n                 | sentences sentencesentence : local_variable\n                | values\n                | case\n                | call\n                | print_values\n                | alter\n                | alterB\n                | signal\n                | viewsignal\n                | sentence7\n                | sentence8\n                | sentence9\n                | sentence10\n                | sentence11\n                | sentence12\n                | isTrue\n                | sentence14\n                | sentence15\n                | emptylocal_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON\n                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLONvalues : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON\n                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLONcall : CALL LPARENT ID RPARENT SEMICOLONprint_values : PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLONprintable_sentences : printable_sentence_var\n                | printable_sentence_string\n                | printable_sentence_var PLUS printable_sentence_var\n                | printable_sentence_string PLUS printable_sentence_string\n                | printable_sentence_var PLUS printable_sentence_string\n                | printable_sentence_string PLUS printable_sentence_var\n                | PLUS printable_sentences PLUS printable_sentence_var\n                | PLUS printable_sentences PLUS printable_sentence_stringprintable_sentence_var : ID printable_sentence_string : STRING alter : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON\n                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLONalterB : ALTERB LPARENT ID RPARENT SEMICOLONsentence7 : ID MAQ INTEGERsentence8 : ID MEQ INTEGERsentence9 : ID EQUAL INTEGERsentence10 : ID DIFFERENT INTEGERsentence11 : ID MEQEQUAL INTEGERsentence12 : ID MAQEQUAL INTEGERisTrue : ISTRUE LPARENT ID RPARENT SEMICOLONsentence14 : REPEAT LPARENT sentences BREAK RPARENT SEMICOLONsentence15 : UNTIL LPARENT instructions RPARENT sentences SEMICOLONinstructions : sentenceinstructions : sentence sentencescase : CASE expression recursive_conditions SEMICOLONelse_condition : LPARENT sentences RPARENTrecursive_conditions : recursive_condition\n                            | recursive_conditions recursive_conditionrecursive_condition :  condition LPARENT sentences RPARENTexpression : IDcondition : WHEN INTEGER THEN signal : SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON\n            | SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLONviewsignal : VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLONempty :'
    
_lr_action_items = {'MASTER':([0,],[3,]),'$end':([1,2,4,5,9,92,121,],[0,-2,-1,-4,-5,-7,-6,]),'PROC':([2,4,5,9,92,121,],[7,7,-4,-5,-7,-6,]),'LPARENT':([3,6,11,35,37,38,39,40,41,42,43,44,45,93,103,122,148,],[8,10,-3,77,80,81,82,83,84,85,86,87,88,123,127,143,-90,]),'ID':([7,8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,36,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,77,80,81,82,83,84,86,87,88,90,94,95,96,97,98,99,109,118,120,125,127,131,132,141,142,147,149,150,155,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[11,34,34,34,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,70,79,34,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,91,-9,100,105,110,112,113,115,117,34,34,-32,-73,-74,-75,-76,-77,-78,110,34,34,-84,34,110,110,34,34,34,-56,-57,110,-72,-93,-79,34,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'NEW':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[33,67,33,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,67,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,67,67,-32,-73,-74,-75,-76,-77,-78,67,67,-84,67,67,67,67,-56,-57,-72,-93,-79,67,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'VALUES':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[35,35,35,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,35,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,35,35,-32,-73,-74,-75,-76,-77,-78,35,35,-84,35,35,35,35,-56,-57,-72,-93,-79,35,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'CASE':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[36,36,36,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,36,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,36,36,-32,-73,-74,-75,-76,-77,-78,36,36,-84,36,36,36,36,-56,-57,-72,-93,-79,36,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'CALL':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[37,37,37,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,37,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,37,37,-32,-73,-74,-75,-76,-77,-78,37,37,-84,37,37,37,37,-56,-57,-72,-93,-79,37,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'PRINTVALUES':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[38,38,38,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,38,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,38,38,-32,-73,-74,-75,-76,-77,-78,38,38,-84,38,38,38,38,-56,-57,-72,-93,-79,38,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'ALTER':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[39,39,39,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,39,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,39,39,-32,-73,-74,-75,-76,-77,-78,39,39,-84,39,39,39,39,-56,-57,-72,-93,-79,39,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'ALTERB':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[40,40,40,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,40,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,40,40,-32,-73,-74,-75,-76,-77,-78,40,40,-84,40,40,40,40,-56,-57,-72,-93,-79,40,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'SIGNAL':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[41,41,41,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,41,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,41,41,-32,-73,-74,-75,-76,-77,-78,41,41,-84,41,41,41,41,-56,-57,-72,-93,-79,41,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'VIEWSIGNAL':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[42,42,42,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,42,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,42,42,-32,-73,-74,-75,-76,-77,-78,42,42,-84,42,42,42,42,-56,-57,-72,-93,-79,42,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'ISTRUE':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[43,43,43,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,43,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,43,43,-32,-73,-74,-75,-76,-77,-78,43,43,-84,43,43,43,43,-56,-57,-72,-93,-79,43,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'REPEAT':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[44,44,44,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,44,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,44,44,-32,-73,-74,-75,-76,-77,-78,44,44,-84,44,44,44,44,-56,-57,-72,-93,-79,44,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'UNTIL':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,87,88,90,94,95,96,97,98,99,118,120,125,127,141,142,147,149,150,160,163,164,166,180,181,185,186,191,192,203,204,205,206,207,208,209,210,],[45,45,45,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,45,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,45,45,-32,-73,-74,-75,-76,-77,-78,45,45,-84,45,45,45,45,-56,-57,-72,-93,-79,45,-80,-81,-54,-55,-91,-92,-29,-30,-68,-69,-70,-71,-52,-53,]),'RPARENT':([8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,69,88,90,94,95,96,97,98,99,105,106,107,108,110,111,113,116,117,119,120,125,127,140,142,145,146,147,149,150,151,152,153,154,160,161,162,163,164,172,173,180,181,183,184,185,186,187,188,189,190,191,192,193,194,203,204,205,206,207,208,209,210,],[-94,-94,68,-8,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,89,-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-9,-94,-32,-73,-74,-75,-76,-77,-78,129,130,-58,-59,-66,-67,135,138,139,141,-82,-84,-94,165,-83,169,170,171,-56,-57,-60,-62,-61,-63,-72,178,179,-93,-79,-64,-65,-80,-81,195,196,-54,-55,197,198,199,200,-91,-92,201,202,-29,-30,-68,-69,-70,-71,-52,-53,]),'MAQ':([34,],[71,]),'MEQ':([34,],[72,]),'EQUAL':([34,],[73,]),'DIFFERENT':([34,],[74,]),'MEQEQUAL':([34,],[75,]),'MAQEQUAL':([34,],[76,]),'BREAK':([47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,87,90,94,95,96,97,98,99,118,125,149,150,160,163,164,180,181,185,186,191,192,205,206,207,208,209,210,],[-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-94,-32,-73,-74,-75,-76,-77,-78,140,-84,-56,-57,-72,-93,-79,-80,-81,-54,-55,-91,-92,-68,-69,-70,-71,-52,-53,]),'SEMICOLON':([47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,68,89,90,94,95,96,97,98,99,101,102,125,126,129,130,135,138,139,141,149,150,160,163,164,165,166,169,170,171,178,179,180,181,185,186,191,192,195,196,197,198,199,200,201,202,205,206,207,208,209,210,],[-31,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,92,121,-32,-73,-74,-75,-76,-77,-78,125,-86,-84,-87,149,150,160,163,164,-94,-56,-57,-72,-93,-79,180,181,185,186,-88,191,192,-80,-81,-54,-55,-91,-92,203,204,205,206,207,208,209,210,-68,-69,-70,-71,-52,-53,]),'COMA':([70,91,100,112,114,115,144,156,157,158,159,167,],[93,122,124,134,136,137,168,174,175,176,177,182,]),'INTEGER':([71,72,73,74,75,76,84,85,104,124,136,137,168,174,175,176,177,182,],[94,95,96,97,98,99,114,116,128,145,161,162,183,187,188,189,190,193,]),'WHEN':([78,79,101,102,126,171,],[104,-89,104,-86,-87,-88,]),'PLUS':([81,107,108,109,110,111,133,151,152,153,154,172,173,],[109,131,132,109,-66,-67,155,-60,-62,-61,-63,-64,-65,]),'STRING':([81,109,131,132,155,],[111,111,111,111,111,]),'TYPE':([123,143,],[144,167,]),'BOOL':([124,168,182,],[146,184,194,]),'THEN':([128,],[148,]),'ADD':([134,],[156,]),'SUB':([134,],[157,]),'MUL':([134,],[158,]),'DIV':([134,],[159,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'master':([0,],[2,]),'procedures':([2,],[4,]),'procedure':([2,4,],[5,9,]),'declare_procedure':([2,4,],[6,6,]),'master_sentences':([8,],[12,]),'master_sentence':([8,12,],[13,69,]),'master_var':([8,12,],[14,14,]),'values':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[15,49,15,49,49,49,49,49,49,49,49,49,49,]),'case':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[16,50,16,50,50,50,50,50,50,50,50,50,50,]),'call':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[17,51,17,51,51,51,51,51,51,51,51,51,51,]),'print_values':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[18,52,18,52,52,52,52,52,52,52,52,52,52,]),'alter':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[19,53,19,53,53,53,53,53,53,53,53,53,53,]),'alterB':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[20,54,20,54,54,54,54,54,54,54,54,54,54,]),'signal':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[21,55,21,55,55,55,55,55,55,55,55,55,55,]),'viewsignal':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[22,56,22,56,56,56,56,56,56,56,56,56,56,]),'sentence7':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[23,57,23,57,57,57,57,57,57,57,57,57,57,]),'sentence8':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[24,58,24,58,58,58,58,58,58,58,58,58,58,]),'sentence9':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[25,59,25,59,59,59,59,59,59,59,59,59,59,]),'sentence10':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[26,60,26,60,60,60,60,60,60,60,60,60,60,]),'sentence11':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[27,61,27,61,61,61,61,61,61,61,61,61,61,]),'sentence12':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[28,62,28,62,62,62,62,62,62,62,62,62,62,]),'isTrue':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[29,63,29,63,63,63,63,63,63,63,63,63,63,]),'sentence14':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[30,64,30,64,64,64,64,64,64,64,64,64,64,]),'sentence15':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[31,65,31,65,65,65,65,65,65,65,65,65,65,]),'empty':([8,10,12,46,87,88,118,120,127,141,142,147,166,],[32,66,32,66,66,66,66,66,66,66,66,66,66,]),'sentences':([10,87,120,127,141,],[46,118,142,147,166,]),'sentence':([10,46,87,88,118,120,127,141,142,147,166,],[47,90,47,120,90,47,47,47,90,90,90,]),'local_variable':([10,46,87,88,118,120,127,141,142,147,166,],[48,48,48,48,48,48,48,48,48,48,48,]),'expression':([36,],[78,]),'recursive_conditions':([78,],[101,]),'recursive_condition':([78,101,],[102,126,]),'condition':([78,101,],[103,103,]),'printable_sentences':([81,109,],[106,133,]),'printable_sentence_var':([81,109,131,132,155,],[107,107,151,154,172,]),'printable_sentence_string':([81,109,131,132,155,],[108,108,152,153,173,]),'instructions':([88,],[119,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> master procedures','start',2,'p_start','Yacc.py',150),
  ('start -> master','start',1,'p_start','Yacc.py',151),
  ('declare_procedure -> PROC ID','declare_procedure',2,'p_declare_procedure','Yacc.py',156),
  ('procedures -> procedure','procedures',1,'p_procedures','Yacc.py',167),
  ('procedures -> procedures procedure','procedures',2,'p_procedures','Yacc.py',168),
  ('procedure -> declare_procedure LPARENT sentences RPARENT SEMICOLON','procedure',5,'p_procedure','Yacc.py',172),
  ('master -> MASTER LPARENT master_sentences RPARENT SEMICOLON','master',5,'p_master','Yacc.py',182),
  ('master_sentences -> master_sentence','master_sentences',1,'p_master_sentences','Yacc.py',194),
  ('master_sentences -> master_sentences master_sentence','master_sentences',2,'p_master_sentences','Yacc.py',195),
  ('master_sentence -> master_var','master_sentence',1,'p_master_sentence','Yacc.py',203),
  ('master_sentence -> values','master_sentence',1,'p_master_sentence','Yacc.py',204),
  ('master_sentence -> case','master_sentence',1,'p_master_sentence','Yacc.py',205),
  ('master_sentence -> call','master_sentence',1,'p_master_sentence','Yacc.py',206),
  ('master_sentence -> print_values','master_sentence',1,'p_master_sentence','Yacc.py',207),
  ('master_sentence -> alter','master_sentence',1,'p_master_sentence','Yacc.py',208),
  ('master_sentence -> alterB','master_sentence',1,'p_master_sentence','Yacc.py',209),
  ('master_sentence -> signal','master_sentence',1,'p_master_sentence','Yacc.py',210),
  ('master_sentence -> viewsignal','master_sentence',1,'p_master_sentence','Yacc.py',211),
  ('master_sentence -> sentence7','master_sentence',1,'p_master_sentence','Yacc.py',212),
  ('master_sentence -> sentence8','master_sentence',1,'p_master_sentence','Yacc.py',213),
  ('master_sentence -> sentence9','master_sentence',1,'p_master_sentence','Yacc.py',214),
  ('master_sentence -> sentence10','master_sentence',1,'p_master_sentence','Yacc.py',215),
  ('master_sentence -> sentence11','master_sentence',1,'p_master_sentence','Yacc.py',216),
  ('master_sentence -> sentence12','master_sentence',1,'p_master_sentence','Yacc.py',217),
  ('master_sentence -> isTrue','master_sentence',1,'p_master_sentence','Yacc.py',218),
  ('master_sentence -> sentence14','master_sentence',1,'p_master_sentence','Yacc.py',219),
  ('master_sentence -> sentence15','master_sentence',1,'p_master_sentence','Yacc.py',220),
  ('master_sentence -> empty','master_sentence',1,'p_master_sentence','Yacc.py',221),
  ('master_var -> NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON','master_var',9,'p_master_var','Yacc.py',226),
  ('master_var -> NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON','master_var',9,'p_master_var','Yacc.py',227),
  ('sentences -> sentence','sentences',1,'p_sentences','Yacc.py',245),
  ('sentences -> sentences sentence','sentences',2,'p_sentences','Yacc.py',246),
  ('sentence -> local_variable','sentence',1,'p_sentence','Yacc.py',252),
  ('sentence -> values','sentence',1,'p_sentence','Yacc.py',253),
  ('sentence -> case','sentence',1,'p_sentence','Yacc.py',254),
  ('sentence -> call','sentence',1,'p_sentence','Yacc.py',255),
  ('sentence -> print_values','sentence',1,'p_sentence','Yacc.py',256),
  ('sentence -> alter','sentence',1,'p_sentence','Yacc.py',257),
  ('sentence -> alterB','sentence',1,'p_sentence','Yacc.py',258),
  ('sentence -> signal','sentence',1,'p_sentence','Yacc.py',259),
  ('sentence -> viewsignal','sentence',1,'p_sentence','Yacc.py',260),
  ('sentence -> sentence7','sentence',1,'p_sentence','Yacc.py',261),
  ('sentence -> sentence8','sentence',1,'p_sentence','Yacc.py',262),
  ('sentence -> sentence9','sentence',1,'p_sentence','Yacc.py',263),
  ('sentence -> sentence10','sentence',1,'p_sentence','Yacc.py',264),
  ('sentence -> sentence11','sentence',1,'p_sentence','Yacc.py',265),
  ('sentence -> sentence12','sentence',1,'p_sentence','Yacc.py',266),
  ('sentence -> isTrue','sentence',1,'p_sentence','Yacc.py',267),
  ('sentence -> sentence14','sentence',1,'p_sentence','Yacc.py',268),
  ('sentence -> sentence15','sentence',1,'p_sentence','Yacc.py',269),
  ('sentence -> empty','sentence',1,'p_sentence','Yacc.py',270),
  ('local_variable -> NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON','local_variable',9,'p_local_variable','Yacc.py',276),
  ('local_variable -> NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON','local_variable',9,'p_local_variable','Yacc.py',277),
  ('values -> VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON','values',7,'p_values','Yacc.py',294),
  ('values -> VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON','values',7,'p_values','Yacc.py',295),
  ('call -> CALL LPARENT ID RPARENT SEMICOLON','call',5,'p_call','Yacc.py',318),
  ('print_values -> PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLON','print_values',5,'p_print_values','Yacc.py',338),
  ('printable_sentences -> printable_sentence_var','printable_sentences',1,'p_printable_sentences','Yacc.py',344),
  ('printable_sentences -> printable_sentence_string','printable_sentences',1,'p_printable_sentences','Yacc.py',345),
  ('printable_sentences -> printable_sentence_var PLUS printable_sentence_var','printable_sentences',3,'p_printable_sentences','Yacc.py',346),
  ('printable_sentences -> printable_sentence_string PLUS printable_sentence_string','printable_sentences',3,'p_printable_sentences','Yacc.py',347),
  ('printable_sentences -> printable_sentence_var PLUS printable_sentence_string','printable_sentences',3,'p_printable_sentences','Yacc.py',348),
  ('printable_sentences -> printable_sentence_string PLUS printable_sentence_var','printable_sentences',3,'p_printable_sentences','Yacc.py',349),
  ('printable_sentences -> PLUS printable_sentences PLUS printable_sentence_var','printable_sentences',4,'p_printable_sentences','Yacc.py',350),
  ('printable_sentences -> PLUS printable_sentences PLUS printable_sentence_string','printable_sentences',4,'p_printable_sentences','Yacc.py',351),
  ('printable_sentence_var -> ID','printable_sentence_var',1,'p_printable_sentence_var','Yacc.py',355),
  ('printable_sentence_string -> STRING','printable_sentence_string',1,'p_printable_sentence_string','Yacc.py',366),
  ('alter -> ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',373),
  ('alter -> ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',374),
  ('alter -> ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',375),
  ('alter -> ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON','alter',9,'p_alter','Yacc.py',376),
  ('alterB -> ALTERB LPARENT ID RPARENT SEMICOLON','alterB',5,'p_alterB','Yacc.py',471),
  ('sentence7 -> ID MAQ INTEGER','sentence7',3,'p_sentence7','Yacc.py',503),
  ('sentence8 -> ID MEQ INTEGER','sentence8',3,'p_sentence8','Yacc.py',530),
  ('sentence9 -> ID EQUAL INTEGER','sentence9',3,'p_sentence9','Yacc.py',557),
  ('sentence10 -> ID DIFFERENT INTEGER','sentence10',3,'p_sentence10','Yacc.py',584),
  ('sentence11 -> ID MEQEQUAL INTEGER','sentence11',3,'p_sentence11','Yacc.py',611),
  ('sentence12 -> ID MAQEQUAL INTEGER','sentence12',3,'p_sentence12','Yacc.py',638),
  ('isTrue -> ISTRUE LPARENT ID RPARENT SEMICOLON','isTrue',5,'p_isTrue','Yacc.py',665),
  ('sentence14 -> REPEAT LPARENT sentences BREAK RPARENT SEMICOLON','sentence14',6,'p_sentence14','Yacc.py',697),
  ('sentence15 -> UNTIL LPARENT instructions RPARENT sentences SEMICOLON','sentence15',6,'p_sentence15','Yacc.py',701),
  ('instructions -> sentence','instructions',1,'p_instructions','Yacc.py',707),
  ('instructions -> sentence sentences','instructions',2,'p_instructions_recursive','Yacc.py',712),
  ('case -> CASE expression recursive_conditions SEMICOLON','case',4,'p_case','Yacc.py',717),
  ('else_condition -> LPARENT sentences RPARENT','else_condition',3,'p_else_condition','Yacc.py',722),
  ('recursive_conditions -> recursive_condition','recursive_conditions',1,'p_recursive_conditions','Yacc.py',732),
  ('recursive_conditions -> recursive_conditions recursive_condition','recursive_conditions',2,'p_recursive_conditions','Yacc.py',733),
  ('recursive_condition -> condition LPARENT sentences RPARENT','recursive_condition',4,'p_recursive_condition','Yacc.py',738),
  ('expression -> ID','expression',1,'p_expression','Yacc.py',744),
  ('condition -> WHEN INTEGER THEN','condition',3,'p_condition','Yacc.py',751),
  ('signal -> SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON','signal',7,'p_signal','Yacc.py',768),
  ('signal -> SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLON','signal',7,'p_signal','Yacc.py',769),
  ('viewsignal -> VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLON','viewsignal',5,'p_viewsignal','Yacc.py',801),
  ('empty -> <empty>','empty',0,'p_empty','Yacc.py',807),
]
