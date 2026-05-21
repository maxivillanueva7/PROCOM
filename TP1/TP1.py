from filtro import RaisedCosineFilter

filtroprueba= RaisedCosineFilter(alpha=0.7, span=8, sps=8, rrc=True)

print('Introduzca un comando')
while True:
    comando= input(">")

    if comando == "exit":
        break
    elif comando == "help":
        print("Comandos disponibles son plot, coef y exit.")
    elif comando == "plot":
        filtroprueba.plot(time_domain=True, freq_domain=False)
    elif comando == "coef":
        print(filtroprueba.get_coefficients())
    else:
        print("Comando desconocido con help puede ver la lista de comandos")