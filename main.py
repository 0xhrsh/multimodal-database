import socket
from json.decoder import JSONDecodeError
import psycopg2
import json

INSERT = "INSERT INTO {} ({})\
     VALUES ({}) ON CONFLICT (id) DO NOTHING;"

UPDATE = "UPDATE {} SET {} WHERE id = '{}';"
READ = "SELECT * FROM PI;"


host = "192.168.1.69"
port = 8000
# todo


INFO_LIST = ['gender', 'age', 'name']
CITY_LIST = ['curr_city']
JSON_LIST = ['card_used', 'fingerprint_hash', 'phone_number']


def add_data_json(data, id):
    try:
        with open('jsons/{}.json'.format(id)) as f:
            curr_data = json.load(f)
    except FileNotFoundError:
        curr_data = {}

    for field in data:
        try:
            if data[field] not in curr_data[field]:
                curr_data[field].append(data[field])

        except KeyError:
            curr_data[field] = [data[field]]

    with open('jsons/{}.json'.format(id), 'w+') as f:
        json.dump(curr_data, f)

    return 'json file updates'


def add_data_psql(data, table, id):
    db = psycopg2.connect(database="google", user="rap",
                          password="rap@iitj", host="127.0.0.1", port="5432")

    names = ""
    values = ""
    updates = ""
    for field in data:
        names += field + ', '
        values += "'" + str(data[field]) + "',"
        updates += field + " = '" + str(data[field]) + "',"
    names += 'id'
    values += "'" + str(id) + "'"

    updates = updates[:-1]

    cur = db.cursor()
    cur.execute(INSERT.format(table, names, values))
    cur.execute(UPDATE.format(table, updates, id))
    db.commit()

    return "data added to table {}".format(table)


def handle_request(data):
    try:
        data = json.loads(data)

    except JSONDecodeError:
        print("json error")
        return

    id = data["id"]

    info_table = {}
    city_table = {}
    json_table = {}

    for field in data:
        if field in INFO_LIST:
            info_table[field] = data[field]
        elif field in CITY_LIST:
            city_table[field] = data[field]
        else:
            json_table[field] = data[field]

    ret = ""

    if info_table:
        ret += add_data_psql(info_table, "info", id) + "\n"
    if city_table:
        ret += add_data_psql(city_table, "city", id) + "\n"

    if json_table:
        ret += add_data_json(json_table, id) + "\n"

    return ret


def startServer():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    print("Listening at", s.getsockname())

    while True:
        conn, addr = s.accept()
        print("Connected by", addr)

        try:
            data = conn.recv(1024)
        except socket.error:
            conn.close()
            return

        response = handle_request(data.decode('utf8'))
        conn.sendall(response.encode('utf8'))
        conn.close()

    return


def main():
    startServer()
    return


if __name__ == '__main__':
    main()
