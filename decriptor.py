#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.msg import EncriptedMsg
from my_interfaces.srv import  FromManager


class Decriptor(Node):

    def __init__(self):
        super().__init__('decriptor')
        self.subscription = self.create_subscription(
            EncriptedMsg,
            '/messages/safe',self.handleMsg, 10)
        
        self.managerCaller = self.create_client(FromManager, '/manager/call')


    def handleMsg(self, msg):
        print("\n[DECRIPTOR] Mensagem criptografada recebida")

        password = input("[ENCRIPTOR] digite a senha para descriptografar a mensagem --> ")
        print("[ENCRIPTOR] Tentando descriptografar mensagem...")

        request = FromManager.Request()
        request.password = password
        future = self.managerCaller.call(request)

        #rclpy.spin_until_future_complete(self, future, timeout_sec=2.0)

        if future.result() is not None:
            print("[ENCRIPTOR] --> Done!")
        else:
            print("Não foi possível comunicar-se com o manager. Tente novamente mais tarde.\n")

def main():
    rclpy.init()

    node = Decriptor()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()