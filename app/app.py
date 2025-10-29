import streamlit as st
import pandas as pd
import pyodbc
import datetime as dt

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="UMPD YARA Police Database", layout="wide")
st.title("University of Maryland Police Department – YARA Database")

# ----------------- DATABASE CONNECTION -----------------
DRIVER = "{ODBC Driver 17 for SQL Server}"
CONN_STR = (
    f"DRIVER={DRIVER};"
    f"SERVER=localhost;"  # Replace if you use a named instance like "localhost\\SQLEXPRESS"
    f"DATABASE=BUDT702_Project_0502_04;"
    f"Trusted_Connection=yes;"
)

def query_to_df(query, params=None):
    """Executes a SQL query and returns a pandas DataFrame"""
    with pyodbc.connect(CONN_STR) as conn:
        return pd.read_sql(query, conn, params=params)

def execute_query(query, params=None):
    """Executes INSERT/UPDATE/DELETE commands"""
    with pyodbc.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Section",
    ["Dashboard", "Add Incident", "Add Person", "Add Arrest", "Search Records"]
)

# ======================================================
# DASHBOARD PAGE
# ======================================================
if page == "Dashboard":
    st.header("Dashboard Overview")
    st.markdown("""
        <style>
        .block-container {
            max-width: 100% !important;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        div[data-testid="stDataFrame"] {
            margin-top: 1rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.08);
        }
        </style>
    """, unsafe_allow_html=True)
    # 🧱 Create equally spaced columns for buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("View All Incidents"):
            df = query_to_df("SELECT * FROM [YARA].[Incident] ORDER BY incidentId")
            # ✅ Bigger, scrollable box
            st.dataframe(df, use_container_width=True, width=2000)

    with col2:
        if st.button("View Officers"):
            df = query_to_df("SELECT * FROM [YARA].[Officer]")
            # ✅ Consistent look
            st.dataframe(df, use_container_width=True, height=600)

    with col3:
        if st.button("View Arrests"):
            df = query_to_df("""
                SELECT a.arrestId, a.arrestDate, a.arrestLocation, a.arrestStatus, p.personName
                FROM [YARA].[Arrest] a
                JOIN [YARA].[Person] p ON a.personSSN = p.personSSN
                ORDER BY a.arrestDate DESC
            """)
            # ✅ Consistent size for all dashboards
            st.dataframe(df, use_container_width=True, height=600)




