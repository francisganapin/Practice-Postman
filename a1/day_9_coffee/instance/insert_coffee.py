import sqlite3
import csv


conn = sqlite3.connect('coffee_shop.db')
cursor = conn.cursor()





with open('coffee_list.csv',newline='',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('INSERT INTO coffee (name, price) VALUES (?, ?)', (row['name'], float(row['price'])))



conn.commit()
conn.close()


print("Data inserted was successfulll")