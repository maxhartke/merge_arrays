import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class MultiArrayPublisher(Node):
    def __init__(self):
        super().__init__('multi_array_publisher')
        self.publisher1_ = self.create_publisher(Int32MultiArray, '/input/array1', 10)
        self.publisher2_ = self.create_publisher(Int32MultiArray, '/input/array2', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg1 = Int32MultiArray(data=[1, 4, 8, 12, 26])
        msg2 = Int32MultiArray(data=[3, 9, 18, 20, 30])
        self.publisher1_.publish(msg1)
        self.publisher2_.publish(msg2)
        self.get_logger().info(", ".join(str(x) for x in msg1.data))
        self.get_logger().info(", ".join(str(x) for x in msg2.data))
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    multi_array_publisher = MultiArrayPublisher()
    rclpy.spin(multi_array_publisher)
    multi_array_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

