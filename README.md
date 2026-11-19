# Snowflake dbt Project

A dbt project that transforms raw customer, order, order-item, and product data in Snowflake into staging views and a daily order revenue mart. An Airflow DAG is included to run dbt debug, build, and test steps on a daily schedule.

## Project structure

- `models/staging/` - views that select and rename columns from the raw Snowflake tables.
- `models/marts/` - the `fct_daily_order_revenue` table, grouped by order date and order.
- `models/staging/sources.yml` - declares the raw source tables in `FINANCE_DB.RAW`.
- `tests/` - dbt data quality tests for order statuses and customer IDs.
- `airflow/dags/dag.py` - daily Airflow workflow for dbt.
- `data/` - synthetic example CSV data for loading into Snowflake; dbt does not load these files automatically.

## Requirements

- Python 3.10 or newer
- dbt Core and the `dbt-snowflake` adapter
- Access to a Snowflake account with the raw tables `CUSTOMERS`, `ORDERS`, `ORDER_ITEMS`, and `PRODUCTS` in `FINANCE_DB.RAW`

Install dbt and the Snowflake adapter in your Python environment:

```shell
python -m pip install dbt-snowflake
```

## Configure Snowflake

Create `~/.dbt/profiles.yml` (on Windows, `%USERPROFILE%\.dbt\profiles.yml`) with credentials and connection details for your account. Do not commit this file or credentials to the repository.

```yaml
snowflake_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: your_account_identifier
      user: your_username
      password: your_password
      role: your_role
      database: FINANCE_DB
      warehouse: your_warehouse
      schema: RAW
      threads: 4
```

Use an appropriate authentication method for your environment. The profile name must remain `snowflake_project` to match `dbt_project.yml`. The source definitions expect the raw tables to be in the `FINANCE_DB.RAW` schema.

## Run dbt

From the project directory:

```shell
dbt debug
dbt run
dbt test
```

Staging models are materialized as views and mart models as tables. The included tests check that order statuses use the accepted values and that `stg_customers.customer_id` is unique.

## Airflow

The DAG is in `airflow/dags/dag.py`. Before using it, update `DBT_PROJECT_DIR`, `DBT_BIN`, and `DBT_PROFILES_DIR` in that file to paths available to your Airflow worker. The worker must have dbt, the Snowflake profile, and access to the project. The DAG runs `dbt debug`, then `dbt run`, then `dbt test` daily.
