from schemas import \
    role as sql_role_schema, \
    status as sql_status_schema, \
    user as sql_user_schema, \
    attendance as sql_attendance_schema

import os
from os.path import join, exists
import sqlite3
from sqlite3 import Cursor
import pandas as pd

def create_table(c: Cursor,
                 sql_cfg: dict,
                 schema: str) -> None:
    c.execute(schema)
    print(f'{schema} created')
    schema_name = schema.split()[2].lower()
    load_sample_data(c, schema_name)

def load_sample_data(c: Cursor,
                     sql_cfg: dict,
                     schema_name: str) -> None:
    data_path = join(sql_cfg.sample_data, f'{schema_name}.csv')
    if exists(data_path):
        data = pd.read_csv(data_path, index_col=False)
        data.to_sql(schema_name, c, if_exists='append', index=False)
        print(f'{schema_name} loaded {len(data)} rows')
    else:
        print(f'{data_path} not found')


def setup_sql(config: dict):
    sql_cfg = config['SQLDatabase']
    os.makedirs(sql_cfg.persistence_data_path, exist_ok=True)
    conn = sqlite3.connect(join(sql_cfg.persistence_data_path, sql_cfg.filename))
    c = conn.cursor()
    create_table(c, sql_role_schema)
    create_table(c, sql_status_schema)
    create_table(c, sql_user_schema)
    create_table(c, sql_attendance_schema)
    conn.commit()
