from pyspark.sql import SparkSession, functions as F, types as T
import os
os.environ["PYSPARK_PYTHON"] = "/opt/conda/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/opt/conda/bin/python"

HDFS_RAW_BASE = "hdfs://namenode:8020/data/raw/currency_rates"
HDFS_ODS      = "hdfs://namenode:8020/data/ods/currency_rates"

spark = (
    SparkSession.builder
    .appName("current_rates_ods")
    .config("spark.pyspark.python", "/opt/conda/bin/python")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .config("spark.yarn.appMasterEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .enableHiveSupport()
    .getOrCreate()
)

df_raw = spark.read.parquet(f"{HDFS_RAW_BASE}/")
if df_raw.rdd.isEmpty():
    print("ODS: RAW пуст, нечего обрабатывать.")
    spark.stop()
    raise SystemExit(0)

schema = T.StructType([
    T.StructField("rates", T.MapType(T.StringType(), T.DoubleType()), True)
])

df_ods = (
    df_raw
    .withColumn("parsed", F.from_json("payload_json", schema))
    .select("provider","as_of_date","collected_at","base",
            F.explode_outer("parsed.rates").alias("quote","price"))
)

(
    df_ods.write
    .mode("overwrite")
    .format("parquet")
    .partitionBy("as_of_date")
    .option("path", HDFS_ODS)
    .saveAsTable("ods.currency_rates")
)

print("ODS записан в HDFS:", HDFS_ODS)
spark.stop()