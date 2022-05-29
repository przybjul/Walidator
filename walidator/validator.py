# Simple example of parsing
# Bartosz Sawicki, 2014-03-13

from scanner import *
from parser1 import *

#input_string = '''
#x := 5;
#y := x;
#PRINT 64;
#'''

input_string = '''
begin # opis obwodu zawsze zawarty jest pomiędzy słowami kluczowymi begin ... end
  v = voltagesource(1.0) # voltagesource z argumentem oznacza stałą wartość napięcia
  u = voltagesource() # voltagesource bez argumentu oznacza źródło o napięciu ustalanym w trakcie analizy obwodu
  r = resistor(1400) # rezystor wymaga podania wartości swojej rezystancji
# sekcja definicji elementów obwodu musi kończyć się co najmniej jedną pustą linią (bez komentarza)
# wcięcia są nieistotne
  c = capacitor(5e-12) # kondensator wymaga podania wartości swojej pojemności
  l = inductor(0.000001) # cewka wymaga podania wartości swojej indukcyjności



  u[2] -- r[1] # ta linia oznacza, że złącze nr 2 źródła napięcia u jest połączone ze złączem nr 1 rezystora r 
  r[2] -- l[1]
  l[2] -- c[1]
  c[2] -- v[1]
  v[2] -- u[1] -- gnd # ta linia oznacza, że złącze nr 2 źródła napięcia v jest połączone ze złączem nr 1 źródła napięcia u oraz z uziemieniem gnd
end
'''


def remove_comments(input_string):
    return re.sub('#.*','',input_string)

input_string = remove_comments(input_string)

print(input_string)
scanner = Scanner(input_string)
print(scanner.tokens)

parser = Parser(scanner)
parser.start()

  
