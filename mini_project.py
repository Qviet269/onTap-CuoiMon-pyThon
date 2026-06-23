import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.ERROR, format='%(message)s')

class BaseDevice(ABC):
    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1000000

    def __init__(self, device_code, device_name, **kwargs):
        if not self.validate_device_code(device_code):
            raise ValueError("ERR-IOT-01")
        
        self.device_code = device_code
        self.device_name = device_name
        self.__operating_hours = 0
        super().__init__(**kwargs)

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        self._device_name = " ".join(value.split()).upper()

    @property
    def operating_hours(self):
        return self.__operating_hours

    def _add_operating_hours(self, hours):
        if hours < 0:
            raise ValueError("ERR-IOT-03")
        self.__operating_hours += hours

    @staticmethod
    def validate_device_code(device_code):
        return len(device_code) == 10 and device_code[0].isalpha()

    @classmethod
    def update_maintenance_cost(cls, new_cost):
        cls.base_maintenance_cost = new_cost

    @abstractmethod
    def track_performance(self):
        pass

    @abstractmethod
    def run_diagnostic(self):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours + other.operating_hours

    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours < other.operating_hours

class ProductionRobot(BaseDevice):
    def __init__(self, device_code, device_name, **kwargs):
        super().__init__(device_code, device_name, **kwargs)
        self.completed_products = kwargs.get('completed_products', 0)

    def track_performance(self, hours=0, products=0):
        self._add_operating_hours(hours)
        if products < 0:
            raise ValueError("ERR-IOT-03")
        self.completed_products += products
        
        max_capacity = 300 
        oee = (self.completed_products / (self.operating_hours * max_capacity)) * 100 if self.operating_hours > 0 else 0.0
        
        print(f"[Thành công]: Đã cập nhật số liệu vận hành.")
        print(f"Tổng số giờ chạy tích lũy: {self.operating_hours} giờ.")
        print(f"Chỉ số hiệu suất thiết bị tổng thể (OEE): {oee:.1f}%")

    def run_diagnostic(self):
        if self.completed_products > 10000:
            print("[Cảnh báo hệ thống]: Thiết bị phát hiện trạng thái bất thường!")
            print(f"Kết quả chẩn đoán: Cần bảo dưỡng gấp! (Sản lượng hiện tại: {self.completed_products})")
            print(f"Định mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND")
        else:
            print("Thiết bị hoạt động trong trạng thái ổn định.")

class ThermalSensor(BaseDevice):
    def __init__(self, device_code, device_name, **kwargs):
        super().__init__(device_code, device_name, **kwargs)
        self.current_temperature = kwargs.get('current_temperature', 0.0)
        self.safety_threshold = kwargs.get('safety_threshold', 80.0)

    def track_performance(self, hours=0, temperature=0.0):
        self._add_operating_hours(hours)
        self.current_temperature = temperature
        
        print(f"[Thành công]: Đã cập nhật số liệu vận hành.")
        print(f"Tổng số giờ chạy tích lũy: {self.operating_hours} giờ.")
        print(f"Nhiệt độ hiện tại: {self.current_temperature} độ C")

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            print("[Cảnh báo hệ thống]: Thiết bị phát hiện trạng thái bất thường!")
            print(f"Kết quả chẩn đoán: Nguy hiểm: Vượt ngưỡng nhiệt! (Nhiệt độ hiện tại: {self.current_temperature} độ C / Ngưỡng an toàn: {self.safety_threshold} độ C)")
            print(f"Định mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND")
        else:
            print("Thiết bị cảm biến nhiệt độ hoạt động ổn định.")

class HybridSmartActuator(ProductionRobot, ThermalSensor):
    def __init__(self, device_code, device_name, **kwargs):
        super().__init__(device_code, device_name, **kwargs)

    def track_performance(self, hours=0, products=0, temperature=0.0):
        self._add_operating_hours(hours)
        if products < 0:
            raise ValueError("ERR-IOT-03")
        self.completed_products += products
        self.current_temperature = temperature
        
        max_capacity = 300 
        oee = (self.completed_products / (self.operating_hours * max_capacity)) * 100 if self.operating_hours > 0 else 0.0
        
        print(f"[Thành công]: Đã cập nhật số liệu vận hành.")
        print(f"Tổng số giờ chạy tích lũy: {self.operating_hours} giờ.")
        print(f"Chỉ số hiệu suất thiết bị tổng thể (OEE): {oee:.1f}%")
        print(f"Nhiệt độ hiện tại: {self.current_temperature} độ C")

    def run_diagnostic(self):
        issues = []
        if self.completed_products > 10000:
            issues.append(f"Vượt tải sản lượng ({self.completed_products})")
        if self.current_temperature > self.safety_threshold:
            issues.append(f"Nguy hiểm: Vượt ngưỡng nhiệt! ({self.current_temperature} > {self.safety_threshold} độ C)")
            
        if issues:
            print("[Cảnh báo hệ thống]: Thiết bị phát hiện trạng thái bất thường!")
            print(f"Kết quả chẩn đoán: {' | '.join(issues)}")
            print(f"Định mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND")
        else:
            print("Thiết bị truyền động thông minh (Hybrid) hoạt động ổn định.")

