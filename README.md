# Spark

* Cài đặt môi trường:

```
    pip3 install -r requirements.txt
```

* Chạy Spark:

```
    podman compose up -d
```
* Chạy application bằng spark-submit
```
    podman exec -it spark-master bash 
    spark-submit --jars mysql-connector-j-9.2.0.jar main.py
```
Or
```
     podman exec -i spark-master bash -c "cd scripts && spark-submit --jars mysql-connector-j-9.2.0.jar main.py"
```
* Spark UI : localhost:8080
* Spark History : localhost:18080