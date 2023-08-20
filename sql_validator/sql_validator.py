import sqlparse
import psycopg2
import click
from colored import fg
import sys


def format_query(query: str) -> str:
    formatted_query = sqlparse.format(
        query,
        strip_comments=True,
        eindent=True,
        keyword_case="upper",
        indent_columns=True,
    )
    return formatted_query


def validate_sql(connection: psycopg2, query: str):
    cursor = connection.cursor()
    try:
        parsed = sqlparse.parse(query)
        if len(parsed) == 0:

            return False, "Invalid SQL: Empty query"
        formatted_query = format_query(query)

        if parsed[0].get_type() == "SELECT":
            cursor.execute(formatted_query)
            result = cursor.fetchall()
            click.secho(formatted_query, fg="green")
            click.secho("Query is valid.")
        else:
            click.secho(formatted_query, fg="yellow")
            click.secho("Invalid SQL: Only SELECT statements are supported for validation", fg="red")
    except psycopg2.Error as e:
        formatted_query = format_query(query)
        click.secho(formatted_query, fg="yellow")
        click.secho(f"Validation error: {str(e)}", fg="red")
    finally:
        cursor.close()
    print("="*30)
