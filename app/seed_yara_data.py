import pyodbc
from faker import Faker
import random
from datetime import datetime

# -------------------------------------
# 1️⃣ DATABASE CONNECTION
# -------------------------------------
# 🧠 Tip: Check your actual instance name from SSMS "Connect" window.
# Example: localhost\SQLEXPRESS or DESKTOP-XXXX\SQLEXPRESS

SERVER = r"YASH"  # 👈 Replace with your actual instance if needed
DATABASE = "BUDT702_Project_0502_04"

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    "Trusted_Connection=yes;"
)
cur = conn.cursor()
fake = Faker()

print(f"✅ Connected successfully to: {DATABASE}")

# -------------------------------------
# 2️⃣ VERIFY YARA SCHEMA AND TABLES
# -------------------------------------
cur.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA='YARA'
""")
tables = [row.TABLE_NAME for row in cur.fetchall()]
print("📋 Tables found in YARA schema:", tables)

required = {"Incident", "Officer", "Person", "Evidence", "Assign", "Contain", "Arrest"}
missing = required - set(tables)
if missing:
    raise Exception(f"❌ Missing tables in YARA schema: {missing}")

# -------------------------------------
# 3️⃣ INSERT FUNCTIONS (DEPENDENCY ORDER)
# -------------------------------------

# INCIDENTS
def insert_incidents(n=100):
    print("🚔 Inserting Incidents...")
    for i in range(1, n + 1):
        iid = f"I{100+i:03}"
        itype = random.choice(["Robbery", "Assault", "Fraud", "Theft", "Cybercrime", "Vandalism"])
        street = fake.street_name()[:20]
        city = random.choice(["Baltimore", "College Park", "Bethesda", "Rockville", "Silver Spring"])
        zipc = str(fake.postcode())[:10]
        status = random.choice(["Open", "Closed", "Under Review", "Pending"])
        date = fake.date_between(start_date="-90d", end_date="today")
        try:
            cur.execute("""
                INSERT INTO [YARA].[Incident] 
                (incidentId, incidentType, incidentStreet, incidentCity, incidentZip, incidentStatus, incidentDate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (iid, itype, street, city, zipc, status, date))
        except pyodbc.IntegrityError:
            print(f"⚠️ Skipped duplicate Incident ID: {iid}")
    conn.commit()
    print(f"✅ {n} Incidents inserted.")

# OFFICERS
def insert_officers(n=80):
    print("👮 Inserting Officers...")
    for i in range(1, n + 1):
        oid = f"O{100+i:03}"
        name = fake.name()[:20]
        phone = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        dob = fake.date_of_birth(minimum_age=25, maximum_age=60)
        hire = fake.date_between(start_date="-15y", end_date="-1y")
        try:
            cur.execute("""
                INSERT INTO [YARA].[Officer] 
                (officerId, officerName, officerPhoneNumber, officerDOB, officerHireDate)
                VALUES (?, ?, ?, ?, ?)
            """, (oid, name, phone, dob, hire))
        except pyodbc.IntegrityError:
            print(f"⚠️ Skipped duplicate Officer ID: {oid}")
    conn.commit()
    print(f"✅ {n} Officers inserted.")

# PERSONS
def insert_persons(n=150):
    print("👤 Inserting Persons...")
    for i in range(1, n + 1):
        pid = f"P{1000+i:05}"[:9]
        name = fake.name()[:20]
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        phone = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        try:
            cur.execute("""
                INSERT INTO [YARA].[Person]
                (personSSN, personName, personDOB, personPhoneNumber)
                VALUES (?, ?, ?, ?)
            """, (pid, name, dob, phone))
        except pyodbc.IntegrityError:
            print(f"⚠️ Skipped duplicate Person SSN: {pid}")
    conn.commit()
    print(f"✅ {n} Persons inserted.")

# EVIDENCE (depends on Incident)
def insert_evidence(n=100):
    print("🔍 Inserting Evidence...")
    cur.execute("SELECT incidentId FROM [YARA].[Incident]")
    incidents = [row.incidentId for row in cur.fetchall()]
    for i in range(1, n + 1):
        eid = f"E{100+i:03}"
        desc = random.choice(["Knife", "CCTV Footage", "DNA Sample", "Fingerprint", "Weapon", "Laptop"])
        loc = f"Locker{random.randint(1, 5)}"
        status = random.choice(["Sealed", "Open", "Stored"])
        inc = random.choice(incidents)
        try:
            cur.execute("""
                INSERT INTO [YARA].[Evidence]
                (evidenceId, evidenceDescription, evidenceStorageLocation, evidenceStatus, incidentId)
                VALUES (?, ?, ?, ?, ?)
            """, (eid, desc, loc, status, inc))
        except pyodbc.IntegrityError:
            print(f"⚠️ Skipped duplicate Evidence ID: {eid}")
    conn.commit()
    print(f"✅ {n} Evidence records inserted.")

# ASSIGN (depends on Incident + Officer)
def insert_assignments(n=100):
    print("🧾 Inserting Assignments...")
    cur.execute("SELECT incidentId FROM [YARA].[Incident]")
    incidents = [row.incidentId for row in cur.fetchall()]
    cur.execute("SELECT officerId FROM [YARA].[Officer]")
    officers = [row.officerId for row in cur.fetchall()]
    for _ in range(n):
        cur.execute("""
            INSERT INTO [YARA].[Assign] (officerId, incidentId, hoursSpent)
            VALUES (?, ?, ?)
        """, (random.choice(officers), random.choice(incidents), random.randint(10, 100)))
    conn.commit()
    print(f"✅ {n} Assignments inserted.")

# CONTAIN (depends on Incident + Person)
def insert_contain(n=100):
    print("🧩 Inserting Contain relationships...")
    cur.execute("SELECT incidentId FROM [YARA].[Incident]")
    incidents = [row.incidentId for row in cur.fetchall()]
    cur.execute("SELECT personSSN FROM [YARA].[Person]")
    persons = [row.personSSN for row in cur.fetchall()]
    for _ in range(n):
        cur.execute("""
            INSERT INTO [YARA].[Contain] (incidentId, personSSN, role)
            VALUES (?, ?, ?)
        """, (random.choice(incidents), random.choice(persons), random.choice(["Victim", "Suspect", "Witness"])))
    conn.commit()
    print(f"✅ {n} Contain records inserted.")

# ARREST (depends on Person)
def insert_arrests(n=100):
    print("🚨 Inserting Arrests...")
    cur.execute("SELECT personSSN FROM [YARA].[Person]")
    persons = [row.personSSN for row in cur.fetchall()]
    for i in range(1, n + 1):
        aid = f"A{100+i:03}"
        date = fake.date_time_between(start_date="-60d", end_date="now")
        loc = random.choice(["Downtown", "Uptown", "Suburb", "Station"])
        status = random.choice(["Arrested", "Released", "Under Investigation"])
        p = random.choice(persons)
        try:
            cur.execute("""
                INSERT INTO [YARA].[Arrest]
                (arrestId, arrestDate, arrestLocation, arrestStatus, personSSN)
                VALUES (?, ?, ?, ?, ?)
            """, (aid, date, loc, status, p))
        except pyodbc.IntegrityError:
            print(f"⚠️ Skipped duplicate Arrest ID: {aid}")
    conn.commit()
    print(f"✅ {n} Arrests inserted.")

# -------------------------------------
# 4️⃣ EXECUTION SEQUENCE
# -------------------------------------
insert_incidents()
insert_officers()
insert_persons()
insert_evidence()
insert_arrests()
insert_contain()


print("\n🎉 Database seeding completed successfully!")
conn.close()
