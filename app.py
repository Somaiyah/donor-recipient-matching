import streamlit as st
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text

# Create SQL
engine = create_engine("sqlite:///kidney_matching.db")

# Schema
with engine.connect() as connection:
    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS recipients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mrn TEXT,
        age INTEGER,
        bmi REAL,
        gender TEXT,
        blood_type TEXT,
        dol DATE,
        dod DATE,
        hd_pd TEXT,
        urgent TEXT,
        years_dialysis INTEGER,
        epts REAL,
        pra INTEGER,
        hla_a TEXT,
        hla_b TEXT,
        hla_cw TEXT,
        hla_dr TEXT,
        unacceptable_antigen TEXT
    )
    """))

    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        donor_hospital TEXT,
        city TEXT,
        do_admission DATE,
        admitting_dx TEXT,
        cause_of_death TEXT,
        age INTEGER,
        gender TEXT,
        ethnicity TEXT,
        weight REAL,
        bmi REAL,
        dm TEXT,
        htn TEXT,
        creat REAL,
        hcv TEXT,
        dcd TEXT,
        kdpi REAL,
        blood_type TEXT,
        hla_a TEXT,
        hla_b TEXT,
        hla_cw TEXT,
        hla_dr TEXT
    )
    """))

# Menu
st.sidebar.title("Kidney Matching System")
menu = st.sidebar.selectbox(
    "Menu", 
    [
        "Home", 
        "Add Recipient", 
        "Add Donor", 
        "Compatibility Check", 
        "View Results", 
        "Manage Data"
    ], 
    format_func=lambda x: {
        "Home": "🏠 Home",
        "Add Recipient": "👤 Add Recipient",
        "Add Donor": "🫀 Add Donor",
        "Compatibility Check": "🔍 Compatibility Check",
        "View Results": "📊 View Results",
        "Manage Data": "🛠️ Manage Data"
    }[x]
)

# Home
if menu == "Home":
    st.title("Kidney Matching System")
    st.write("Welcome to the Kidney Matching System!")
    st.write("This system matches kidney donors and recipients based on compatibility and priority scoring.")
    st.markdown("<hr style='border:2px solid teal'>", unsafe_allow_html=True)

