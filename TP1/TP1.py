import time
import serial
from filtro import RaisedCosineFilter

filtroprueba= RaisedCosineFilter(alpha=0.7, span=8, sps=8, rrc=True)

ser = serial.serial_for_url('loop://', timeout=1) #me permite que yo mismo lea lo que mando a este puerto
ser.flushInput()
ser.flushOutput()


print('Introduzca un comando')
while True:
    entrada = input(">")
    mensaje = entrada + "\n"
    mensaje_bytes= mensaje.encode()
    ser.write(mensaje_bytes)
    time.sleep(2)


    comando= ser.readline().decode().strip()

    if "=" in comando:
        dividir= comando.split("=")
        parametro= dividir[0]
        valor=dividir[1]

        if parametro == "alpha":
            valor = float(valor)
            if valor<0 or valor>1:
                print("Valor invalido. Un valor valido es 0<=Alpha<=1.")    
            else:
                filtroprueba.alpha = valor
                print(f"Valor de alpha actualizado a {valor}")

        elif parametro == "span":
            valor = int(valor)
            filtroprueba.span = valor
            print(f"Valor de span actualizado a {valor}")

        elif parametro == "sps":
            valor = int(valor)
            filtroprueba.sps = valor
            print(f"Valor de sps actualizado a {valor}")

        elif parametro == "rrc":
            if valor == "True":
                filtroprueba.rrc= True
                print(f"Valor de rrc actualizado a True")
            elif valor == "False":
                filtroprueba.rrc= False
                print(f"Valor de rrc actualizado a False")
            else:
                print("Valor invalido usar True o False")
                
    elif comando == "exit":
        ser.close()
        break
    elif comando == "generate":
        filtroprueba.taps = filtroprueba._generate_filter()
        print("Filtro generado nuevamente con parámetros cambiados")
    elif comando == "help":
        print("Comandos disponibles son plot, coef,exit, generate, alpha=<float>, span=<int>, sps=<int> y rrc=<Bool>.")
    elif comando == "plot":
        filtroprueba.plot(time_domain=True, freq_domain=False)
    elif comando == "coef":
        print(filtroprueba.get_coefficients())
    else:
        print("Comando desconocido con help puede ver la lista de comandos")