# ======================================================
# ADD INCIDENT PAGE
# ======================================================
elif page == "Add Incident":
    st.header("Add New Incident")
    with st.form("add_incident_form"):
        iid = st.text_input("Incident ID (e.g., I010)")
        itype = st.text_input("Incident Type (e.g., Theft, Assault)")
        street = st.text_input("Street")
        city = st.text_input("City")
        zipc = st.text_input("ZIP Code")
        status = st.selectbox("Status", ["Open", "Closed", "Under Review"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not all([iid, itype, street, city, zipc]):
            st.warning("Please fill all fields.")
        else:
            try:
                execute_query("""
                    INSERT INTO [YARA].[Incident]
                    (incidentId, incidentType, incidentStreet, incidentCity, incidentZip, incidentStatus, incidentDate)
                    VALUES (?, ?, ?, ?, ?, ?, GETDATE())
                """, (iid, itype, street, city, zipc, status))
                st.success(f"Incident {iid} added successfully.")
            except Exception as e:
                st.error("Failed to insert incident.")
                st.code(str(e))

# ======================================================
# ADD PERSON PAGE
# ======================================================
elif page == "Add Person":
    st.header("Add New Person")
    with st.form("add_person_form"):
        ssn = st.text_input("Person SSN (e.g., P10000001)")
        name = st.text_input("Full Name")
        dob = st.date_input(
            "Date of Birth",
            value=dt.date(2000, 1, 1),                # default date shown
            min_value=dt.date(1950, 1, 1),            # earliest selectable date
            max_value=dt.date(2025, 12, 31)           # latest selectable date
)
        phone = st.text_input("Phone Number (10 digits)")
        submit = st.form_submit_button("Add Person")

    if submit:
        if not all([ssn, name, phone]):
            st.warning("Please fill all fields.")
        else:
            try:
                execute_query("""
                    INSERT INTO [YARA].[Person]
                    (personSSN, personName, personDOB, personPhoneNumber)
                    VALUES (?, ?, ?, ?)
                """, (ssn, name, dob, phone))
                st.success(f"Person {name} added successfully.")
            except Exception as e:
                st.error("Failed to add person.")
                st.code(str(e))

# ======================================================
# ADD ARREST PAGE
# ======================================================
elif page == "Add Arrest":
    st.header("Record New Arrest")
    with st.form("add_arrest_form"):
        aid = st.text_input("Arrest ID (e.g., A010)")
        personSSN = st.text_input("Person SSN (must exist in database)")
        adate = st.date_input("Arrest Date")
        atime = st.time_input("Arrest Time")
        location = st.text_input("Arrest Location")
        status = st.selectbox("Arrest Status", ["Arrested", "Released", "Under Investigation"])
        submit = st.form_submit_button("Submit Arrest")

    if submit:
        if not all([aid, personSSN, location]):
            st.warning("Please fill all required fields.")
        else:
            try:
                datetime_combined = f"{adate} {atime}"
                execute_query("""
                    INSERT INTO [YARA].[Arrest]
                    (arrestId, arrestDate, arrestLocation, arrestStatus, personSSN)
                    VALUES (?, ?, ?, ?, ?)
                """, (aid, datetime_combined, location, status, personSSN))
                st.success(f"Arrest {aid} recorded successfully.")
            except Exception as e:
                st.error("Failed to record arrest.")
                st.code(str(e))

# ======================================================
# SEARCH PAGE (SECURE & FUNCTIONAL)
# ======================================================
elif page == "Search Records":
    st.header("Search Records Across All Tables")
    st.write("You can search by ID, name, type, city, status, or keyword (case-insensitive).")

    search = st.text_input("Enter ID, name, or keyword")

    if st.button("Search"):
        if search.strip() == "":
            st.warning("Please enter a value to search.")
        else:
            try:
                search_param = f"%{search}%"  # safely add wildcards
                query = """
                SELECT 
                    'Incident' AS Category, 
                    incidentId AS Record_ID,
                    CONCAT('Type: ', incidentType, ' | City: ', incidentCity, ' | Status: ', incidentStatus) AS Details
                FROM [YARA].[Incident]
                WHERE 
                    incidentId LIKE ? OR
                    incidentType LIKE ? OR
                    incidentCity LIKE ? OR
                    incidentStatus LIKE ? OR
                    incidentStreet LIKE ? OR
                    incidentZip LIKE ?

                UNION ALL

                SELECT 
                    'Person' AS Category, 
                    personSSN AS Record_ID,
                    CONCAT('Name: ', personName, ' | Phone: ', personPhoneNumber) AS Details
                FROM [YARA].[Person]
                WHERE 
                    personSSN LIKE ? OR
                    personName LIKE ? OR
                    personPhoneNumber LIKE ?

                UNION ALL

                SELECT 
                    'Arrest' AS Category, 
                    arrestId AS Record_ID,
                    CONCAT('Location: ', arrestLocation, ' | Status: ', arrestStatus, ' | Date: ', CONVERT(VARCHAR(20), arrestDate, 120)) AS Details
                FROM [YARA].[Arrest]
                WHERE 
                    arrestId LIKE ? OR
                    arrestLocation LIKE ? OR
                    arrestStatus LIKE ? OR
                    CONVERT(VARCHAR(20), arrestDate, 120) LIKE ?
                """

                # repeat same parameter for all LIKEs
                params = [search_param]*6 + [search_param]*3 + [search_param]*4

                df = query_to_df(query, params)
                if df.empty:
                    st.info("No matching records found.")
                else:
                    st.success(f"Found {len(df)} matching record(s).")
                    st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error("Search failed.")
                st.code(str(e))
