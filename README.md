# Walidator
Uproszczony walidator dla składni ﻿plików z opisem obwodów elektrycznych. Zakres sprawdzanej składni obejmuje konstrukcje wykorzystujące słowa kluczowe:  
  
-voltagesource  
-voltageprobe  
-currentsource  
-currentprobe  
-resistor  
-capacitor  
-inductor  
-diode  
-begin  
-end  
-gnd  

Celem zadania jest praca z gramatyką w notacji BNF, nauka dostrzegania wzorców w analizowanym tekście oraz rozróżniania symboli terminalnych i nieterminalnych.  
Poniżej przykład do walidacji:  
  
begin  
  R1 = resistor(13.2) # rezystor o wartości 13.2 ohm  
  C1 = capacitor(100e-9) # kondensator o wartości 100e-9 faradów  
  VIN = voltagesource()  
  AM1 = currentprobe()  

  VIN[2] -- R1[1]  
  R1[2] -- C1[1]  
  C1[2] -- AM1[1]  
  AM1[2] -- VIN[1]  
  VIN[1] -- gnd  
end  

# Uruchomienie
Aby walidator zadziałał należy uruchomić plik Validator.py, wykorzystano Python w wersji 3.7.1
