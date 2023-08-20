import sqlparse
import psycopg2
import click
from colored import fg
import sys


def format_query(query):
    formatted_query = sqlparse.format(
        query,
        strip_comments=True,
        eindent=True,
        keyword_case="upper",
        indent_columns=True,
    )
    return formatted_query

def print_results(is_valid=False, error_msg=None):
    if is_valid:
        print("Query is valid.")
    else:
        color = fg('red')
        print("Query is not valid.",)
        print(color + f"Validation error: {error_msg}")
    color = fg('white')
    print(color + "=" * 20)


def validate_sql(connection, query):
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
            click.secho("Valiation error: Invalid SQL: Only SELECT statements are supported for validation", fg="red")
    except psycopg2.Error as e:
        formatted_query = format_query(query)
        click.secho(formatted_query, fg="yellow")
        click.secho(f"Validation error: {str(e)}", fg="red")
    finally:
        cursor.close()
    print("="*30)
