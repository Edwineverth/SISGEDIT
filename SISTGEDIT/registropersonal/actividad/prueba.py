import time

ahora = time.strftime("%c")
# representacion de fecha y hora
print ("Fecha y hora " + time.strftime("%c"))

# representacion del tiempo
print ("Fecha " + time.strftime("%x"))

hola = time.strftime("%x")
print ("la fecha actual es ", hola)

# representacion de la hora
print ("Hora " + time.strftime("%X"))

# Muestra fecha y hora actual a partir de la variable
print("Fecha y hora de la variable %s" % ahora)

print ("La fecha de hoy en el sistema es: ", time.strftime("%d/%m/%Y"))