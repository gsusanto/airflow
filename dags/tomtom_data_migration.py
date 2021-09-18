import argparse
from pathlib import Path

from model import Connection
import config

# Initialize Tomtom Table
def main(db_connection):
    Path(config.CSV_FILE_DIR).mkdir(parents=True, exist_ok=True)
    
    connection = Connection(db_connection)
    session = connection.get_session()
    session.execute('''CREATE TABLE IF NOT EXISTS tomtom (
    timestamp INT PRIMARY KEY,
    date_time TIMESTAMP, 
    traffic_index INT, 
    jams_count INT, 
    jams_length DECIMAL, 
    jams_delay DECIMAL, 
    traffic_index_weekago INT, 
    weekday VARCHAR(20))''')
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.connection)