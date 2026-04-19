from pyspark.sql import SparkSession, functions as F
import os
os.environ["PYSPARK_PYTHON"] = "/opt/conda/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/opt/conda/bin/python"

HDFS_RAW_BASE = "hdfs://namenode:8020/data/raw/currency_rates"
HDFS_ODS      = "hdfs://namenode:8020/data/ods/currency_rates"
HDFS_MART = "hdfs://namenode:8020/data/mart/currency_rates"
spark = (
    SparkSession.builder
    .appName("fx_ods_hdfs_parquet_simple")
    .master("yarn")
    .config("spark.submit.deployMode", "client")
    .config("spark.pyspark.python", "/opt/conda/bin/python")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .config("spark.yarn.appMasterEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .enableHiveSupport()
    .getOrCreate()
)

df_ods = spark.read.parquet(HDFS_ODS)
if df_ods.rdd.isEmpty():
    print("MART: ODS пуст, нечего агрегировать.")
    spark.stop()
    raise SystemExit(0)

df_mart = (
    df_ods
    .withColumn("hour", F.date_format(F.col("collected_at"), "HH"))
    .groupBy("as_of_date","provider","base","quote","hour")
    .agg(
        F.count(F.lit(1)).alias("cnt"),
        F.avg("price").alias("avg_price"),
        F.min("price").alias("min_price"),
        F.max("price").alias("max_price"),
    )
)

(
    df_mart.write.mode("overwrite")
    .format("parquet")
    .partitionBy("as_of_date")
    .option("path", HDFS_MART)
    .saveAsTable("dm.currency_rates")
)

print("MART записан в HDFS:", HDFS_MART)
spark.read.parquet(HDFS_MART).orderBy(F.col("as_of_date").desc(), F.col("hour").desc()).show(20, truncate=False)
spark.stop()