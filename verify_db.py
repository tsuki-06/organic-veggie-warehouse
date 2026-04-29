import sqlite3

conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

# ดูรายชื่อตาราง
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('ตารางที่สร้างขึ้น:', [table[0] for table in tables])

# นับจำนวน records ในแต่ละตาราง
tables_list = ['Farmers', 'Vegetables', 'Storage_Zones', 'Stock_Batches', 'Transactions']
for table in tables_list:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'จำนวน {table}: {count} records')

conn.close()