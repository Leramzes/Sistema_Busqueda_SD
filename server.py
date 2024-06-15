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

    def exposed_depositar(self, amount, sender, receiver):
        userReceiver = receiver.upper()
        userSender = sender.upper()
        
        receiver_found = False
        for user in self.data:
            if user["usuario"] == userReceiver:
                user["saldo"] += amount
                guardar_archivo(self.data, "data.txt")
                receiver_found = True
                break
        
        if receiver_found:
            if userSender != userReceiver:
                for user in self.data:
                    if user["usuario"] == userSender:
                        user["saldo"] -= amount
                        guardar_archivo(self.data, "data.txt")
                        guardar_transaccionD("Deposito", userReceiver, userSender, amount, self.data)
                        return f"Depósito realizado correctamente a {userReceiver}"
            else:
                guardar_transaccionD("Deposito a cuenta propia", userReceiver, userSender, amount, self.data)
                return "Depósito realizado correctamente a su cuenta"
        else:
            return "No se encontró el usuario"
    
    def exposed_retirar(self, amountRetire, user):
        for users in self.data:
            if users["usuario"] == user.upper():
                if users["saldo"] >= amountRetire:
                    users["saldo"] -= amountRetire
                    guardar_archivo(self.data, "data.txt")
                    guardar_transaccionR("Retiro", user, amountRetire, self.data)
                    return f"Retiro realizado correctamente.\nSaldo actual: {str(users["saldo"])}"
                else:
                    return f"No tiene saldo suficiente.\nSaldo actual: {str(users["saldo"])}"
        return "No se encontro el usuario"
    
    def exposed_listar_Transaction(self, user):
        user = user.upper()
        transactions_list = []
        
        for usuario in self.data:
            if usuario["usuario"] == user:
                for transaction in usuario["transacciones"]:
                    transaction_info = {
                        "ID": transaction["id"],
                        "Tipo": transaction["tipo"],
                        "Fecha": transaction["fecha"],
                        "Usuario Origen": transaction.get("usuario origen", None),
                        "Usuario Destino": transaction.get("usuario destino", None),
                        "Monto": transaction["monto"]
                    }
                    transactions_list.append(transaction_info)
                return transactions_list  # Devuelve la lista de transacciones encontradas

        return None  
                
                

        



        


if __name__ == "__main__":
    server = ThreadedServer(MiClaseService, port=7000)
    print("Server RPC iniciado...")
    server.start()
    