class MQTTEngineGateway:
    def process_stream(self, device):
        print("[Hệ thống MQTT Engine]: Đang khởi tạo băng thông kết nối dữ liệu IoT...")
        print("Xác thực cổng ngoại vi bằng Duck Typing thành công!")
        print(f"Dữ liệu của thiết bị {device.device_code} đã được đóng gói và xuất chuỗi luồng thành công.")

class ERPReportGateway:
    def process_stream(self, device):
        print("[Hệ thống ERP]: Đang đồng bộ hóa kho dữ liệu sản xuất...")
        print("Xác thực cổng ngoại vi bằng Duck Typing thành công!")
        print(f"Dữ liệu của thiết bị {device.device_code} đã được ghi nhận vào ERP.")

def export_telemetry_data(data_gateway, device_object):
    if not hasattr(data_gateway, 'process_stream'):
        raise TypeError("ERR-IOT-05")
    data_gateway.process_stream(device_object)

def print_menu():
    print("\n--- RIKKEI SMART FACTORY IOT SIMULATOR ---")
    print("1. Đăng ký & Khởi tạo thiết bị IoT mới")
    print("2. Xem thông tin thiết bị & Thứ tự kế thừa (MRO)")
    print("3. Check-in giờ vận hành & Cập nhật chỉ số (Đa hình)")
    print("4. Thực thi quy trình tự chẩn đoán kỹ thuật (Diagnostic)")
    print("5. Cộng gộp thời gian tải & So sánh hao mòn (Toán tử)")
    print("6. Xuất dữ liệu vận hành ra Cổng ngoại vi (Duck Typing)")
    print("7. Thoát chương trình")

