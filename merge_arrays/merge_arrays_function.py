import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class MultiArraySubscriber(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        self.subscription1_ = self.create_subscription(Int32MultiArray, '/input/array1', self.subscriber_callback1, 10)
        self.subscription2_ = self.create_subscription(Int32MultiArray, '/input/array2', self.subscriber_callback2, 10)
        self.publisher_ = self.create_publisher(Int32MultiArray, '/output/array', 10)
        self.received_data1_ = []
        self.received_data2_ = []

    def subscriber_callback1(self, msg):
        self.received_data1_ = msg.data
    def subscriber_callback2(self, msg):
        self.received_data2_ = msg.data

        merged_data = []
        while(len(self.received_data1_) > 0 and len(self.received_data2_) > 0):
            if self.received_data1_[0] < self.received_data2_[0]:
                merged_data.append(self.received_data1_[0])
                self.received_data1_.pop(0)
            else:
                merged_data.append(self.received_data2_[0])
                self.received_data2_.pop(0)

        if len(self.received_data1_) > 0:
            merged_data.extend(self.received_data1_)
        if len(self.received_data2_) > 0:
            merged_data.extend(self.received_data2_)

        merged_msg = Int32MultiArray(data=merged_data)
        self.publisher_.publish(merged_msg)
        self.get_logger().info(", ".join(str(x) for x in merged_msg.data))


def main(args=None):
    rclpy.init(args=args)
    merge_arrays_node = MultiArraySubscriber()
    rclpy.spin(merge_arrays_node)
    merge_arrays_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
