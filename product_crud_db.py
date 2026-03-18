import sqlite3


class Product:
    def __init__(self, product_id, name, price, quantity):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Tên: {self.name} | "
            f"Giá: {self.price} | "
            f"Số lượng: {self.quantity}"
        )


class ProductDB:
    def __init__(self, db_name="products.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def add_product(self, product):
        sql = """
        INSERT INTO products (id, name, price, quantity)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, (product.id, product.name, product.price, product.quantity))
            self.conn.commit()
            print("Thêm sản phẩm thành công.")
        except sqlite3.IntegrityError:
            print("ID đã tồn tại, không thể thêm.")

    def get_all_products(self):
        sql = "SELECT id, name, price, quantity FROM products"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        products = []
        for row in rows:
            product = Product(row[0], row[1], row[2], row[3])
            products.append(product)

        return products

    def find_product_by_id(self, product_id):
        sql = "SELECT id, name, price, quantity FROM products WHERE id = ?"
        self.cursor.execute(sql, (product_id,))
        row = self.cursor.fetchone()

        if row:
            return Product(row[0], row[1], row[2], row[3])
        return None

    def update_product(self, product):
        sql = """
        UPDATE products
        SET name = ?, price = ?, quantity = ?
        WHERE id = ?
        """
        self.cursor.execute(sql, (product.name, product.price, product.quantity, product.id))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print("Cập nhật sản phẩm thành công.")
        else:
            print("Không tìm thấy sản phẩm để cập nhật.")

    def delete_product(self, product_id):
        sql = "DELETE FROM products WHERE id = ?"
        self.cursor.execute(sql, (product_id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print("Xóa sản phẩm thành công.")
        else:
            print("Không tìm thấy sản phẩm để xóa.")

    def close(self):
        self.conn.close()


def print_menu():
    print("\n===== QUẢN LÝ SẢN PHẨM =====")
    print("1. Thêm sản phẩm")
    print("2. Xem danh sách sản phẩm")
    print("3. Tìm sản phẩm theo ID")
    print("4. Cập nhật sản phẩm")
    print("5. Xóa sản phẩm")
    print("6. Thoát")


def create_product_input():
    try:
        product_id = int(input("Nhập ID sản phẩm: "))
        name = input("Nhập tên sản phẩm: ")
        price = float(input("Nhập giá sản phẩm: "))
        quantity = int(input("Nhập số lượng: "))

        if price < 0 or quantity < 0:
            print("Giá và số lượng phải >= 0.")
            return None

        return Product(product_id, name, price, quantity)

    except ValueError:
        print("Dữ liệu nhập không hợp lệ.")
        return None


def show_all_products(db):
    products = db.get_all_products()

    print("\n--- DANH SÁCH SẢN PHẨM ---")
    if not products:
        print("Chưa có sản phẩm nào.")
        return

    for product in products:
        print(product)


def find_product(db):
    try:
        product_id = int(input("Nhập ID cần tìm: "))
        product = db.find_product_by_id(product_id)

        if product:
            print("\nĐã tìm thấy sản phẩm:")
            print(product)
        else:
            print("Không tìm thấy sản phẩm.")

    except ValueError:
        print("ID không hợp lệ.")


def update_product_input(db):
    try:
        product_id = int(input("Nhập ID sản phẩm cần cập nhật: "))
        old_product = db.find_product_by_id(product_id)

        if not old_product:
            print("Không tìm thấy sản phẩm.")
            return

        print("Thông tin hiện tại:")
        print(old_product)

        name = input("Nhập tên mới: ")
        price = float(input("Nhập giá mới: "))
        quantity = int(input("Nhập số lượng mới: "))

        if price < 0 or quantity < 0:
            print("Giá và số lượng phải >= 0.")
            return

        updated_product = Product(product_id, name, price, quantity)
        db.update_product(updated_product)

    except ValueError:
        print("Dữ liệu nhập không hợp lệ.")


def delete_product_input(db):
    try:
        product_id = int(input("Nhập ID sản phẩm cần xóa: "))
        db.delete_product(product_id)

    except ValueError:
        print("ID không hợp lệ.")


def main():
    db = ProductDB()

    while True:
        print_menu()
        choice = input("Chọn chức năng (1-6): ")

        if choice == "1":
            product = create_product_input()
            if product:
                db.add_product(product)

        elif choice == "2":
            show_all_products(db)

        elif choice == "3":
            find_product(db)

        elif choice == "4":
            update_product_input(db)

        elif choice == "5":
            delete_product_input(db)

        elif choice == "6":
            db.close()
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()