from pyspark.sql import SparkSession

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
            "driver": jdbc_driver,
            "fetchsize" : "1000",
            "numPartitions" : "5",
        }
    )

    df_from_table.createOrReplaceTempView(df_table)

if __name__ == '__main__':
    # load data from table to dataframe
    create_dataframe("orders", "df_orders")
    create_dataframe("books", "df_books")

    # Save dataframe to table
    results = spark.sql('''
            select df_books.id, (df_books.title) as title, (df_books.type) as type, (df_books.stock) as stock, (df_books.price) as price,sum(df_orders.quality) as order_quantity,sum(df_orders.quality) * (price) as total_price
            from df_books
            inner join df_orders on df_books.id = df_orders.book_id
            WHERE ordered_at > '2024-01-01'
            GROUP BY df_books.id,df_books.title,df_books.type,df_books.stock,df_books.price
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