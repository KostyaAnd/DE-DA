#!/usr/bin/env python3

import pyspark.sql
from pyspark.sql import functions as F

# Задаём параметры
topic_in = "name_surname_lab03_tutorial_in"
kafka_bootstrap = "10.10.10.10:6667"
app_name = "Lab03RollMyOwnKafkacat"

#######################################

# Поверхностно проверяем что параметры изменялись
assert not topic_in.startswith("name_surname")
assert not kafka_bootstrap.startswith("10.10.10.10")

# Создаём спарк контекст
spark = pyspark.sql.SparkSession.builder.appName(app_name).getOrCreate()
spark.sparkContext.setLogLevel('WARN')

# Считываем сообщения из кафки
kafka_df = (
    spark.readStream.format("kafka")
    .option("group.id", "some-group-id-just-in-case")
    .option("checkpointLocation", "/tmp/checkpoint-read-super-simple")
    .option("kafka.bootstrap.servers", kafka_bootstrap)
    .option("subscribe", topic_in)
    .option("startingOffsets", "latest")
    .load()
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
)

query = kafka_df.writeStream.format("console").outputMode("append").trigger(processingTime='5 seconds').start()
query.awaitTermination()
