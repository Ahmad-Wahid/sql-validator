import click
import sys

from sql_validator.db_connector import connect_db
from sql_validator.sql_validator import validate_sql


@click.command()
@click.option("--query", type=str, help="SQL query to validate")
@click.option(
    "--file", type=click.Path(exists=True), help="Path to file containing SQL queries"
)
@click.option("--show-data", default=False, type=bool, help="Print out the data")
def main(query: str, file, show_data: bool):
    conn = connect_db()
    try:
        if query:
            queries = [query]
        elif file:
            with open(file, "r") as f:
                queries = f.read().split(";")
        else:
            click.echo("Please provide either --query or --file option.")
            return

        for sql_query in queries:
            if sql_query.strip():
                validate_sql(conn, sql_query.strip(), show_data=show_data)
            else:
                click.echo("Empty string is passed.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        conn.close()
