import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import psycopg2
import psycopg2.extras
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


#Extract 

def _extract():
    response = requests.get('https://www.imdb.com/chart/moviemeter')

    soup = BeautifulSoup(response.content, 'html.parser')

    movie_table = soup.find('table', class_='chart full-width').tbody

    movies = []
    for movie_row in movie_table.find_all('tr'):
        try:
            movie_title = movie_row.find('td', class_='titleColumn').a.text
            movie_rating = movie_row.find('td', class_='ratingColumn imdbRating').strong.text
        except AttributeError:
            movie_title = movie_row.find('td', class_='titleColumn').a.text
            movie_rating = ''

        movie = {
            'title': movie_title,
            'rating': movie_rating
        }
        movies.append(movie)

    return movies


#Transform
def _transform(ti):
    movies=ti.xcom_pull(task_ids='Extract')
    cleaned_movies = []
    for movie in movies:
        if movie['rating']:
            rating = float(movie['rating'].replace(',', '.'))
            cleaned_movies.append({
                'title': movie['title'],
                'rating': rating
            })
    return cleaned_movies

#Load 
def _load(ti):
    movies=ti.xcom_pull(task_ids='Transform')
    hostname = "host.docker.internal"
    database = "ETL"
    username = "airflow"
    pwd = "airflow"
    port_id = 5432
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    ) 
    print(movies)
    cursor = conn.cursor()
    for movie in movies:
        cursor.execute(
            "INSERT INTO movie_ratings (title, rating) VALUES (%s, %s);",
            (movie['title'], movie['rating'])
        )
    conn.commit()
    cursor.close()
    conn.close()



default_args={
    'owner':'mbahraoui',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}


with DAG(
    default_args=default_args,
    dag_id='ETL_DAG_final_01',
    description='ETL dag',
    start_date=datetime(2023,3,24),
    schedule_interval='@weekly'
) as dag:
    task1=PythonOperator(
        task_id='Extract',
        python_callable=_extract
    )

    task2=PythonOperator(
        task_id='Transform',
        python_callable=_transform
    )

    task3=PythonOperator(
        task_id='Load',
        python_callable=_load
    )

    task1 >> task2 >> task3