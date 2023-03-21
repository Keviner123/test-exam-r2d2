from DAL.sqlite_dal import SQLiteDAL

db = SQLiteDAL('database.db')

db.execute_query('INSERT INTO token (value) VALUES (?)', ('a Doe',))

token = db.get_record('SELECT * FROM token WHERE id = 1')

pass
