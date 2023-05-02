#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.msg import ToManager
from my_interfaces.srv import FromManager



class Manager(Node):

    def __init__(self):
        super().__init__('manager')

        self.dataStorage = {}

        self.dataReceiver = self.create_subscription(ToManager, f'/manager/send', self.handleReceive, 10)
        self.dataSender = self.create_service(FromManager, f'/manager/call', self.handleSend)

    def handleReceive(self, msg):
        print("\n[MANAGER] <> [IN] Recebendo novos dados a serem armazenados")
        try:
            self.dataStorage[msg.password] = msg.key
            print("[MANAGER] <> [IN] Dados armazenados com sucesso!")
            print("[MANAGER] <> [IN] Número de senhas armazenadas: " + str(len(self.dataStorage)))
        except:
            print("[MANAGER] <> [IN] Erro ao armazenar dados. Verifique se a senha já não foi utilizada anteriormente. Dados ignorados.")

    def handleSend(self, req, res):
        print("\n[MANAGER] <> [OUT] Recebendo solicitação de chave")
        try:
            answer = self.dataStorage.get(req.password)

            if answer is None:
                print("[MANAGER] <> [OUT] Senha não encontrada. Verifique se a senha foi digitada corretamente.")
                res.key = 404
            else:
                print(answer)
                res.key = answer
                print("[MANAGER] <> [OUT] Chave enviada com sucesso!")
        except:
            print("[MANAGER] <> [OUT] Erro ao encontrar chave.")
            res.key = 404
        return res


def main():
    rclpy.init()

    node = Manager()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()