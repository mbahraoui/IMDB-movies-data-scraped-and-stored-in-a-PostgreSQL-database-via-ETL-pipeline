FROM apache/airflow
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install pandas
RUN pip install psycopg2
