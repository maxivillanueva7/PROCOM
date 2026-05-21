import time
import serial

#############################################
# Nota:
# Comentar esta linea si se utiliza el puerto serie
# con la FPGA
ser = serial.serial_for_url('loop://', timeout=1) #me permite que yo mismo lea lo que mando a este puerto

#############################################
# Nota:
# Descomentar esta linea si se utiliza el puerto serie
# con la FPGA
#############################################
# ser = serial.Serial(
#     port     = '/dev/ttyUSB1', #COM3
#     baudrate = 9600,
#     parity   = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )

ser.isOpen() #para ver si el puerto esta funcionando
ser.timeout=None #entiendo que espera hasta que llegan los bits que pedimos
ser.flushInput() #limpia el buffer de la entrada
ser.flushOutput() #limpia el buffer de la salida

print('Ingrese un comando:\n')
while 1 :
    char_v = []
    data = input("ToSent: ")
    if data == 'exit':
        if ser.isOpen():
            ser.close()
        break
    else:
        # Arma el vector a transmitir
        for ptr in range(len(data)):
            char_v.append(data[ptr])
        print(char_v)
        
        for ptr in range(len(char_v)):
            ser.write(char_v[ptr].encode())
            time.sleep(1)

        out = ''
        while ser.inWaiting() > 0:
            out += ser.read(1).decode()

        if out != '':
            print(">> " + out)