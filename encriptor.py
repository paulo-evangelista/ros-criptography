#!/usr/bin/env python3
import rclpy
from cryptography.fernet import Fernet
from rclpy.node import Node
from my_interfaces.msg import ToEncriptor, EncriptedMsg, ToManager


class Encriptor(Node):

    def __init__(self):
        super().__init__('encriptor')
        self.subscription = self.create_subscription(
            ToEncriptor,
            '/messages/encript',
            self.handleMsg,
            10)
        
        self.encriptedMsgPublisher = self.create_publisher(EncriptedMsg, f'/messages/safe', 10)

        self.managerPublisher = self.create_publisher(ToManager, f'/manager/send', 10)

    def handleMsg(self, msg):
        print("\n[ENCRIPTOR] Mensagem recebida com senha")

        key = Fernet.generate_key()
        f = Fernet(key)
        encriptedMsg = f.encrypt(bytes(msg.msg, 'utf-8'))

        print("[ENCRIPTOR] Enviando mensagem criptografada...")
        encriptedInfo = EncriptedMsg()
        encriptedInfo.msg = encriptedMsg
        self.encriptedMsgPublisher.publish(encriptedInfo)

        print("[ENCRIPTOR] --> Done!")
        print("[ENCRIPTOR] Enviando chave e senha para o Manager...")

        managerMsg = ToManager()
        managerMsg.key = key
        managerMsg.password = msg.password
        self.managerPublisher.publish(managerMsg)

        print("[ENCRIPTOR] --> Done!\n")



def main():
    rclpy.init()

    node = Encriptor()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()