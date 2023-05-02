#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.msg import UnencriptedMsg


class message_receiver(Node):

    def __init__(self):
        super().__init__('message_receiver')
        self.Unencriptedsub = self.create_subscription(
            UnencriptedMsg,
            '/messages/unencripted',
            self.handleUnsafeMsg,
            10) # prevent unused variable warning

    def handleUnsafeMsg(self, msg):
        print("\n[UNSAFE] Mensagem não segura recebida:")
        print("[UNSAFE] --> ", msg.msg)



def main():
    rclpy.init()

    node = message_receiver()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()