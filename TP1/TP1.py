import numpy as np
import matplotlib.pyplot as plt
#import time para la prueba de que si era el puerto serie
import serial
from filtro import RaisedCosineFilter

filtroprueba= RaisedCosineFilter(alpha=0.7, span=8, sps=8, rrc=True)

ser = serial.serial_for_url('loop://', timeout=1) #me permite que yo mismo lea lo que mando a este puerto
ser.flushInput()
ser.flushOutput()

def graficar_comparacion():
    span= filtroprueba.span
    sps= filtroprueba.sps
    rrc= filtroprueba.rrc

    filtro_1= RaisedCosineFilter(alpha=0.2, span=span, sps=sps, rrc=rrc)
    filtro_2= RaisedCosineFilter(alpha=0.5, span=span, sps=sps, rrc=rrc)
    filtro_3= RaisedCosineFilter(alpha=0.8, span=span, sps=sps, rrc=rrc)

    N= span*sps
    t= np.arange(-N//2,N//2+1)/sps

    plt.figure(figsize=(16,9))
    plt.plot(t[:len(filtro_1.taps)], filtro_1.taps, label="Alpha=0.2")
    plt.plot(t[:len(filtro_2.taps)], filtro_2.taps, label="Alpha=0.5")
    plt.plot(t[:len(filtro_3.taps)], filtro_3.taps, label="Alpha=0.8")
    plt.title("Comparación de filtros con variación de alpha")
    plt.ylabel("Amplitud")
    plt.xlabel("Tiempo")
    plt.grid(True)
    plt.legend()
    plt.show()

def graficar_tiempo_y_frecuencia():
    sps = filtroprueba.sps
    span = filtroprueba.span
    N = span * sps
    t = np.arange(-N//2, N//2 + 1) / sps
    t = t[:len(filtroprueba.taps)]
    
    #Copio lo del ejemplo de filtro para pasar a frecuencia
    H = np.fft.fftshift(np.fft.fft(filtroprueba.taps, 1024))
    f = np.linspace(-0.5, 0.5, len(H), endpoint=False)
    H_dB = 20 * np.log10(np.abs(H) + 1e-6)

    plt.figure(figsize=(16,9))
    plt.subplot(1,2,1)
    plt.plot(t[:len(filtroprueba.taps)],filtroprueba.taps)
    plt.title("Respuesta en el Tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.subplot(1,2,2)
    plt.plot(f,H_dB)
    plt.title("En frecuencia")
    plt.xlabel("Frecuencia")
    plt.ylabel("Magnitud en dB")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


print('Introduzca un comando')
while True:
    entrada = input(">")
    mensaje = entrada + "\n"
    mensaje_bytes= mensaje.encode()
    ser.write(mensaje_bytes)
    #time.sleep(2) lo use para probar que verdaderamente se este mandando por el puerto serie.


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
    elif comando == "comparar":
        graficar_comparacion()
    elif comando == "ambas":
        graficar_tiempo_y_frecuencia()    
    elif comando == "generate":
        filtroprueba.taps = filtroprueba._generate_filter()
        print("Filtro generado nuevamente con parámetros cambiados")
    elif comando == "help":
        print("Comandos disponibles son plot, coef,exit, generate, comparar, ambas (muestra ambas respuestas en tiempo y frecuencia del filtro), alpha=<float>, span=<int>, sps=<int> y rrc=<Bool>.")
    elif comando == "plot":
        filtroprueba.plot(time_domain=True, freq_domain=False)
    elif comando == "coef":
        print(filtroprueba.get_coefficients())
    else:
        print("Comando desconocido con help puede ver la lista de comandos")