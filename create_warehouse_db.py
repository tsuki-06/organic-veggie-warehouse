import sqlite3
import os

# ตรวจสอบและลบไฟล์ฐานข้อมูลเดิมถ้ามีอยู่
if os.path.exists('warehouse.db'):
    os.remove('warehouse.db')
    print("ลบไฟล์ฐานข้อมูลเดิมเรียบร้อยแล้ว")

# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

# สร้าง SQL script สำหรับสร้างตารางและแทรกข้อมูล
sql_script = """
-- สร้างตาราง Farmers
CREATE TABLE Farmers (
    farmer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    address TEXT
);

-- สร้างตาราง Vegetables
CREATE TABLE Vegetables (
    veg_id INTEGER PRIMARY KEY,
    veg_name TEXT NOT NULL,
    category TEXT,
    storage_temp TEXT
);

-- สร้างตาราง Storage_Zones
CREATE TABLE Storage_Zones (
    zone_id INTEGER PRIMARY KEY,
    zone_name TEXT NOT NULL,
    capacity INTEGER
);

-- สร้างตาราง Stock_Batches
CREATE TABLE Stock_Batches (
    batch_id INTEGER PRIMARY KEY,
    veg_id INTEGER,
    farmer_id INTEGER,
    zone_id INTEGER,
    quantity INTEGER CHECK (quantity >= 0),
    receive_date DATE,
    expiry_date DATE,
    FOREIGN KEY (veg_id) REFERENCES Vegetables (veg_id),
    FOREIGN KEY (farmer_id) REFERENCES Farmers (farmer_id),
    FOREIGN KEY (zone_id) REFERENCES Storage_Zones (zone_id)
);

-- สร้างตาราง Transactions
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    batch_id INTEGER,
    transaction_type TEXT CHECK (transaction_type IN ('IN', 'OUT')),
    qty_changed INTEGER,
    transaction_date DATE,
    FOREIGN KEY (batch_id) REFERENCES Stock_Batches (batch_id)
);

-- แทรกข้อมูล Farmers (10 records)
INSERT INTO Farmers VALUES (1, 'นายสมชาย ใจดี', '0812345678', 'กรุงเทพฯ');
INSERT INTO Farmers VALUES (2, 'นางสาวสมหญิง รักดี', '0823456789', 'เชียงใหม่');
INSERT INTO Farmers VALUES (3, 'นายวิชัย สุขใจ', '0834567890', 'นครราชสีมา');
INSERT INTO Farmers VALUES (4, 'นางสาวกานต์ รักงาน', '0845678901', 'ขอนแก่น');
INSERT INTO Farmers VALUES (5, 'นายประสิทธิ์ ดีเลิศ', '0856789012', 'ภูเก็ต');
INSERT INTO Farmers VALUES (6, 'นางสาวนิด รักธรรม', '0867890123', 'สุราษฎร์ธานี');
INSERT INTO Farmers VALUES (7, 'นายชัยวัฒน์ มั่นคง', '0878901234', 'ชลบุรี');
INSERT INTO Farmers VALUES (8, 'นางสาวอรุณี สวยงาม', '0889012345', 'ระยอง');
INSERT INTO Farmers VALUES (9, 'นายธนวัฒน์ ร่ำรวย', '0890123456', 'ปทุมธานี');
INSERT INTO Farmers VALUES (10, 'นางสาวปราณี ใจเย็น', '0801234567', 'สมุทรปราการ');

-- แทรกข้อมูล Vegetables (10 records)
INSERT INTO Vegetables VALUES (1, 'ผักกาดหอม', 'ผักใบ', '4°C');
INSERT INTO Vegetables VALUES (2, 'มะเขือเทศ', 'ผักผล', '7°C');
INSERT INTO Vegetables VALUES (3, 'คะน้า', 'ผักใบ', '4°C');
INSERT INTO Vegetables VALUES (4, 'บร็อกโคลี', 'ผักดอก', '4°C');
INSERT INTO Vegetables VALUES (5, 'แครอท', 'ผักราก', '0°C');
INSERT INTO Vegetables VALUES (6, 'หัวหอมใหญ่', 'ผักหัว', '0°C');
INSERT INTO Vegetables VALUES (7, 'พริกหยวก', 'ผักผล', '7°C');
INSERT INTO Vegetables VALUES (8, 'แตงกวา', 'ผักผล', '10°C');
INSERT INTO Vegetables VALUES (9, 'ผักชี', 'ผักใบ', '4°C');
INSERT INTO Vegetables VALUES (10, 'กะหล่ำปลี', 'ผักดอก', '0°C');

-- แทรกข้อมูล Storage_Zones (10 records)
INSERT INTO Storage_Zones VALUES (1, 'โซน A', 1000);
INSERT INTO Storage_Zones VALUES (2, 'โซน B', 800);
INSERT INTO Storage_Zones VALUES (3, 'โซน C', 1200);
INSERT INTO Storage_Zones VALUES (4, 'โซน D', 900);
INSERT INTO Storage_Zones VALUES (5, 'โซน E', 1100);
INSERT INTO Storage_Zones VALUES (6, 'โซน F', 700);
INSERT INTO Storage_Zones VALUES (7, 'โซน G', 1300);
INSERT INTO Storage_Zones VALUES (8, 'โซน H', 600);
INSERT INTO Storage_Zones VALUES (9, 'โซน I', 1400);
INSERT INTO Storage_Zones VALUES (10, 'โซน J', 750);

-- แทรกข้อมูล Stock_Batches (10 records)
INSERT INTO Stock_Batches VALUES (1, 1, 1, 1, 100, '2023-01-01', '2023-01-10');
INSERT INTO Stock_Batches VALUES (2, 2, 2, 2, 200, '2023-01-02', '2023-01-12');
INSERT INTO Stock_Batches VALUES (3, 3, 3, 3, 150, '2023-01-03', '2023-01-13');
INSERT INTO Stock_Batches VALUES (4, 4, 4, 4, 120, '2023-01-04', '2023-01-14');
INSERT INTO Stock_Batches VALUES (5, 5, 5, 5, 180, '2023-01-05', '2023-01-15');
INSERT INTO Stock_Batches VALUES (6, 6, 6, 6, 90, '2023-01-06', '2023-01-16');
INSERT INTO Stock_Batches VALUES (7, 7, 7, 7, 210, '2023-01-07', '2023-01-17');
INSERT INTO Stock_Batches VALUES (8, 8, 8, 8, 160, '2023-01-08', '2023-01-18');
INSERT INTO Stock_Batches VALUES (9, 9, 9, 9, 140, '2023-01-09', '2023-01-19');
INSERT INTO Stock_Batches VALUES (10, 10, 10, 10, 170, '2023-01-10', '2023-01-20');

-- แทรกข้อมูล Transactions (10 records)
INSERT INTO Transactions VALUES (1, 1, 'IN', 100, '2023-01-01');
INSERT INTO Transactions VALUES (2, 2, 'IN', 200, '2023-01-02');
INSERT INTO Transactions VALUES (3, 3, 'IN', 150, '2023-01-03');
INSERT INTO Transactions VALUES (4, 4, 'IN', 120, '2023-01-04');
INSERT INTO Transactions VALUES (5, 5, 'IN', 180, '2023-01-05');
INSERT INTO Transactions VALUES (6, 6, 'OUT', 50, '2023-01-06');
INSERT INTO Transactions VALUES (7, 7, 'IN', 210, '2023-01-07');
INSERT INTO Transactions VALUES (8, 8, 'OUT', 30, '2023-01-08');
INSERT INTO Transactions VALUES (9, 9, 'IN', 140, '2023-01-09');
INSERT INTO Transactions VALUES (10, 10, 'OUT', 20, '2023-01-10');
"""

# รัน SQL script
cursor.executescript(sql_script)

# ยืนยันการเปลี่ยนแปลง
conn.commit()

# ปิดการเชื่อมต่อ
conn.close()

# แสดงข้อความสำเร็จ
print("ฐานข้อมูล warehouse.db ได้ถูกสร้างสำเร็จแล้ว!")