import pandas as pd
import datetime
import random
import json
# # Категории товаров
categories = [
    {"category_id": 1, "category_name": "Electronics"},
    {"category_id": 2, "category_name": "Books"},
    {"category_id": 3, "category_name": "Clothing"},
    {"category_id": 4, "category_name": "Home"},
    {"category_id": 5, "category_name": "Sports"},
    {"category_id": 6, "category_name": "Toys"},
    {"category_id": 7, "category_name": "Beauty"},
    {"category_id": 8, "category_name": "Automotive"},
    {"category_id": 9, "category_name": "Grocery"},
    {"category_id": 10,"category_name": "Garden"}
]
df_categories = pd.DataFrame(categories)
df_categories.to_csv("spark-client/dataset/categories.csv", index=False)
print("Создан файл categories.csv с категориями:", df_categories.shape)
df_categories.head()


#Генерируем 1000 товаров с случайными категориями и ценой
products = []
for prod_id in range(1, 1001):
    product = {
        "product_id": prod_id,
        "product_name": f"Product_{prod_id}",
        "category_id": random.randint(1, len(categories)),
        "price": round(random.uniform(5.0, 500.0), 2)  # цена от 5 до 500
    }
    products.append(product)

# Сохраняем в JSON (по строкам)
with open("spark-client/dataset/products.json", "w") as f:
    for prod in products:
        f.write(f"{json.dumps(prod)}\n")
print("Создан файл products.json с товарами:", len(products))
# Вывод первых 3 товаров для примера
print(pd.DataFrame(products).head(3))
import mysql.connector
import string
# Генерация 50000 клиентов
conn = mysql.connector.connect(host="localhost", user="testuser", password="testpass", database = "testdb")
cursor = conn.cursor()
# cursor.execute("CREATE DATABASE IF NOT EXISTS shop")
# cursor.execute("USE shop")
# Создаем таблицу customers
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY,
        name VARCHAR(100),
        city VARCHAR(100)
    )
""")
num_customers = 50000
customers = []
for cid in range(1, num_customers+1):
    name = "Customer_" + str(cid)
    city = "City_" + str(random.randint(1, 100))  # случайный город из 100 возможных
    customers.append((cid, name, city))

# Вставка данных батчами по 1000 записей
batch_size = 1000
for i in range(0, len(customers), batch_size):
    batch = customers[i:i+batch_size]
    cursor.executemany("INSERT INTO customers (customer_id, name, city) VALUES (%s, %s, %s)", batch)
    conn.commit()
print(f"Inserted {num_customers} customers into MySQL.")
cursor.close()
conn.close()

num_orders = 100000   # число заказов
orders = []
order_items = []

order_id = 1
for order_id in range(1, num_orders+1):
    cust_id = random.randint(1, num_customers)
    # случайная дата в 2023 году
    date = datetime.date(2023, random.randint(1,12), random.randint(1,28)).isoformat()
    orders.append({"order_id": order_id, "customer_id": cust_id, "order_date": date})
    # сгенерируем 1-5 позиций для этого заказа
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        prod = random.choice(products)        # случайный товар из списка
        quantity = random.randint(1, 5)
        order_items.append({
            "order_id": order_id,
            "product_id": prod["product_id"],
            "quantity": quantity
        })

df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)
df_orders.to_csv("orders.csv", index=False)
df_order_items.to_csv("order_items.csv", index=False)
print("Созданы файлы orders.csv и order_items.csv")
print("Orders:", df_orders.shape, " Order Items:", df_order_items.shape)