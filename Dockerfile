FROM amancevice/pandas

# create virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# INSTALL JAVA 11 for Spark
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# COPY MYSQL CONNECTOR JAR FOR JDBC connection
COPY mysql-connector-j-8.0.33.jar /usr/share/java/

# COPY INPUT DATA TO /input DIR
RUN mkdir /input
COPY input.csv /input

RUN mkdir /app
WORKDIR /app

# EXPOSE MYSQL PORTS
EXPOSE 3306
EXPOSE 3307

# DECLARE INPUT PATH ENV FOR PASSING TO THE SCRIPT
ENV input_path=/input
ENV mysql_host=localhost
ENV mysql_port=3306
ENV mysql_db=test
ENV mysql_table=PERSON
ENV db_user=root
ENV db_password=root

# Run the application:
COPY ingestion/spark/dataingestion.py .
CMD . /opt/venv/bin/activate &&  exec python /app/dataingestion.py --input_path=${input_path} --mysql_host=${mysql_host} --mysql_port=${mysql_port} --mysql_db=${mysql_db} --mysql_table=${mysql_table} --db_user=${db_user} --db_password=${db_password}
