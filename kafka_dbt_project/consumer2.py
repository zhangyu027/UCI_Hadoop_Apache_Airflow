"""Read sales events and profit data from Kafka and insert them into PostgreSQL."""

import json
import os

import psycopg2
from kafka import KafkaConsumer


CREATE_SALES_TABLE_SQL = """
create table if not exists raw_sales (
    user_id integer,
    event varchar(50),
    amount integer
);
"""

CREATE_PROFIT_TABLE_SQL = """
create table if not exists raw_profit_events (
    product_id integer,
    product_name varchar(100),
    category varchar(50),
    year integer,
    quantity integer,
    revenue decimal(10, 2),
    cost decimal(10, 2),
    profit decimal(10, 2),
    profit_margin decimal(5, 2)
);
"""

INSERT_SALES_SQL = """
insert into raw_sales (user_id, event, amount)
values (%s, %s, %s);
"""

INSERT_PROFIT_SQL = """
insert into raw_profit_events (product_id, product_name, category, year, quantity, revenue, cost, profit, profit_margin)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


def main() -> None:
    connection = psycopg2.connect(
        host="localhost",
        port=int(os.getenv("ANALYTICS_DB_PORT", "5433")),
        database="analytics",
        user="postgres",
        password="postgres",
    )
    cursor = connection.cursor()
    
    # Create tables
    cursor.execute(CREATE_SALES_TABLE_SQL)
    cursor.execute(CREATE_PROFIT_TABLE_SQL)
    connection.commit()
    print("Tables created successfully!")

    # Create consumer group to read all topics
    consumer = KafkaConsumer(
        "sales_topic",
        "profit_events",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="sales-profit-postgres-consumer",
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )

    print("Listening for Kafka messages... (Ctrl+C to stop)")
    for message in consumer:
        data = message.value
        topic = message.topic
        
        if topic == "sales_topic":
            print(f"Received sales event: {data}")
            cursor.execute(
                INSERT_SALES_SQL,
                (data["user_id"], data["event"], data["amount"]),
            )
        elif topic == "profit_events":
            print(f"Received profit event: {data}")
            cursor.execute(
                INSERT_PROFIT_SQL,
                (
                    data["product_id"],
                    data["product_name"],
                    data["category"],
                    data["year"],
                    data["quantity"],
                    data["revenue"],
                    data["cost"],
                    data["profit"],
                    data["profit_margin"],
                ),
            )
        
        connection.commit()


if __name__ == "__main__":
    main()
