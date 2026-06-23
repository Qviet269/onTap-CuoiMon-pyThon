

class Product:
    def __init__(self, id, name, import_price, quantity, storage_fee):
        self.id = id
        self.name = name
        self.import_price = import_price
        self.quantity = quantity
        self.storage_fee = storage_fee
        self.total_value = 0
        self.stock_status = "chưa có dữ liệu"
    
    def calculate_total_value(self):
        self.total_value = (self.import_price * self.quantity) + self.storage_fee
        return self.total_value

    def classify_stock_status(self):

        if self.total_value <= 0:
            print("Tổng giá trị không được bằng và dưới 0")
            return

        if self.total_value < 9000000:
            self.stock_status = "Thấp"
        elif self.total_value < 15000000:
            self.stock_status = "Trung bình"
        elif self.total_value < 30000000:
            self.stock_status = "Cao"
        else:
            self.stock_status = "Rất Cao"

class ProductManager:
    def __init__(self):
        self.products: list[Product] = []
    
    def validate_input(self, prompt: str, type_input: str = "str"):
        while True:
            user_input = input(prompt)

            if not user_input:
                print("Dữ liệu không được bỏ trông!")
                continue

            if type_input == "int":
                try:
                    value = int(user_input)
                    if value <= 0:
                        print("Giá trị phải lớn hơn 0!")
                        continue
                    return value
                except:
                    print("Dữ liệu không hợp lệ!")
                    continue

            if type_input == "quan":
                try:
                    value = int(user_input)
                    if value < 0 or value > 1000:
                        print("Số lượng phải nằm trong khoảng 0 - 1000")
                        continue
                    return value
                except:
                    print("Dữ liệu không hợp lệ!")
                    continue
            return user_input 

    def add_product(self):
        while True:
            input_id = self.validate_input("Nhập mã SP: ")
            for i, v in enumerate(self.products):
                if input_id.upper() == v.id.upper():
                    print("Mã SP đã tồn tại! vui lòng nhập lại")
                    break
            else:
                break
        name = self.validate_input("Nhập tên sản phẩm: ")
        import_price = self.validate_input("Giá nhập sản phẩm: ", "int")
        storage_fee = self.validate_input("Chi phí kho: ", "int")
        quantity = self.validate_input("Nhập số lượng tồn kho: ", "quan")

        new_product = Product(input_id, name, import_price, quantity, storage_fee)
        self.products.append(new_product)
        new_product.calculate_total_value()
        new_product.classify_stock_status()
        print("Thêm thành công!")
        return
    
    def show_all (self):
        if not self.products:
            print("Kho hàng trống!")
            return
        
        print(f"{'Ma SP':<6}| {'Tên sản phẩm':<20}| {'Giá Nhập':<10}| {'Số Lượng':<10}| {'Chi phí kho':<15}| {'Tổng giá trị':<15}| {'Trạng thái tồn':<15}")
        for i, v in enumerate(self.products):
            print(f"{v.id:<6}| {v.name:<20}| {v.import_price:<10}| {v.quantity:<10}| {v.storage_fee:<15}| {v.total_value:<15}| {v.stock_status:<15}")
    
    def update_product(self):
        if not self.products:
            print("Kho hàng trống!")
            return
        
        input_id = self.validate_input("Nhập mã SP cần cập nhật: ")
        for i, v in enumerate(self.products):
            if input_id.upper() == v.id.upper():
                print(f"Đã tìm thấy mã {input_id}")
                v.import_price = self.validate_input("Cập nhật lại giá nhập: ", "int")
                v.quantity = self.validate_input("Cập nhật lại số lượng: ", "quan")
                v.storage_fee = self.validate_input("Cập nhật lại chi phí kho: ", "int")

                v.calculate_total_value()
                v.classify_stock_status()
                print("Đã cập nhật thành công!")
                break
        else:
            print('Không tìm thấy mã SP!')
            return

    def delete_product(self):
        if not self.products:
            print("Kho hàng trống!")
            return
        
        input_id = self.validate_input("Nhập mã SP muốn xóa: ")
        for i, v in enumerate(self.products):
            if input_id.upper() == v.id.upper():
                print('Bạn có chắc chắn muốn xóa sản phẩm này khỏi hệ thống không? (Y/N):')
                mini_choice = self.validate_input("")
                if mini_choice.upper() == "Y":
                    self.products.pop(i)
                    print("bạn đã xóa thành công!")
                    break
                else:
                    print("Thoát không xóa thành công!")
                    break
        else:
            print("Không tìm thấy mã sản phẩm!")
            return
    
    def search_product(self):
        if not self.products:
            print("Kho hàng trống!")
            return
        flag = False
        input_name = self.validate_input("Nhập Tên sản phẩm cần tìm: ")
        for i, v in enumerate(self.products):
            if input_name.title() in v.name.title():
                flag = True
                print(f"{v.id:<6}| {v.name:<20}| {v.import_price:<10}| {v.quantity:<10}| {v.storage_fee:<15}| {v.total_value:<15}| {v.stock_status:<15}")

        if not flag:
            print("Không tìm thấy mã SP!")
            return


def menu():
    print("""
==================== MENU ====================
    1. Hiển thị danh sách sản phẩm trong kho
    2. Nhập sản phẩm mới vào kho
    3. Cập nhật thông tin sản phẩm
    4. xóa sản phẩm khỏi kho
    5. Tìm kiếm sản phẩm theo tên
    6. Thoát
==============================================
""")    

def main():
    manager = ProductManager()
    manager.products = [
        Product("PR001", "Iphone18 ProMax", 36000000, 12, 1000000000)
    ]
    while True:
        menu()
        choice = input("Nhập lựa chọn của bạn: ").strip()
        match choice:
            case "1":
                print("------ Hiển thị danh sách --------")
                manager.show_all()
            case "2":
                print("------ Nhập sản phẩm mơi ---------")
                manager.add_product()
            case "3":
                print("------ Cập nhật -------")
                manager.update_product()
            case "4":
                print("----- Xóa sản phẩm --------")
                manager.delete_product
            case "5":
                print("----- Tìm kiếm ---------")
                manager.search_product()
            case "6":
                print("Cmả ơn bạn đã sử dụng hệ thống quản lý kho hàng!")
                break
            case _:
                print("Lựa chọn không hợp lệ!")
if __name__ == "__main__":
    main()