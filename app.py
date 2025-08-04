import streamlit as st

st.title("Ερωτηματολόγιο Πελάτη για Άρδευση")

# --- Στοιχεία Πελάτη ---
st.header("🧑‍💼 Στοιχεία Πελάτη")
first_name = st.text_input("Όνομα")
last_name = st.text_input("Επώνυμο")
location = st.text_input("Τοποθεσία")
phone = st.text_input("Τηλέφωνο")

# --- Διαστάσεις Χωραφιού ---
st.header("🌾 Διαστάσεις Χωραφιού")
length = st.number_input("Μήκος (m)", min_value=0.0, step=1.0)
width = st.number_input("Πλάτος (m)", min_value=0.0, step=1.0)
area = st.number_input("Στρέμματα", min_value=0.0, step=0.1)

# --- Φύτευση ---
st.header("🌱 Πληροφορίες Φύτευσης")
in_row_spacing = st.number_input("Απόσταση φύτευσης επί της γραμμής (cm)", min_value=1.0)
between_row_spacing = st.number_input("Πλάτος διαδρόμου (cm)", min_value=1.0)

# --- Υπολογισμός BOM ---
if st.button("Υπολογισμός BOM"):
    if length > 0 and width > 0 and in_row_spacing > 0 and between_row_spacing > 0:
        # Μετατροπή cm σε m
        in_row_spacing_m = in_row_spacing / 100
        between_row_spacing_m = between_row_spacing / 100

        num_rows = int(width / between_row_spacing_m)
        plants_per_row = int(length / in_row_spacing_m)
        total_plants = num_rows * plants_per_row
        total_laid_pipe = num_rows * length

        st.success("✅ Υπολογισμός Ολοκληρώθηκε!")

        st.markdown("### 📋 Αποτελέσματα Υπολογισμών:")
        st.write(f"- Αριθμός γραμμών: **{num_rows}**")
        st.write(f"- Φυτά ανά γραμμή: **{plants_per_row}**")
        st.write(f"- Συνολικός αριθμός φυτών: **{total_plants}**")
        st.write(f"- Συνολικό μήκος λάστιχου: **{total_laid_pipe:.2f} m**")

        st.markdown("---")
        st.markdown("Μπορείς να χρησιμοποιήσεις τα παραπάνω για προσφορά ή BOM.")
    else:
        st.error("⚠️ Συμπλήρωσε όλα τα απαραίτητα πεδία πριν κάνεις υπολογισμό.")
