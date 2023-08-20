import sqlparse
import psycopg2
import click
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

def print_results(is_valid, validation_result):
    if is_valid:
        click.echo("Query is valid.")
        print("=" * 20)
        # if validation_result:
        #     click.echo("Query result:")
        #     for row in validation_result:
        #         click.echo(row)
    else:
        print("Query is not valid.", file=sys.stderr)
        click.secho(
            f"Validation error: {validation_result}",
            file=sys.stderr,
            fg="red",
        )
        print("=" * 20)


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
            print_results(True, result)
        else:
            click.secho(formatted_query, fg="yellow")
            print_results(False, "Invalid SQL: Only SELECT statements are supported for validation")
    except psycopg2.Error as e:
        formatted_query = format_query(query)
        click.secho(formatted_query, fg="yellow")
        print_results(False, str(e))
    finally:
        cursor.close()

