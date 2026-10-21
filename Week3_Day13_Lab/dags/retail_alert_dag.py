
from datetime import datetime
import logging

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.utils.email import send_email


def send_notification():
    logging.info("Starting email notification...")

    send_email(
        to=["namrotag.stocks@gmail.com"],
        subject="Airflow Email Notification Test",
        html_content="""
        <h2>Airflow Email Test</h2>
        <p>Hello!</p>
        <p>Your Airflow DAG ran successfully.</p>
        <p>This email was sent automatically by Apache Airflow.</p>
        """,
    )

    logging.info("Email notification sent successfully.")


with DAG(
    dag_id="email_dag",
    description="Send an email notification from Airflow",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["email", "notification"],
) as dag:

    email_task = PythonOperator(
        task_id="send_email",
        python_callable=send_notification,
    )

email_task