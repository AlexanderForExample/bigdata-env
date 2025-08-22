import os, json, random, time
from datetime import datetime, timedelta
from pathlib import Path

PG_HOST = os.getenv("PG_HOST", "postgres-tgt")
PG_DB   = os.getenv("PG_DB",   "postgres")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PWD  = os.getenv("PG_PWD",  "postgres")
PG_PORT = int(os.getenv("PG_PORT", "5432"))

N_PRODUCTS  = 10_000
N_USERS     = 100_000
N_ORDERS    = 120_000
JSON_CHUNK  = 10_000
BATCH_SIZE  = 50_000

OUT_DIR = Path("/tmp/orders_json"); OUT_DIR.mkdir(parents=True, exist_ok=True)
CITIES  = ["Moscow"]*40 + ["SPb"]*25 + ["Kazan"]*10 + ["Novosibirsk"]*10 + ["Other"]*15
CATS    = [f"Category_{i}" for i in range(100)]

def gen_products():
    for pid in range(N_PRODUCTS):
        yield (pid, f"Product_{pid}", random.choice(CATS))

def gen_users():
    for uid in range(N_USERS):
        yield (uid, random.choice(CITIES))

def gen_order_docs():
    base = datetime.utcnow().date() - timedelta(days=29)
    for oid in range(N_ORDERS):
        dt = base + timedelta(days=random.randint(0, 29))
        ts = datetime.combine(dt, datetime.min.time()) + timedelta(seconds=random.randint(0, 86399))
        user_id = random.randint(0, N_USERS-1)
        items_cnt = max(1, min(5, int(random.gauss(3, 1))))
        items = []
        for _ in range(items_cnt):
            pid  = random.randint(0, N_PRODUCTS-1)
            qty  = random.randint(1, 5)
            price = round(random.uniform(5.0, 200.0), 2)
            items.append({"product_id": pid, "qty": qty, "price": price})
        yield {
            "order_id": oid,
            "order_ts": ts.isoformat() + "Z",
            "user": {"user_id": user_id, "city": random.choice(CITIES)},
            "items": items,
            "dt": dt.isoformat()
        }

def write_json_files():
    buf, idx, total = [], 0, 0
    t0 = time.time()
    for doc in gen_order_docs():
        buf.append(json.dumps(doc, ensure_ascii=False))
        if len(buf) >= JSON_CHUNK:
            (OUT_DIR / f"orders_{idx:05d}.json").write_text("\n".join(buf), encoding="utf-8")
            total += len(buf); buf.clear(); idx += 1
    if buf:
        (OUT_DIR / f"orders_{idx:05d}.json").write_text("\n".join(buf), encoding="utf-8")
        total += len(buf)
    print(f"[JSON] wrote {total} orders into {idx+1} files at {OUT_DIR} in {time.time()-t0:.1f}s")

def load_postgres():
    import psycopg2
    from psycopg2.extras import execute_values
    conn = psycopg2.connect(host="localhost", port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PWD)
    conn.autocommit = True; cur = conn.cursor()

    # DDL
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
        product_id INT PRIMARY KEY, name TEXT, category TEXT);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT PRIMARY KEY, city TEXT);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        order_id BIGINT, item_id INT, user_id BIGINT,
        product_id INT, qty INT, price NUMERIC(10,2),
        amount NUMERIC(12,2), ts TIMESTAMP, dt DATE);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS orders_json(
        id SERIAL PRIMARY KEY, order_data JSONB);""")

    # очистка
    cur.execute("TRUNCATE TABLE products;")
    cur.execute("TRUNCATE TABLE users;")
    cur.execute("TRUNCATE TABLE orders;")
    cur.execute("TRUNCATE TABLE orders_json;")

    # products
    prod = list(gen_products())
    execute_values(cur, "INSERT INTO products(product_id,name,category) VALUES %s", prod, page_size=10_000)
    print(f"[PG] products: {len(prod)}")

    # users
    usr = list(gen_users())
    execute_values(cur, "INSERT INTO users(user_id,city) VALUES %s", usr, page_size=10_000)
    print(f"[PG] users: {len(usr)}")

    # orders + orders_json
    t0 = time.time(); items_batch = []; json_batch = []; total_items = total_orders = 0
    for doc in gen_order_docs():
        json_batch.append((json.dumps(doc),))
        for i, it in enumerate(doc["items"]):
            amt = round(it["qty"] * it["price"], 2)
            items_batch.append((doc["order_id"], i, doc["user"]["user_id"], it["product_id"],
                                it["qty"], it["price"], amt,
                                doc["order_ts"].replace("Z","").replace("T"," "),
                                doc["dt"]))
        if len(items_batch) >= BATCH_SIZE:
            execute_values(cur, """INSERT INTO orders(order_id,item_id,user_id,product_id,qty,price,amount,ts,dt)
                                   VALUES %s""", items_batch, page_size=BATCH_SIZE)
            total_items += len(items_batch); items_batch.clear()
        if len(json_batch) >= BATCH_SIZE:
            execute_values(cur, "INSERT INTO orders_json(order_data) VALUES %s", json_batch, page_size=BATCH_SIZE)
            total_orders += len(json_batch); json_batch.clear()

    if items_batch:
        execute_values(cur, """INSERT INTO orders(order_id,item_id,user_id,product_id,qty,price,amount,ts,dt)
                               VALUES %s""", items_batch, page_size=BATCH_SIZE)
        total_items += len(items_batch)
    if json_batch:
        execute_values(cur, "INSERT INTO orders_json(order_data) VALUES %s", json_batch, page_size=BATCH_SIZE)
        total_orders += len(json_batch)

    print(f"[PG] orders rows: {total_items}; orders_json docs: {total_orders} in {time.time()-t0:.1f}s")
    # индексы под демо
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_dt  ON orders(dt);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_pid ON orders(product_id);")
    cur.close(); conn.close()

if __name__ == "__main__":
    write_json_files()
    load_postgres()
    print("Done.")
