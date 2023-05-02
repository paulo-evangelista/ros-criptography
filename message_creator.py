#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from turtlesim.srv import SetPen, TeleportAbsolute, Kill, Spawn
from my_interfaces.msg import ToEncriptor, UnencriptedMsg

class message_creator(Node):
    def __init__(self):
        super().__init__("message_creator")
        self.encriptorPublisher = self.create_publisher(ToEncriptor, f'/messages/encript', 10)
        self.unencriptedPublisher = self.create_publisher(UnencriptedMsg, f'/messages/unencripted', 10)
        self.timer = self.create_timer(1.0, self.sendMsg)
        

    def sendMsg(self):
        message = ToEncriptor()
        print("\ninsira a mensagem a ser enviada:")
        inputText = input("--> ")
        isencript = input("Deseja encriptar a mensagem? (s/n): ")
        if isencript.lower() == 's':
            safeMsg = ToEncriptor()
            safeMsg.msg = inputText
            safeMsg.password = input("Insira a senha desejada --> ")
            self.encriptorPublisher.publish(safeMsg)
            print("--Mensagem e senha de criptografia enviadas--")
        else:
            unsafeMsg = UnencriptedMsg()
            unsafeMsg.msg = inputText
            self.unencriptedPublisher.publish(unsafeMsg)
            print("--Mensagem enviada sem criptografia--")


def main():
    rclpy.init()
    node = message_creator()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