# Add Recipient Page
elif menu == "Add Recipient":
    st.title("👤 Add Recipient")
    
    # Inputs outside the form for interactivity
    name = st.text_input("Full Name")
    mrn = st.text_input("Medical Record Number (MRN)")
    age = st.number_input("Age", min_value=0, step=1)
    bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, step=0.1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    blood_type = st.selectbox("Blood Type", ["O", "A", "B", "AB"])
    pra = st.slider("PRA% (Panel Reactive Antibodies)", 0, 100)
    dol = st.date_input("Date of Listing (DOL)")
    dod = st.date_input("Date of Dialysis Start (DOD)")
    hd_pd = st.selectbox("Type of Dialysis", ["Hemodialysis", "Peritoneal Dialysis"])
    urgent = st.selectbox("Urgency Level", ["Yes", "No"])

    # Calculate Years on Dialysis interactively
    today = datetime.now().date()
    if dod and dod <= today:
        years_dialysis = max((today - dod).days // 365, 0)  # Prevent negative values
    else:
        years_dialysis = 0

    st.write(f"Calculated Years on Dialysis: {years_dialysis}")

    # Other inputs
    epts = st.number_input("EPTS Score (Expected Post-Transplant Survival)", min_value=0.0, step=0.1)
    hla_a = st.text_input("HLA-A", placeholder="Enter HLA-A value")
    hla_b = st.text_input("HLA-B", placeholder="Enter HLA-B value")
    hla_cw = st.text_input("HLA-Cw", placeholder="Enter HLA-Cw value")
    hla_dr = st.text_input("HLA-DR", placeholder="Enter HLA-DR value")
    unacceptable_antigen = st.text_area("Unacceptable Antigens (comma-separated)")

    # Submit button
    if st.button("Submit"):
        try:
            with engine.connect() as connection:
                connection.execute(text("""
                INSERT INTO recipients (
                    name, mrn, age, bmi, gender, blood_type, pra, dol, dod, hd_pd,
                    urgent, years_dialysis, epts, hla_a, hla_b, hla_cw, hla_dr, unacceptable_antigen
                ) VALUES (
                    :name, :mrn, :age, :bmi, :gender, :blood_type, :pra, :dol, :dod, :hd_pd,
                    :urgent, :years_dialysis, :epts, :hla_a, :hla_b, :hla_cw, :hla_dr, :unacceptable_antigen
                )
                """), {
                    "name": name, "mrn": mrn, "age": age, "bmi": bmi, "gender": gender,
                    "blood_type": blood_type, "pra": pra, "dol": dol, "dod": dod,
                    "hd_pd": hd_pd, "urgent": urgent, "years_dialysis": years_dialysis,
                    "epts": epts, "hla_a": hla_a, "hla_b": hla_b, "hla_cw": hla_cw,
                    "hla_dr": hla_dr, "unacceptable_antigen": unacceptable_antigen
                })
            st.success("Recipient added successfully!")
        except Exception as e:
            st.error(f"Error adding recipient: {e}")

# Add Donor
elif menu == "Add Donor":
    st.title("🫀 Add Donor")
    
    # Inputs outside the form for interactivity
    name = st.text_input("Full Name")
    donor_hospital = st.text_input("Donor Hospital")
    city = st.text_input("City")
    do_admission = st.date_input("Date of Admission")
    admitting_dx = st.text_input("Admitting Diagnosis")
    cause_of_death = st.text_input("Cause of Death")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ethnicity = st.text_input("Ethnicity")
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, step=0.1)
    dm = st.selectbox("Diabetes Mellitus (DM)", ["Yes", "No"])
    htn = st.selectbox("Hypertension (HTN)", ["Yes", "No"])
    creat = st.number_input("Creatinine Level (mg/dL)", min_value=0.0, step=0.1)
    hcv = st.selectbox("Hepatitis C Virus (HCV)", ["Positive", "Negative"])
    dcd = st.selectbox("Donation after Cardiac Death (DCD)", ["Yes", "No"])

    # Dynamically calculate KDPI
    try:
        kdpi = (
            10 * age +
            2 * (1 if dm == "Yes" else 0) +
            3 * (1 if htn == "Yes" else 0) +
            2 * (1 if dcd == "Yes" else 0)
        )
    except Exception:
        kdpi = 0

    st.write(f"Calculated KDPI: {kdpi}")

    # Other inputs
    blood_type = st.selectbox("Blood Type", ["O", "A", "B", "AB"])
    hla_a = st.text_input("HLA-A", placeholder="Enter HLA-A value")
    hla_b = st.text_input("HLA-B", placeholder="Enter HLA-B value")
    hla_cw = st.text_input("HLA-Cw", placeholder="Enter HLA-Cw value")
    hla_dr = st.text_input("HLA-DR", placeholder="Enter HLA-DR value")

    # Submit button
    if st.button("Submit"):
        try:
            with engine.connect() as connection:
                connection.execute(text("""
                INSERT INTO donors (
                    name, donor_hospital, city, do_admission, admitting_dx, cause_of_death,
                    age, gender, ethnicity, weight, bmi, dm, htn, creat, hcv, dcd, kdpi,
                    blood_type, hla_a, hla_b, hla_cw, hla_dr
                ) VALUES (
                    :name, :donor_hospital, :city, :do_admission, :admitting_dx, :cause_of_death,
                    :age, :gender, :ethnicity, :weight, :bmi, :dm, :htn, :creat, :hcv, :dcd, :kdpi,
                    :blood_type, :hla_a, :hla_b, :hla_cw, :hla_dr
                )
                """), {
                    "name": name, "donor_hospital": donor_hospital, "city": city,
                    "do_admission": do_admission, "admitting_dx": admitting_dx, "cause_of_death": cause_of_death,
                    "age": age, "gender": gender, "ethnicity": ethnicity, "weight": weight, "bmi": bmi,
                    "dm": dm, "htn": htn, "creat": creat, "hcv": hcv, "dcd": dcd, "kdpi": kdpi,
                    "blood_type": blood_type, "hla_a": hla_a, "hla_b": hla_b, "hla_cw": hla_cw, "hla_dr": hla_dr
                })
            st.success("Donor added successfully!")
        except Exception as e:
            st.error(f"Error adding donor: {e}")
