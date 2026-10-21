
from datetime import timedelta
import json
import logging
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from airflow.sdk import DAG
from airflow.exceptions import AirflowException
from airflow.providers.standard.operators.python import PythonOperator
from pendulum import datetime


API_URL = "https://imdb236.p.rapidapi.com/api/imdb/most-popular-tv"
API_HOST = "imdb236.p.rapidapi.com"

RAW_FILE = Path("/tmp/most_popular_tv.json")
TOP5_FILE = Path("/tmp/top_5_tv.json")


# TASK 1: Extract data from RapidAPI
def fetch_imdb_data():

    # Read credentials when the task executes
    rapidapi_key = os.environ.get("RAPIDAPI_KEY")

    if not rapidapi_key:
        raise AirflowException(
            "RAPIDAPI_KEY is missing from the Airflow environment."
        )

    request = Request(
        API_URL,
        headers={
            "x-rapidapi-host": API_HOST,
            "x-rapidapi-key": rapidapi_key,
            "User-Agent": "Mozilla/5.0",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=30) as response:
            status_code = response.status
            response_text = response.read().decode("utf-8")

    except HTTPError as error:
        error_body = error.read().decode(
            "utf-8", errors="replace"
        )

        raise AirflowException(
            f"IMDb API returned HTTP {error.code}: "
            f"{error_body[:500]}"
        ) from error

    except (URLError, TimeoutError) as error:
        raise AirflowException(
            f"Could not connect to IMDb API: {error}"
        ) from error

    logging.info("IMDb API returned HTTP %s", status_code)

    try:
        data = json.loads(response_text)

    except json.JSONDecodeError as error:
        raise AirflowException(
            "IMDb API did not return valid JSON."
        ) from error

    # Save the raw JSON response
    with RAW_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    logging.info("Raw response saved to %s", RAW_FILE)
    logging.info("Response type: %s", type(data).__name__)

    return str(RAW_FILE)


# TASK 2: Transform data and extract top five
def extract_top_5(ti):

    # Retrieve the file path from Task 1 using XCom
    raw_path = ti.xcom_pull(
        task_ids="fetch_most_popular_tv"
    )

    if not raw_path or not Path(raw_path).exists():
        raise AirflowException(
            f"Raw data file not found: {raw_path}"
        )

    with Path(raw_path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract the records
    if isinstance(data, list):
        shows = data

    elif isinstance(data, dict):
        shows = data.get("data", data.get("results", []))

    else:
        raise AirflowException(
            "Unexpected API response format."
        )

    if not isinstance(shows, list) or not shows:
        raise AirflowException(
            "No shows found. Inspect the raw JSON response."
        )

    valid_shows = [
        show for show in shows
        if isinstance(show, dict)
    ]

    if not valid_shows:
        raise AirflowException(
            "No valid TV show records found."
        )

    # Sort by rank only if the response provides it
    if all(show.get("rank") is not None for show in valid_shows):

        def get_rank(show):
            try:
                return int(show["rank"])
            except (ValueError, TypeError):
                return float("inf")

        top_5 = sorted(valid_shows, key=get_rank)[:5]

    else:
        logging.warning(
            "Rank field missing in some records. "
            "Preserving API response order."
        )
        top_5 = valid_shows[:5]

    # Save transformed results
    with TOP5_FILE.open("w", encoding="utf-8") as file:
        json.dump(top_5, file, indent=2)

    logging.info("Top five TV shows:")

    for show in top_5:
        logging.info(
            "Rank: %s | Title: %s | Year: %s",
            show.get("rank", "N/A"),
            show.get(
                "title",
                show.get("primaryTitle", "Unknown")
            ),
            show.get(
                "year",
                show.get("startYear", "N/A")
            ),
        )

    logging.info("Top-five results saved to %s", TOP5_FILE)

    return str(TOP5_FILE)


# DAG DEFINITION
with DAG(
    dag_id="imdb_tv_analysis_dag",
    description="Fetch popular IMDb TV shows and extract the top five",
    start_date=datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(seconds=15),
    },
    tags=["imdb", "api", "analysis"],
) as dag:

    fetch_data = PythonOperator(
        task_id="fetch_most_popular_tv",
        python_callable=fetch_imdb_data,
    )

    analyze_top_5 = PythonOperator(
        task_id="extract_top_5_shows",
        python_callable=extract_top_5,
    )

    fetch_data >> analyze_top_5

