from rpyc import Service
from rpyc.utils.server import ThreadedServer
from library import *



class MiClaseService(Service):
    def __init__(self):
        self.data = leer_archivo("data.txt")


    def on_connect(self, conn):
        print("MiClaseService::on_connect")
        
    def on_disconnect(self, conn):
        print("MiClaseService::on_disconnect")

    def exposed_logear(self, user,  password):
        userConfirm = buscar_igual(self.data, "usuario", user)
        passwordConfirm = buscar_igual(self.data, "clave", encript(password))
        if userConfirm and passwordConfirm:
            return True
        return False

    #agg logica para descontar saldo de quien deposita otro user
    def exposed_depositar(self, amount, sender, receiver):
        userReceiver = receiver.upper()
        userSender = sender.upper()
        for users in self.data:
            if users["usuario"] == userReceiver:
                users["saldo"] += amount
                guardar_archivo(self.data, "data.txt")
                if userSender != userReceiver:
                    #guardar_transaccion("Depósito",userSender,amount,self.data)
                    return "Deposito realizado correctamente a " + users["usuario"]
                else:
                    return "Deposito realizado correctamente a su cuenta"
        return "No se encontro el usuario"
    
    def exposed_retirar(self, amountRetire, user):
        for users in self.data:
            if users["usuario"] == user.upper():
                if users["saldo"] >= amountRetire:
                    users["saldo"] -= amountRetire
                    guardar_archivo(self.data, "data.txt")
                    return "Retiro realizado correctamente.\nSaldo actual: "+str(users["saldo"])
                else:
                    return "No tiene saldo suficiente.\nSaldo actual: "+str(users["saldo"])
        
        return "No se encontro el usuario"
        



        


if __name__ == "__main__":
    server = ThreadedServer(MiClaseService, port=7000)
    print("Server RPC iniciado...")
    server.start()
    