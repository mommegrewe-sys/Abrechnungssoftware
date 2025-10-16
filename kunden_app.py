import streamlit as st
import psycopg2
import pandas as pd

# ==========================
# 🔌 Verbindung zur Datenbank
# ==========================
def get_connection():
    return psycopg2.connect(
        dbname="Abrechnung",
        user="mommegrewe",
        password="",  # ggf. anpassen
        host="localhost",
        port="5432"
    )

# ==========================
# 🔍 Seite: Kundenverwaltung
# ==========================
st.set_page_config(page_title="Kundenverwaltung", layout="wide")
st.title("📇 Kundenverwaltung")

# --- Filterleiste ---
col1, col2 = st.columns([4, 1])
with col1:
    search_term = st.text_input("🔍 Suche nach Name, E-Mail, Ort, ID oder Kundennummer", "")
with col2:
    only_active = st.checkbox("Nur aktive Kunden anzeigen", value=False)

# ==========================
# 📊 Daten abrufen
# ==========================
try:
    conn = get_connection()

    query = """
        SELECT 
            p.id,
            p.name AS "Name",
            p.email_contact AS "E-Mail",
            p.postal_code AS "PLZ",
            p.city AS "Ort",
            CONCAT(p.street, ' ', p.house_number) AS "Adresse",
            p.email_invoice AS "E-Mail Rechnung",
            p.invoice_by_mail AS "Rechnung per Mail",
            p.active AS "Aktiv",
            p.created_at AS "Erstellt am"
        FROM partners p
    ORDER BY p.name;
    """

    kunden_df = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f"❌ Fehler beim Laden der Kunden: {e}")
    st.stop()

# --- Filter anwenden ---
if search_term:
    search_term = search_term.lower()
    kunden_df = kunden_df[
        kunden_df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)
    ]

if only_active:
    kunden_df = kunden_df[kunden_df["Aktiv"] == True]

# ==========================
# 📋 Tabellenanzeige
# ==========================
st.subheader("Kundenliste")
if kunden_df.empty:
    st.info("Keine Kunden gefunden.")
    selected_row = None
else:
    # Eine auswählbare Tabelle mit Dropdown (simuliert Klick)
    row_labels = [f"{r['Name']} ({r['Ort']})" for _, r in kunden_df.iterrows()]
    selected_index = st.selectbox(
        "Kunde auswählen:",
        options=range(len(kunden_df)),
        format_func=lambda i: row_labels[i] if len(row_labels) > 0 else "",
        index=0 if len(kunden_df) > 0 else None
    )

    selected_row = kunden_df.iloc[selected_index]
    st.dataframe(
        kunden_df.style.highlight_between(
            subset=["Name"], left=selected_row["Name"], right=selected_row["Name"],
            color="#d1e7dd"
        ),
        use_container_width=True,
        hide_index=True
    )

# ==========================
# 🧭 Aktionen
# ==========================
st.markdown("---")
col_a1, col_a2, col_a3 = st.columns([1, 1, 8])

# --- "Neuer Kunde" ---
with col_a1:
    if st.button("➕ Neu"):
        with st.form("neuer_kunde", clear_on_submit=True):
            st.subheader("🧾 Neuen Kunden anlegen")
            name = st.text_input("Name*")
            kundennummer = st.text_input("Kundennummer")
            email = st.text_input("E-Mail")
            plz = st.text_input("PLZ")
            ort = st.text_input("Ort")
            strasse = st.text_input("Straße")
            hausnr = st.text_input("Hausnummer")
            ansprechpartner_vn = st.text_input("Ansprechpartner Vorname")
            ansprechpartner_nn = st.text_input("Ansprechpartner Nachname")
            rechnung_per_mail = st.checkbox("Rechnung per Mail", value=True)
            aktiv = st.checkbox("Aktiv", value=True)

            submitted = st.form_submit_button("💾 Speichern")
            if submitted:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO partners 
                        (name, customer_number, email_contact, postal_code, city, street, house_number, invoice_by_mail, active)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id;
                    """, (name, kundennummer, email, plz, ort, strasse, hausnr, rechnung_per_mail, aktiv))
                    new_id = cur.fetchone()[0]
                    cur.execute("""
                        INSERT INTO contacts (first_name, last_name, partner_id)
                        VALUES (%s,%s,%s);
                    """, (ansprechpartner_vn, ansprechpartner_nn, new_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Kunde '{name}' erfolgreich angelegt!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Fehler beim Speichern: {e}")

# --- "Bearbeiten" ---
with col_a2:
    if st.button("✏️ Bearbeiten", disabled=kunden_df.empty):
        if selected_row is not None:
            with st.form("edit_kunde", clear_on_submit=False):
                st.subheader(f"✏️ Kunde bearbeiten: {selected_row['Name']}")
                name = st.text_input("Name", selected_row["Name"])
                email = st.text_input("E-Mail", selected_row["E-Mail"])
                ort = st.text_input("Ort", selected_row["Ort"])
                aktiv = st.checkbox("Aktiv", bool(selected_row["Aktiv"]))

                save_edit = st.form_submit_button("💾 Änderungen speichern")
                if save_edit:
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("""
                            UPDATE partners 
                            SET name=%s, email_contact=%s, city=%s, active=%s
                            WHERE id=%s;
                        """, (name, email, ort, aktiv, int(selected_row["id"])))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success("✅ Änderungen gespeichert!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Fehler beim Aktualisieren: {e}")

# --- "Löschen" ---
with col_a3:
    if st.button("🗑️ Löschen", disabled=kunden_df.empty):
        if selected_row is not None:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM partners WHERE id=%s;", (int(selected_row["id"]),))
                conn.commit()
                cur.close()
                conn.close()
                st.warning(f"🗑️ Kunde '{selected_row['Name']}' gelöscht.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Fehler beim Löschen: {e}")
