import datetime as dt
import json
import time
import requests

from pyspark.sql import SparkSession, functions as F, types as T
import os
os.environ["PYSPARK_PYTHON"] = "/opt/conda/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/opt/conda/bin/python"

HDFS_RAW_BASE = "hdfs://namenode:8020/data/raw/currency_rates"
PROVIDER = "frankfurter"

BASES  = ["USD", "EUR"]
QUOTES = ["USD", "EUR"]
LAST_N_DAYS = 7


spark = (
    SparkSession.builder
    .appName("currency_rates_raw")
    .config("spark.pyspark.python", "/opt/conda/bin/python")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .config("spark.yarn.appMasterEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .getOrCreate()
)

schema = T.StructType([
    T.StructField("provider",     T.StringType(),  False),
    T.StructField("base",         T.StringType(),  False),
    T.StructField("as_of_date",   T.StringType(),  False),
    T.StructField("collected_at", T.StringType(),  False),
    T.StructField("payload_json", T.StringType(),  False),
])

rows = []
today = dt.date.today()

for offset in range(LAST_N_DAYS):
    the_day = today - dt.timedelta(days=offset)
    date_str = the_day.strftime("%Y-%m-%d")

    for base in BASES:

        to_list = [q for q in QUOTES if q.upper() != base.upper()]
        if not to_list:
            continue

        url = f"https://api.frankfurter.app/{date_str}"
        params = {"from": base, "to": ",".join(to_list)}
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        js = r.json()

        rates = js.get("rates") or {}
        filtered = {k: float(v) for k, v in rates.items() if k in QUOTES and k != base}
        if not filtered:
            continue

        collected_at = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append((
            PROVIDER,
            base,
            js.get("date"),
            collected_at,
            json.dumps({"rates": filtered}, ensure_ascii=False),
        ))

        time.sleep(0.05)


if not rows:
    print("RAW: провайдер не вернул данных.")
    spark.stop()
    raise SystemExit(0)

df = spark.createDataFrame(rows, schema=schema)

(
    df.repartition(1).write
      .mode("overwrite")
      .partitionBy("as_of_date")
      .parquet(HDFS_RAW_BASE)
)

print("RAW записан в HDFS:", HDFS_RAW_BASE)
spark.stop()