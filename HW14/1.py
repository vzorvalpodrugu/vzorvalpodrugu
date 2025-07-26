import  sqlite3
connection = sqlite3.connect("marvel_not_normal.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM MarvelCharacters")

# rows = cursor.fetchall()
# for row in rows:
#     print(row)