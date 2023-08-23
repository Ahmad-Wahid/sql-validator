
from __future__ import annotations

import click
import pandas as pd

from sql_validator.connect_db import connect_db
from sql_validator.validate_sql import validate_sql


@click.command()
@click.option("--query", type=str, help="SQL query to validate",)
@click.option(
    "--file", required=False, type=click.Path(exists=True), help="Path to file containing SQL queries",
)
@click.option(
    "--metadata",
    required=False,
    type=click.Path(exists=True),
    help="Path to the file/metadata used for validating the user queries results.",
)
@click.option("--show-data", default=False, type=bool, help="Print out the data",)
def commands(query: str, file, metadata, show_data: bool):
    conn = connect_db()
    try:
        if query:
            queries_df = pd.DataFrame([query], columns=["queries"])
        elif file:
            queries_df = load_file(file)
        else:
            click.echo("Please provide either --query or --file option.")
            return

        metadata_df = None
        if metadata:
            metadata_df = load_file(metadata)

        for row in range(queries_df.shape[0]):
            query = queries_df["queries"].iloc[row].strip()

            try:
                if query:
                    validate_sql(conn, query, metadata_query=metadata_df["queries"].iloc[row].strip(), show_data=show_data)
                else:
                    click.echo("Empty string is passed.")
            except IndexError as e:
                print("The following queries are not present in the metadata.")
                print(queries_df["queries"].iloc[row::])

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        conn.close()


def load_file(file: str):
    if ".xls" in file or ".xlsx" in file or ".xlsm" in file:
        queries_df = pd.read_excel(file)
        queries_df.index = queries_df.index+1
    elif ".csv" in file:
        queries_df = pd.read_csv(file)
        queries_df.index = queries_df.index + 1
    elif ".sql" in file:
        with open(file, "r") as f:
            queries_list = f.read().split(";")
            queries_df = pd.DataFrame(queries_list, columns=["queries"])
            queries_df.index = queries_df.index + 1
    return queries_df
