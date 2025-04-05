import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp

jdbc_url = "jdbc:mysql://host.docker.internal:4000/bookshop"
jdbc_user = "root"
jdbc_driver = "com.mysql.cj.jdbc.Driver"

spark = SparkSession.builder \
           .appName('BookExample') \
           .config("spark.jars", "mysql-connector-j-9.2.0.jar") \
           .getOrCreate()

def create_dataframe(table_name,df_table):
    df_from_table = spark.read.jdbc(
        url=jdbc_url,
        table=table_name,
        properties={
            "user": jdbc_user,
            "driver": jdbc_driver
        }
    )

    df_from_table.createOrReplaceTempView(df_table)
    print(table_name)

if __name__ == '__main__':
    # load data from table to dataframe
    create_dataframe("orders", "orders")
    create_dataframe("books", "books")

    # Save dataframe to table
    results = spark.sql('''select books.id, any_value(books.title), any_value(books.type), any_value(books.stock), any_value(books.price),sum(orders.quality) * any_value(price) as total_price
            from books
            inner join orders on books.id = orders.book_id
            WHERE ordered_at > '2024-01-01'
            GROUP BY books.id
            ORDER BY total_price DESC
    ''')
    results.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://host.docker.internal:3306/bookshop") \
        .option("dbtable","order_modify") \
        .option("user", "danhhnc") \
        .option("password", "danhhnc") \
        .option("driver", jdbc_driver) \
        .option("isolation","READ-UNCOMMITTED") \
        .mode("append") \
        .save()
    spark.stop()