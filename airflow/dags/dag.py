
from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

# Your existing dbt project and shared virtual environment
DBT_PROJECT_DIR = "/home/lenovo/projects/~"
DBT_BIN = "/home/lenovo/projects/~/.venv/bin/dbt"
DBT_PROFILES_DIR = "/home/lenovo/.dbt"

with DAG(
    dag_id="dbt_workflow",
    description="Orchestrate dbt transformations and tests on Snowflake",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "data_engineering",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["dbt", "snowflake", "data-engineering"],
) as dag:

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=(
            f"cd '{DBT_PROJECT_DIR}' && "
            f"'{DBT_BIN}' debug "
            f"--profiles-dir '{DBT_PROFILES_DIR}'"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd '{DBT_PROJECT_DIR}' && "
            f"'{DBT_BIN}' run "
            f"--profiles-dir '{DBT_PROFILES_DIR}'"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd '{DBT_PROJECT_DIR}' && "
            f"'{DBT_BIN}' test "
            f"--profiles-dir '{DBT_PROFILES_DIR}'"
        ),
    )

    dbt_debug >> dbt_run >> dbt_test
