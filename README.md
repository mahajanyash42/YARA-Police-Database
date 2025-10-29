# 🎓 University of Maryland – UMPD YARA Database  

## 📘 Project Overview  
The **UMPD YARA Database** is a Police Data Management System created as part of the DBMS project at the University of Maryland.  
It enables officers to record, manage, and retrieve information about incidents, arrests, and evidence through a Streamlit-based web interface connected to a SQL Server database.  
This project demonstrates complete end-to-end database design, implementation, and integration using Python and SQL Server.

---

## 🎯 Project Objectives  
- Design a normalized relational database in SQL Server  
- Develop a user-friendly Streamlit interface for CRUD operations  
- Automate data generation and ETL using Faker  
- Maintain referential integrity with primary and foreign keys  
- Enable real-time data interaction between UI and backend  

---

## 🧰 Technology Stack  
| Layer | Technology |
|:------|:------------|
| **Frontend** | Streamlit (Python) |
| **Backend** | SQL Server |
| **ETL / Seeding** | Python + Faker + pyodbc |
| **Language** | Python 3.x |
| **Schema** | YARA |
| **Platform** | Windows / WSL |

---

## 🧱 Database Schema  
The database contains **seven main tables** under the `YARA` schema:  
**Incident**, **Officer**, **Person**, **Evidence**, **Assign**, **Contain**, **Arrest**

### Relationships  
- One **Incident** can have many **Officers** through the **Assign** table  
- One **Incident** can have multiple **Evidence** records through the **Contain** table  
- One **Incident** can have multiple **Arrests** linking **Persons** and **Officers**  
All relationships are maintained using **foreign keys** with cascading updates.

---

## ⚙️ Implementation Steps  
1️⃣ Create a Python virtual environment and install required libraries such as Streamlit, Pandas, pyodbc, Faker, and python-dotenv.  
2️⃣ Configure the `.env` file with SQL Server details (Driver, Server Name, Database, and Trusted Connection).  
3️⃣ In SQL Server Management Studio (SSMS):  
 • Create the `YARA` schema  
 • Add all seven tables with appropriate primary and foreign keys  
 • Enforce referential integrity constraints  
4️⃣ Optionally, run the Python ETL script (`seed_yara.py`) to generate and insert sample data automatically.  
5️⃣ Launch the application in Streamlit and open it locally in your browser at **http://localhost:8501**.  

---

## 🖥️ System Workflow  
- Officers can enter, update, or delete records for incidents, persons, arrests, and evidence.  
- Streamlit communicates with SQL Server in real time using **pyodbc** connections.  
- Users can view, filter, and search linked data across tables.  
- The **Faker** library is used to generate large volumes of test data for performance and validation.  

---

## 📊 Example SQL Queries  

**1. Incidents per Officer**  
Select the OfficerID and count the number of incidents assigned to each officer from the Assign table.  

**2. Evidence linked to Incidents**  
Select each IncidentID and count the number of evidence items linked to it using a join between the Incident and Contain tables.  

**3. Most Common Arrest Charges**  
Group all arrests by the charge type and count how many times each charge occurs, ordering the results from highest to lowest.  

---

## 🧠 Learning Outcomes  
- Developed strong understanding of relational database design and normalization  
- Automated ETL and data generation workflows using Python  
- Built seamless integration between Streamlit UI and SQL Server backend  
- Improved skills in data querying, validation, and visualization  

---

## 🚀 Future Enhancements  
- Add authentication and access roles (Admin vs Officer)  
- Implement evidence image uploads and secure storage  
- Develop interactive analytics dashboards for trends and summaries  
- Add logging and audit tracking for user actions  
- Deploy the complete app using Docker containers  

---

## 👨‍💻 Author  
**Yash Mahajan**  
MS Information Systems – University of Maryland, College Park  
GitHub: [mahajanyash42](https://github.com/mahajanyash42)  
LinkedIn : https://www.linkedin.com/in/yashhmahajan/ 
Email : mahajanyash42@gmail.com