def main():
    devices_list = []
    current_device = None

    while True:
        print_menu()
        choice = input("Chọn chức năng (1-7): ")

        try:
            match choice:
                case '1':
                    print("\n--- ĐĂNG KÝ THIẾT BỊ IOT MỚI ---")
                    print("1. Production Robot (Robot sản xuất lắp ráp)")
                    print("2. Thermal Sensor (Cảm biến nhiệt độ)")
                    print("3. Hybrid Smart Actuator (Thiết bị truyền động lai)")
                    dev_type = input("Chọn phân loại thiết bị (1-3): ")
                    
                    code = input("Nhập mã thiết bị 10 ký tự: ")
                    name = input("Nhập tên thiết bị: ")
                    
                    match dev_type:
                        case '1':
                            current_device = ProductionRobot(code, name)
                            print("[Thành công]: Đăng ký Robot sản xuất thành công!")
                        case '2':
                            current_device = ThermalSensor(code, name)
                            print("[Thành công]: Đăng ký Cảm biến nhiệt độ thành công!")
                        case '3':
                            current_device = HybridSmartActuator(code, name)
                            print("[Thành công]: Đăng ký Thiết bị lai thành công!")
                        case _:
                            raise ValueError("ERR-IOT-06")
                        
                    print(f"Tên thiết bị: {current_device.device_name}")
                    devices_list.append(current_device)

                case '2':
                    if current_device is None:
                        raise AttributeError("ERR-IOT-02")
                        
                    print("\n--- THÔNG TIN THIẾT BỊ HIỆN TẠI ---")
                    print(f"Loại thiết bị: {current_device.__class__.__name__}")
                    print(f"Nhà máy: {current_device.factory_name}")
                    print(f"Mã thiết bị: {current_device.device_code}")
                    print(f"Tên thiết bị: {current_device.device_name}")
                    print(f"Số giờ vận hành: {current_device.operating_hours} giờ")
                    
                    match current_device:
                        case HybridSmartActuator():
                            print(f"Sản phẩm hoàn thành: {current_device.completed_products} sản phẩm")
                            print(f"Nhiệt độ hiện tại: {current_device.current_temperature} độ C")
                        case ProductionRobot():
                            print(f"Sản phẩm hoàn thành: {current_device.completed_products} sản phẩm")
                        case ThermalSensor():
                            print(f"Nhiệt độ hiện tại: {current_device.current_temperature} độ C")
                        
                    mro_path = " -> ".join([cls.__name__ for cls in current_device.__class__.mro()])
                    print(f"[Hệ thống MRO]: {mro_path}")

                case '3':
                    if current_device is None:
                        raise AttributeError("ERR-IOT-02")
                        
                    print("\n--- GHI NHẬN SỐ LIỆU VẬN HÀNH ---")
                    try:
                        hours = float(input("Nhập số giờ chạy mới phát sinh: "))
                        match current_device:
                            case HybridSmartActuator():
                                products = int(input("Nhập số lượng sản phẩm hoàn thành mới bổ sung: "))
                                temp = float(input("Nhập nhiệt độ hệ thống cập nhật: "))
                                current_device.track_performance(hours=hours, products=products, temperature=temp)
                            case ProductionRobot():
                                products = int(input("Nhập số lượng sản phẩm hoàn thành mới bổ sung: "))
                                current_device.track_performance(hours=hours, products=products)
                            case ThermalSensor():
                                temp = float(input("Nhập nhiệt độ hệ thống cập nhật: "))
                                current_device.track_performance(hours=hours, temperature=temp)
                    except ValueError:
                        raise ValueError("ERR-IOT-03")

                case '4':
                    if current_device is None:
                        raise AttributeError("ERR-IOT-02")
                    print("\n--- QUY TRÌNH TỰ CHẨN ĐOÁN LỖI KỸ THUẬT ---")
                    current_device.run_diagnostic()

                case '5':
                    if current_device is None:
                        raise AttributeError("ERR-IOT-02")
                        
                    print("\n--- KIỂM KÊ & SO SÁNH TẢI (OPERATOR OVERLOADING) ---")
                    print(f"Thiết bị hiện tại (A): {current_device.device_code} (Số giờ chạy: {current_device.operating_hours} giờ)")
                    
                    other_device = ThermalSensor("IOT0099999", "CẢM BIẾN NHIỆT LÒ NUNG")
                    other_device._add_operating_hours(250)
                    
                    print(f"Chọn thiết bị đối ứng (B) từ danh sách: {other_device.device_code} ({other_device.device_name} - Số giờ chạy: {other_device.operating_hours} giờ)")
                    
                    if current_device < other_device:
                        print("[Kết quả So sánh (__lt__)]: Hao mòn (số giờ chạy) của thiết bị A ÍT HƠN thiết bị B.")
                    else:
                        print("[Kết quả So sánh (__lt__)]: Hao mòn (số giờ chạy) của thiết bị A NHIỀU HƠN HOẶC BẰNG thiết bị B.")
                    
                    total_hours = current_device + other_device
                    print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời gian tải vận hành của cả 2 thiết bị là: {total_hours} giờ.")

                case '6':
                    if current_device is None:
                        raise AttributeError("ERR-IOT-02")
                        
                    print("\n--- XUẤT DỮ LIỆU VẬN HÀNH RA CỔNG NGOẠI VI ---")
                    print("1. Xuất dữ liệu qua cổng MQTT (Cloud Stream)")
                    print("2. Đồng bộ số liệu vào hệ thống quản trị ERP")
                    gw_choice = input("Chọn cổng kết nối ngoại vi (1-2): ")
                    
                    match gw_choice:
                        case '1':
                            gateway = MQTTEngineGateway()
                        case '2':
                            gateway = ERPReportGateway()
                        case _:
                            raise ValueError("ERR-IOT-06")
                        
                    export_telemetry_data(gateway, current_device)

                case '7':
                    print("Cảm ơn bạn đã sử dụng hệ thống Quản lý Thiết bị Rikkei Smart Factory IoT Pro!")
                    break

                case _:
                    raise ValueError("ERR-IOT-06")

        except ValueError as e:
            match str(e):
                case "ERR-IOT-01":
                    logging.error("[Lỗi] (ERR-IOT-01): Mã thiết bị không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng tiền tố quy định.")
                case "ERR-IOT-03":
                    logging.error("[Lỗi] (ERR-IOT-03): Định dạng dữ liệu sai! Giá trị nhập vào phải là số lớn hơn 0.")
                case "ERR-IOT-06":
                    logging.error("[Lỗi] (ERR-IOT-06): Lựa chọn không hợp lệ! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 7.")
                case _:
                    logging.error("[Lỗi] (ERR-IOT-03): Định dạng dữ liệu sai! Giá trị nhập vào phải là số lớn hơn 0.")
                    
        except AttributeError as e:
            match str(e):
                case "ERR-IOT-02":
                    logging.error("[Lỗi] (ERR-IOT-02): Thao tác bị từ chối! Hệ thống chưa có thông tin thiết bị hoạt động.")
                case _:
                    logging.error(f"Lỗi thuộc tính: {e}")
                
        except TypeError as e:
            match str(e):
                case "ERR-IOT-04":
                    logging.error("[Lỗi] (ERR-IOT-04): Lỗi kiểu dữ liệu! Không thể thực hiện toán tử với đối tượng ngoài hệ thống.")
                case "ERR-IOT-05":
                    logging.error("[Lỗi] (ERR-IOT-05): Xung đột kiến trúc! Không thể xuất dữ liệu do cấu hình cổng ngoại vi không tương thích.")
                case _:
                    logging.error(f"Lỗi kiểu dữ liệu: {e}")

if __name__ == "__main__":
    main()