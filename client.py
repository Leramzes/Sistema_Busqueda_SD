import rpyc
from library import *
import getpass

host_server = "localhost"
port_server = 7000

# Conectar al server RPC
conn = rpyc.connect(host_server, port_server)

endMenu = False
while endMenu == False:

    print("#### SISTEMA DE TRANSACCIONES BANCARIAS ####")
    user = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su clave: ")
    print(password)

    logeado = conn.root.exposed_logear(user, password)
    if logeado:
        print("Logeado con exito \n")
        while logeado:
            print("##########################")
            print(f"# Usuario: {user} #")
            print("# 1. Movimiento-Depositar#")
            print("# 2. Movimiento-Retirar  #")
            print("# 3. Ver Transacciones   #")
            print("# 4. Salir               #")
            print("##########################")
            opc = int(input("Ingrese su opcion:"))

            if opc == 1:
                userReceiver = str(input("Ingrese el código del usuario a depositar: "))
                amount = float(input("Ingrese el monto a depositar: "))
                result = conn.root.exposed_depositar(amount,user,userReceiver)
                print(result)
            if opc == 2:
                amount = float(input("Ingrese el monto a retirar: "))
                result = conn.root.exposed_retirar(amount,user)
                print(result)
            if opc == 3:
                result = conn.root.listar_Transaction(user)
                if not result:
                    print("No tiene transacciones registradas")
                else:
                    print(format_transacciones(result))
            if opc == 4:
                logeado = False
                print("Exit\n")

    else:
        print("Credenciales incorrectas")