# Compatibility Check
elif menu == "Compatibility Check":
    st.title("🔍 Compatibility Check")
    
    # Load data from the database
    donors = pd.read_sql("SELECT * FROM donors", engine)
    recipients = pd.read_sql("SELECT * FROM recipients", engine)

    # تنظيف الأعمدة غير المرغوبة
    unwanted_columns = ['zero_abdrq_mm', 'zero_drdq_mm', 'zero_ab_mm']
    recipients = recipients.drop(columns=[col for col in unwanted_columns if col in recipients.columns])
    donors = donors.drop(columns=[col for col in unwanted_columns if col in donors.columns])

    # Function to check compatibility
    def is_compatible(donor, recipient):
        # Blood type compatibility
        blood_match = (
            donor["blood_type"] == "O" or  # Universal donor
            donor["blood_type"] == recipient["blood_type"] or  # Exact match
            recipient["blood_type"] == "AB"  # Universal recipient
        )

        # HLA compatibility (full match for all HLA fields)
        hla_match = all([
            donor["hla_a"] == recipient["hla_a"],
            donor["hla_b"] == recipient["hla_b"],
            donor["hla_cw"] == recipient["hla_cw"],
            donor["hla_dr"] == recipient["hla_dr"]
        ])

        # Antibody matching: Ensure none of the recipient's unacceptable antibodies match donor's HLA
        unacceptable_antibodies = recipient["unacceptable_antigen"].split(",") if recipient["unacceptable_antigen"] else []
        antibodies_match = not any(
            antibody.strip() in [donor["hla_a"], donor["hla_b"], donor["hla_cw"], donor["hla_dr"]]
            for antibody in unacceptable_antibodies
        )

        # Compatibility is achieved only if all three conditions are true
        return blood_match and hla_match and antibodies_match

    # Find compatibility between donors and recipients
    results = []
    for _, donor in donors.iterrows():
        compatible_recipients = []
        for _, recipient in recipients.iterrows():
            if is_compatible(donor, recipient):
                compatible_recipients.append(recipient["name"])
        results.append({
            "Donor": donor["name"],
            "Compatible Recipients": ", ".join(compatible_recipients),
            "Count": len(compatible_recipients)
        })

    # Display the results
    results_df = pd.DataFrame(results)
    st.write(results_df)
# View Results
elif menu == "View Results":
    st.title("📊 Final Matching Results")
    
    # Load recipients from the database
    recipients = pd.read_sql("SELECT * FROM recipients", engine)

    # Function to calculate priority score
    def calculate_priority(recipient):
        score = 0
        if recipient["urgent"] == "Yes":
            score += 300
        if recipient["age"] < 18:
            score += 1
        score += recipient.get("years_dialysis", 0)

        # Add PRA points
        pra = recipient.get("pra", 0)
        if pra == 100:
            score += 202
        elif pra == 99:
            score += 50.09
        elif pra == 98:
            score += 24.4
        elif pra == 97:
            score += 17.3
        elif pra == 96:
            score += 12.17
        elif pra == 95:
            score += 10.82
        elif 90 <= pra <= 94:
            score += 6.71
        elif 85 <= pra <= 89:
            score += 4.05
        elif 80 <= pra <= 84:
            score += 2.46
        elif 75 <= pra <= 79:
            score += 1.58
        elif 70 <= pra <= 74:
            score += 1.09
        elif 60 <= pra <= 69:
            score += 0.81
        elif 50 <= pra <= 59:
            score += 0.48
        elif 40 <= pra <= 49:
            score += 0.34
        elif 30 <= pra <= 39:
            score += 0.21
        elif 20 <= pra <= 29:
            score += 0.08
        return score

    # Apply priority scoring
    recipients["Priority_Score"] = recipients.apply(calculate_priority, axis=1)
    recipients_sorted = recipients.sort_values(by="Priority_Score", ascending=False)
    
    # تنظيف الأعمدة غير المرغوبة
    unwanted_columns = ['zero_abdrq_mm', 'zero_drdq_mm', 'zero_ab_mm']
    recipients_sorted = recipients_sorted.drop(columns=[col for col in unwanted_columns if col in recipients_sorted.columns])

    # Display results
    st.write(recipients_sorted)
# Manage Data
elif menu == "Manage Data":
    st.title("🛠️ Manage Data")
    
    manage_choice = st.selectbox("Choose Data to Manage", ["Recipients", "Donors"])
    
    if manage_choice == "Recipients":
        # Load recipients data
        recipients = pd.read_sql("SELECT * FROM recipients", engine)
        st.write("### Recipients Data")
        st.write(recipients)
        
        # Delete recipient
        delete_id = st.number_input("Enter Recipient ID to Delete", min_value=1, step=1)
        if st.button("Delete Recipient"):
            try:
                with engine.connect() as connection:
                    connection.execute(text("DELETE FROM recipients WHERE id = :id"), {"id": delete_id})
                st.success(f"Recipient with ID {delete_id} deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting recipient: {e}")

    elif manage_choice == "Donors":
        # Load donors data
        donors = pd.read_sql("SELECT * FROM donors", engine)
        st.write("### Donors Data")
        st.write(donors)
        
        # Delete donor
        delete_id = st.number_input("Enter Donor ID to Delete", min_value=1, step=1)
        if st.button("Delete Donor"):
            try:
                with engine.connect() as connection:
                    connection.execute(text("DELETE FROM donors WHERE id = :id"), {"id": delete_id})
                st.success(f"Donor with ID {delete_id} deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting donor: {e}")

