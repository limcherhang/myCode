# 使用 Ubuntu 22.04 作為基礎映像
FROM ubuntu:22.04

# 安裝必要的套件
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    pkg-config \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 設定環境變數
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient -lpthread -lz -lm -lrt -latomic -lssl -lcrypto -ldl"

# 安裝 Python 相關套件
RUN pip3 install \
    pymysql \
    pymongo \
    apache-airflow \
    apache-airflow[mysql]

# 執行 Airflow 初始化
RUN airflow db init

# 定義工作目錄
WORKDIR /usr/src/app

# 預設指令
CMD ["bash"]