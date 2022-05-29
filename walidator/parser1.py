
from pickle import TRUE


class Parser:

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()
    self.prev_line = 0
    self.empty_line = 0
    self.assign_num = 0
    self.con_num = 0
    self.ID_array = []
    self.recent_ID = ""
    self.con_blockade = 0

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error("Unexpected token: %s" % token_type)

    if token_type != 'EOF':
      self.token = self.next_token() 

  def error(self,msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  # Starting symbol
  def start(self):
    # begin -> end -> program EOF
    if self.token.type == 'begin': #check if string starts with 'begin'
      self.take_token('begin')
      self.program()
      self.take_token('end')

    else:
      self.error("'begin' must appear as a beginning")
   
  def program(self):
    # program -> statement program
    if self.token.type == 'ID' or self.token.type == 'gnd':
      self.prev_line = self.token.line
      self.statement()

      if (self.token.line - self.prev_line) >= 2:
        self.empty_line = 1 #empty line detected
      self.program()
    # program -> eps
    else:
      pass

  def statement(self):
    # statement 
    if self.token.type == 'ID':
      self.ID_array.append(self.token.value)#add electric element(ID) to the list
      self.recent_ID = self.token.value
      self.take_token("ID")

      if self.token.type == 'ASSIGN': #statement-> assign statment
        self.assign_stmt()
        self.empty_line = 0
        pass

      else: # statement -> connection statement
        self.ID_array.pop()#delete last electric element(ID) from the list because it wasn't a decleration

        if self.ID_array.count(self.recent_ID) == 1:
          self.con_stmt()

        else:
          self.error("electric element was not declared")
    # statement -> connection statement
    elif self.token.type == 'gnd':# statement -> connection statement when it starts with 'gnd'
      self.con_stmt()
      pass

    else:
      self.error("Epsilon not allowed")

# assign_stmt -> ID ASSIGN value END
  def assign_stmt(self):

    if self.con_blockade == 1:
      self.error("Connection appeard before assignment")

    if self.token.type == 'ASSIGN':
      self.take_token('ASSIGN')   

      if self.token.type == 'voltagesource' or self.token.type == 'currentsource':
        self.take_token(self.token.type)
        self.take_token('OPEN_PAR')
        if(self.token.type == 'NUMBER'):
          self.value()
          self.take_token('CLOSE_PAR')
        elif(self.token.type == 'CLOSE_PAR'):
          self.take_token(self.token.type)
        else:
          self.error(f'This number: "{self.token.value}" is not suitable')
        
  
      elif self.token.type == 'voltageprobe' or self.token.type == 'currentprobe':
        self.take_token(self.token.type)
        self.take_token('OPEN_PAR')
        self.take_token('CLOSE_PAR')
      
      elif self.token.type == 'resistor'or self.token.type == 'capacitor'or self.token.type == 'inductor':
        self.take_token(self.token.type)
        self.take_token('OPEN_PAR')
        if(self.token.type == 'NUMBER'):
          self.take_token(self.token.type)
          self.take_token('CLOSE_PAR')   
        else:
          self.error("There must be a value in element like: resistor, capacitor, inductor")

      elif self.token.type == 'diode':
        self.take_token('diode')
        self.take_token('OPEN_PAR')

        if self.token.type == "ID":
          self.diode()

        elif self.token.type == "CLOSE_PAR":
          self.take_token('CLOSE_PAR')
          pass

        else:
          self.error("Wrong diode parameters")

      else:
        self.error("Wrong name of electric equipment")
            
      self.assign_num += 1
      print("assign_stmt", self.assign_num ,"OK")
      pass

    else:
      self.error("Epsilon not allowed")
  
  def diode(self):

    self.take_token('ID')
    self.take_token('ASSIGN')  
    self.value()

    if self.token.type == 'COMMA':
      self.take_token('COMMA')
      self.diode()
    else:
      self.take_token('CLOSE_PAR')
      pass


  def value(self):
    # value -> NUMBER
    if self.token.type == 'NUMBER':
      self.take_token('NUMBER')     
      pass
    else:
      self.error(f'This number: "{self.token.value}" is not suitable')



  # connection statement
  def con_stmt(self):
    if self.token.type == 'OPEN_IDX' or self.token.type == 'gnd':
      if self.empty_line == 0:
        self.error("Definition of electric elements must end with empty line")

      elif self.token.type == 'gnd':
        self.take_token('gnd')
        if self.token.type == 'CON':
          self.con_loop()
          pass

        else:
          self.error("Connection is required")

      elif self.token.type == 'OPEN_IDX':
        self.take_token('OPEN_IDX')
        self.digit()
        self.take_token('CLOSE_IDX')

        if self.token.type == 'CON':
          self.con_loop()
          pass

        else:
          self.error("Connection is required")
        
      else:
        self.error("Connection requiers an object")

    else:
      self.error("Epsilon not allowed")
  

  def con_loop(self):
    self.take_token('CON')
    self.con_blockade = 1
    if self.token.type == 'ID':
      if self.ID_array.count(self.token.value) == 0:
        self.error("electric element was not declared")
      self.take_token('ID')
      self.take_token('OPEN_IDX')
      self.digit()
      self.take_token('CLOSE_IDX')

    elif self.token.type == 'gnd':
      self.take_token('gnd')

    else:
      self.error("Connection requiers an object")
    
    if self.token.type == 'CON':
      self.con_loop()

    else:
      self.con_num += 1
      print("con_stmt", self.con_num ,"OK")
      pass

  def digit(self):
    # value -> NUMBER
    if self.token.type == 'NUMBER':
      if self.token.value.isdigit() == True:
        self.take_token('NUMBER')    
      else:
        self.error('In connection index only digits are acceptable')
      pass
    else:
      self.error(f'This number: "{self.token.value}" is not a digit')

  
       
