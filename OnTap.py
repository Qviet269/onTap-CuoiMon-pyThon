class DeliveryOrder:
    def __init__(self, order_id, receiver_name, base_fee, distance, surcharge):
        self.order_id = order_id
        self.receiver_name = receiver_name
        self.base_fee  = base_fee
        self.distance = distance
        self.surcharge = surcharge
        self.total_delivery_cost = 0
        self.delivery_status  = "Chưa có dữ liệu"
    
    def calculate_total_cost(self):
        self.total_delivery_cost = (self.base_fee  * self.distance ) + self.surcharge 
        return self.total_delivery_cost

    def classify_delivery_status(self):
        if self.total_delivery_cost < 0:
            print("Tổng chi phí không được âm!")
            return

        if self.total_delivery_cost < 100000:
            self.delivery_status = "Đơn hàng tiêu chuẩn"
        elif self.total_delivery_cost < 300000:
            self.delivery_status = "Đơn hàng Cận tỉnh"
        elif self.total_delivery_cost < 600000:
            self.delivery_status = "Đơn hàng Đường dài"
        else:
            self.delivery_status = "Đơn hàng Đặc biệt"
            

class OrderManager:
    def __init__(self):
        self.orders: list[DeliveryOrder] = []

    def validate_orders (self, prompt: str, input_type: str = "str"):
        while True:
            input_user = input(prompt).strip()

            if not input_user :
                print("Dữ liệu không được bỏ trống!")
                continue

            if input_type == "int":
                try:
                    value = int(input_user)
                    if value <= 0:
                        print("Giá trị phải lớn hơn 0!")
                        continue
                    return value
                except:
                    print("Dữ liệu không hợp lệ!")
                    continue
            
            if input_type == "km":
                try:
                    value = int(input_user)
                    if value < 1 or value > 5000:
                        print("Khoảng cách nằm trong đoạn từ 1 đến 5000 km")
                        continue
                    return value
                except:
                    print("Dữ liệu không hợp lệ!")
                    continue

            return input_user
        
    def add_order(self):
            while True:
                input_id = self.validate_orders("Nhập mã đơn muốn thêm: ")
                for i, v in enumerate(self.orders):
                    if input_id.upper() == v.order_id.upper():
                        print("Mã đã tồn tại! Hãy nhập lại")
                        break
                else:
                    break

            receiver_name = self.validate_orders("Nhập tên người nhận: ")
            base_fee = self.validate_orders("Nhập Cước phí: ", "int")
            distance = self.validate_orders("Nhập Khoảng cách giao hàng - KM", "km")
            surcharge = self.validate_orders("Nhập phụ phí: ", "int")

            new_order = DeliveryOrder (input_id, receiver_name, base_fee, distance, surcharge)
            self.orders.append(new_order)
            new_order.calculate_total_cost()
            new_order.classify_delivery_status()
            print("Đã thêm thông tin thành công!")
            return
    
    def show_all_orders(self):
        if not self.orders:
            print("Đơn hàng rỗng!")
            return
        
        print(f"{'Mã Đơn':<6}| {'Tên Người Nhận':<20}| {'Cước nền':<10}| {'Khoảng cách(KM)':<15}| {'Phụ phí':<10}| {'Tổng chi phí':<15}| {'Trạng thái đơn':<25}")
        for i, v in enumerate(self.orders):
            print(f"{v.order_id:<6}| {v.receiver_name:<20}| {v.base_fee:<10}| {v.distance:<15} KM| {v.surcharge :<10}| {v.total_delivery_cost :<15}| {v.delivery_status :<25}")

    def update_order(self):
        if not self.orders:
            print("Đơn hàng rỗng!")
            return
        
        input_id = self.validate_orders("Nhập mã đơn cần cập nhật: ")
        for i, v in enumerate(self.orders):
            if input_id.upper() == v.order_id.upper():
                v.base_fee = self.validate_orders("Nhập Cước nền cần cập nhật: ", "int")
                v.distance = self.validate_orders("Nhập khoảng cách cần cập nhật: ", "km")
                v.surcharge = self.validate_orders("Nhập phụ phí: ", "int")

                v.calculate_total_cost()
                v.classify_delivery_status()
                print('Đã cập nhật thành công!')
                break
        else:
            print("Không tìm thấy mã!")
            return
    
    def delete_order (self):
        if not self.orders:
            print("Đơn hàng rỗng!")
            return
        
        input_id = self.validate_orders("Nhập mã đơn cần xóa: ")
        for i, v in enumerate(self.orders):
            if input_id.upper() == v.order_id.upper():
                print("Bạn có chắc chắn muốn xóa đơn này khỏi hệ thống không? (Y/N)")
                mini_choice = self.validate_orders("")
                if mini_choice.upper() == "Y":
                    self.orders.pop(i)
                    print("bạn đã xóa thành công!")
                    break
                else:
                    print("Bạn đã xác nhận không muốn xóa!")
                    break
        else:
            print("Không tìm thấy mã!")
            return
        
    def search_by_receiver (self):
        if not self.orders:
            print("Đơn hàng rỗng!")
            return
        flag = False
        input_name = self.validate_orders("Nhập tên đơn hàng cần tìm: ")
        for i, v in enumerate(self.orders):
            if input_name.title() in v.receiver_name .title():
                flag = True
                print(f"{v.order_id:<6}| {v.receiver_name:<20}| {v.base_fee:<10}| {v.distance:<10}| {v.surcharge :<10}| {v.total_delivery_cost :<15}| {v.delivery_status :<25}")
        if not flag:
            print("Không tìm thấy mã!")
            return
                
def menu():

    print("""
================ MENU ================
1. Hiển thị danh sách vận đơn trong hệ thống
2. Nhập vận đơn mới
3. Cập nhật thông tin vận đơn
4. Xóa vận đơn khỏi hệ thống
5. Tìm kiếm vận đơn theo tên người nhận
6. Thoát
=====================================
""")
    
def main():
    manager = OrderManager()
    manager.orders = [
        DeliveryOrder("HR001", "Quốc Việt", 16000, 37, 16000)
    ]
    while True:
        menu()

        choice = input("Nhập lựa chọn của bạn: ").strip()
        match choice:
            case "1":
                print("------ Hiển thị danh sách -----")
                manager.show_all_orders()
            case "2":
                print("------ Thêm thông tin -----")
                manager.add_order()
            case "3":
                print("---- Cập nhật -----")
                manager.update_order()
            case "4":
                print("---- Xóa mã ----")
                manager.delete_order()
            case "5":
                print("----- tìm kiếm -----")
                manager.search_by_receiver()
            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vận đơn!")
                break
            case _:
                print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
