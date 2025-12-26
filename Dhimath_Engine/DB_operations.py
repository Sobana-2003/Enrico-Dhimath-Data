import pandas as pd
import psycopg2 as psql

from sqlalchemy import create_engine, sql

def get_connection_string(db_type, username, password, host, port, database):
    if db_type == "Postgresql":
        conn_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    elif db_type == "MySQL":
        conn_string = f"mysql://{username}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    return conn_string

def extract_tables(conn_string, schema):
    engine = create_engine(conn_string)
    with engine.connect() as conn:
        query = sql.text(f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = :schema
            AND table_type = 'BASE TABLE';
        """)
        result = conn.execute(query.params(schema=schema))
        tables = [row[0] for row in result]
    return tables

def create_views(tables, conn_string, schema):
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    views = []
    for table in tables:
        safe_table = table.lower()
        view_name = f"{safe_table}_view"
        
        sql_query = f"""
            CREATE OR REPLACE VIEW {schema}.{view_name} AS 
            (SELECT * FROM {schema}.{safe_table})
        """
        
        cursor.execute(sql_query)
        views.append(view_name)
    cursor.close()
    conn.close()
    return views

def load_table_data(conn_string, schema_name, table_name):
    engine = create_engine(conn_string)
    query = f"SELECT * FROM {schema_name}.{table_name}"
    df = pd.read_sql(query, engine)
    return df

def table_metadata(conn_string, table_name):
    engine = create_engine(conn_string)
    query = sql.text(f"""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_name = :table
                """)
    df = pd.read_sql(query, engine, params={"table": table_name})
    return df

def get_create_scripts(tables, conn_string, schema):
    engine = create_engine(conn_string)
    create_scripts = {}
    with engine.connect() as conn:
        for table in tables:
            column_query = sql.text("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = :schema
                AND table_name = :table
                ORDER BY ordinal_position;
            """)

            pk_query = sql.text("""
                SELECT c.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.constraint_column_usage AS ccu 
                USING (constraint_schema, constraint_name)
                JOIN information_schema.columns AS c 
                ON c.table_schema = tc.constraint_schema
                AND tc.table_name = c.table_name 
                AND ccu.column_name = c.column_name
                WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = :schema
                AND tc.table_name = :table;
            """)
            columns = conn.execute(column_query, {"schema": schema, "table": table}).fetchall()
            pk_columns = [pk[0] for pk in conn.execute(pk_query, {"schema": schema, "table": table}).fetchall()]
            create_script = f'CREATE TABLE {schema}.{table} (\n'
            column_definitions = []
            for col in columns:
                col_name, data_type, max_length, nullable, default = col
                definition = f"    {col_name} {data_type}"
                if max_length is not None:
                    definition += f"({max_length})"
                if nullable == 'NO':
                    definition += " NOT NULL"
                if default is not None:
                    definition += f" DEFAULT {default}"
                column_definitions.append(definition)
            if pk_columns:
                pk_constraint = f"    CONSTRAINT {table}_pkey PRIMARY KEY ({', '.join(pk_columns)})"
                column_definitions.append(pk_constraint)
            create_script += ',\n'.join(column_definitions)
            create_script += '\n);'
            create_scripts[table] = create_script   

    return create_scripts