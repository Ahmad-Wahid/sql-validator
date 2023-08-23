from __future__ import annotations

import pandas as pd
import sqlparse
import psycopg2
import click


def format_query(query: str) -> str:
    formatted_query = sqlparse.format(
        query,
        strip_comments=True,
        # reindent=True,
        keyword_case="upper",
        reindent_aligned=True,
    )
    return formatted_query


def get_query_result(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [des[0] for des in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    return df


def validate_sql(connection: psycopg2, query: str, metadata_query: str = None, show_data: bool = False):
    cursor = connection.cursor()
    try:
        parsed = sqlparse.parse(query)
        if len(parsed) == 0:
            return False, "Invalid SQL: Empty query"
        formatted_query = format_query(query)

        if parsed[0].get_type() == "SELECT":
            query_result = get_query_result(cursor, query)
            click.secho(formatted_query, fg="green")

            if metadata_query:
                metadata_result = get_query_result(cursor, metadata_query)
                validation_status = validate_results(query_result, metadata_result, show_data)
                if validation_status:
                    click.secho("Data is valid.")
                else:
                    click.secho("Data is not valid, please check your query.")
            else:
                click.secho("Query is valid.")
        else:
            click.secho(formatted_query, fg="yellow")
            click.secho(
                "Invalid SQL: Only SELECT statements are supported for validation",
                fg="red",
            )
    except psycopg2.Error as e:
        formatted_query = format_query(query)
        click.secho(formatted_query, fg="yellow")
        click.secho(f"Validation error: {str(e)}", fg="red")
    finally:
        cursor.close()
    print("=" * 30)


def validate_results(query_result: pd.DataFrame, metadata_result: pd.DataFrame, show_data: bool):
    try:
        if all(query_result == metadata_result):
            if show_data:
                print(query_result)
            return True
    except ValueError as e:
        return False
