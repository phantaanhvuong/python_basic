products = []


def print_menu():
    print("\n===== QUẢN LÝ SẢN PHẨM =====")
    print("1. Thêm sản phẩm")
    print("2. Xem danh sách sản phẩm")
    print("3. Tìm sản phẩm theo ID")
    print("4. Cập nhật sản phẩm")
    print("5. Xóa sản phẩm")
    print("6. Thoát")


def create_product():
    print("\n--- THÊM SẢN PHẨM ---")
    try:
        product_id = int(input("Nhập ID sản phẩm: "))
        name = input("Nhập tên sản phẩm: ")
        price = float(input("Nhập giá sản phẩm: "))
        quantity = int(input("Nhập số lượng: "))

        # Kiểm tra ID đã tồn tại chưa
        for product in products:
            if product["id"] == product_id:
                print("ID đã tồn tại, không thể thêm.")
                return

        new_product = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity
        }

        products.append(new_product)
        print("Thêm sản phẩm thành công.")

    except ValueError:
        print("Dữ liệu nhập không hợp lệ.")


def read_products():
    print("\n--- DANH SÁCH SẢN PHẨM ---")
    if not products:
        print("Chưa có sản phẩm nào.")
        return

    for product in products:
        print(
            f"ID: {product['id']} | "
            f"Tên: {product['name']} | "
            f"Giá: {product['price']} | "
            f"Số lượng: {product['quantity']}"
        )


def find_product_by_id():
    print("\n--- TÌM SẢN PHẨM ---")
    try:
        product_id = int(input("Nhập ID cần tìm: "))

        for product in products:
            if product["id"] == product_id:
                print("Đã tìm thấy sản phẩm:")
                print(product)
                return

        print("Không tìm thấy sản phẩm.")

    except ValueError:
        print("ID không hợp lệ.")


def update_product():
    print("\n--- CẬP NHẬT SẢN PHẨM ---")
    try:
        product_id = int(input("Nhập ID sản phẩm cần cập nhật: "))

        for product in products:
            if product["id"] == product_id:
                print("Nhập thông tin mới:")
                product["name"] = input("Tên mới: ")
                product["price"] = float(input("Giá mới: "))
                product["quantity"] = int(input("Số lượng mới: "))

                print("Cập nhật sản phẩm thành công.")
                return

        print("Không tìm thấy sản phẩm để cập nhật.")

    except ValueError:
        print("Dữ liệu nhập không hợp lệ.")


def delete_product():
    print("\n--- XÓA SẢN PHẨM ---")
    try:
        product_id = int(input("Nhập ID sản phẩm cần xóa: "))

        for product in products:
            if product["id"] == product_id:
                products.remove(product)
                print("Xóa sản phẩm thành công.")
                return

        print("Không tìm thấy sản phẩm để xóa.")

    except ValueError:
        print("ID không hợp lệ.")


def main():
    while True:
        print_menu()
        choice = input("Chọn chức năng (1-6): ")

        if choice == "1":
            create_product()
        elif choice == "2":
            read_products()
        elif choice == "3":
            find_product_by_id()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    main()