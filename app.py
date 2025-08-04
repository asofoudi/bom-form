import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="BOM Υπολογισμός", page_icon="🌱")

# ------------------------
# Google Sheet setup (You must replace with your own credentials and sheet)
# ------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("BOM Ερωτηματολόγιο").sheet1

# ------------------------
# Σελίδα 1: Γενικά Στοιχεία Παραγωγού
# ------------------------
st.title("1. ΓΕΝΙΚΑ ΣΤΟΙΧΕΙΑ ΠΑΡΑΓΩΓΟΥ & ΑΓΡΟΤΕΜΑΧΙΟΥ")

st.markdown("Συμπληρώστε τα παρακάτω πεδία με στοιχεία παραγωγού και αγροτεμαχίου.")

with st.form("form_farm"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Ονοματεπώνυμο")
        location = st.text_input("Τοποθεσία αγροτεμαχίου (περιοχή/χωριό)")
        field_area_declared = st.number_input("Έκταση αγροτεμαχίου (σε στρέμματα)", min_value=0.0, step=0.1)
        row_spacing = st.number_input("Απόσταση μεταξύ σειρών (m)", min_value=0.0, step=0.1)
    with col2:
        phone = st.text_input("Τηλέφωνο επικοινωνίας")
        dimensions = st.text_input("Διαστάσεις χωραφιού (π.χ. 80x120)")
        tree_spacing = st.number_input("Απόσταση δέντρων πάνω στη σειρά (m)", min_value=0.0, step=0.1)
        support_type = st.selectbox("Τύπος Υποστύλωσης", ["Κρεβατίνα", "ΤΑΦ", "Άλλο"])

    submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        try:
            dims = dimensions.lower().replace("μ", "").replace("m", "").replace(" ", "").split("x")
            if len(dims) == 2:
                length = float(dims[0])
                width = float(dims[1])
                area_from_dims = round((length * width) / 1000, 2)

                st.markdown("### 📏 Έλεγχος έκτασης βάσει διαστάσεων:")
                st.write(f"- Υπολογισμένη έκταση βάσει διαστάσεων: **{area_from_dims} στρέμματα**")
                st.write(f"- Δήλωση χρήστη: **{field_area_declared} στρέμματα**")

                diff = abs(area_from_dims - field_area_declared)
                if diff > 0.5:
                    st.warning("⚠️ Διαφορά μεταξύ διαστάσεων και δηλωμένης έκτασης. Ελέγξτε τα στοιχεία.")
                else:
                    st.success("✅ Οι διαστάσεις συμφωνούν με την έκταση.")

                # Αποθήκευση στο Google Sheet
                sheet.append_row([name, phone, location, dimensions, field_area_declared, row_spacing, tree_spacing, support_type, area_from_dims])

            else:
                st.error("⚠️ Λάθος μορφή διαστάσεων. Χρησιμοποίησε μορφή π.χ. 80x120")

        except ValueError:
            st.error("⚠️ Δώσε αριθμούς σε σωστή μορφή στο πεδίο διαστάσεων.")
        except Exception as e:
            st.error("⚠️ Δεν ήταν δυνατή η σύνδεση με το Google Sheet. Ελέγξτε τα credentials.")
