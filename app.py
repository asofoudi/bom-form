import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BOM Υπολογισμός", page_icon="🌱")

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

            else:
                st.error("⚠️ Λάθος μορφή διαστάσεων. Χρησιμοποίησε μορφή π.χ. 80x120")

        except ValueError:
            st.error("⚠️ Δώσε αριθμούς σε σωστή μορφή στο πεδίο διαστάσεων.")

# ------------------------
# Σελίδα 2: Καταγραφή Υδρομέτρου
# ------------------------
st.title("2. Καταγραφή Ενδείξεων Υδρομέτρου")

st.markdown("Συμπληρώστε τις μετρήσεις: ώρα, ένδειξη υδρομέτρου και πίεση λειτουργίας. Η εφαρμογή υπολογίζει την παροχή (m³/h).")

num_rows = st.number_input("Πόσες μετρήσεις θέλετε να καταχωρήσετε;", min_value=2, max_value=20, step=1)

measurements = []

for i in range(int(num_rows)):
    st.markdown(f"#### Μέτρηση {i+1}")
    col1, col2, col3 = st.columns(3)
    with col1:
        time_str = st.text_input(f"Ώρα (π.χ. 09:15)", key=f"time_{i}")
    with col2:
        value = st.number_input("Ένδειξη Υδρομέτρου (m³)", key=f"reading_{i}", min_value=0.0)
    with col3:
        pressure = st.number_input("Πίεση (bar)", key=f"pressure_{i}", min_value=0.0)

    measurements.append({"time": time_str, "reading": value, "pressure": pressure})

if st.button("Υπολογισμός Παροχών"):
    try:
        df = pd.DataFrame(measurements)
        df['parsed_time'] = pd.to_datetime(df['time'], format='%H:%M')
        df['flow'] = None

        for i in range(1, len(df)):
            delta_m3 = df.loc[i, 'reading'] - df.loc[i-1, 'reading']
            delta_time = (df.loc[i, 'parsed_time'] - df.loc[i-1, 'parsed_time']).seconds / 3600
            flow_rate = delta_m3 / delta_time if delta_time > 0 else 0
            df.loc[i, 'flow'] = round(flow_rate, 2)

        st.markdown("### 📊 Αποτελέσματα Παροχής")
        st.dataframe(df[['time', 'reading', 'pressure', 'flow']].rename(columns={
            'time': 'Ώρα', 'reading': 'Ένδειξη (m³)', 'pressure': 'Πίεση (bar)', 'flow': 'Παροχή (m³/h)'
        }), use_container_width=True)
    except Exception as e:
        st.error("⚠️ Σφάλμα στην επεξεργασία χρόνου ή δεδομένων. Βεβαιωθείτε ότι η ώρα είναι σωστή (π.χ. 09:30).")

# ------------------------
# Σελίδα 3: Σκαρίφημα
# ------------------------
st.title("3. ΣΧΕΔΙΟ (ΣΚΑΡΙΦΗΜΑ) ΤΟΥ ΧΩΡΑΦΙΟΥ")

st.markdown("""
Παρακαλείται ο παραγωγός να επισυνάψει **χειρόγραφο ή ψηφιακό σκαρίφημα** του αγροτεμαχίου,
στο οποίο να φαίνονται:

- Η θέση της αντλίας
- Η κατεύθυνση και διαδρομή του αρδευτικού δικτύου
- Οι διατομές σωληνώσεων (π.χ. Φ90 - Φ110)
- Οι σειρές φύτευσης
- Αν υπάρχουν κλίσεις ή υψομετρικές διαφορές
""")

uploaded_sketch = st.file_uploader("📎 Μεταφόρτωση Σκαριφήματος (εικόνα ή PDF)", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_sketch is not None:
    file_details = {"Όνομα": uploaded_sketch.name, "Μέγεθος": uploaded_sketch.size, "Τύπος": uploaded_sketch.type}
    st.write("✅ Αρχείο ανεβάστηκε:", file_details)

    if uploaded_sketch.type in ["image/png", "image/jpeg"]:
        st.image(uploaded_sketch, caption="Προεπισκόπηση Σκαριφήματος", use_column_width=True)
    elif uploaded_sketch.type == "application/pdf":
        st.info("📄 Ανέβηκε αρχείο PDF. Μπορείς να το δεις μετά την αποθήκευση.")
