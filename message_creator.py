#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
from turtlesim.srv import SetPen, TeleportAbsolute, Kill, Spawn


class message_creator(Node):
    def __init__(self):
        super().__init__("message_creator")
        time.sleep(0.4)
        self.messagePublisher = self.create_publisher("Twistchr", f'/messages/encript', 10)
        self.uncriptedMessageClient = self.create_client(TeleportAbsolute, f'/messages/unsafe')
        time.sleep(0.4)

    def kill(self):
        self.killReq = Kill.Request()
        self.killReq.name = self.get_name()
        self.killClient.call_async(self.killReq)
        time.sleep(0.2)

    def teleport(self, x, y):
        self.telReq = TeleportAbsolute.Request()
        self.telReq.x = x
        self.telReq.y = y
        self.teleportClient.call_async(self.telReq)
        time.sleep(0.4)

    def move(self, repeat:int=1, lx=0.0, ly=0.0,lz=0.0, ax=0.0, ay=0.0, az=0.0):
        for i in range(0,repeat):
            self.twist_msg_ = Twist()
            self.twist_msg_.linear.x = lx
            self.twist_msg_.linear.y = ly
            self.twist_msg_.linear.z = lz
            self.twist_msg_.angular.x = ax
            self.twist_msg_.angular.y = ay
            self.twist_msg_.angular.z = az
            self.publisher_.publish(self.twist_msg_)
            time.sleep(1.1)

    def change_pen(self, r=0, g=0, b=0, w=5):
        self.penReq = SetPen.Request()
        self.penReq.off = False
        self.penReq.r = r
        self.penReq.g = g
        self.penReq.b = b      
        self.penReq.width = w
        self.penClient.call_async(self.penReq)

    
def main():
    rclpy.init()

if __name__ == '__main__':
    main()