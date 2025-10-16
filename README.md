# 💼 Abrechnungssoftware

Dies ist ein Entwicklungsprojekt für eine datenbankgestützte **Abrechnungssoftware**,  
die in Python entwickelt und mit PostgreSQL betrieben wird.  
Die Anwendung bietet ein webbasiertes Frontend (Streamlit)  
zur Verwaltung von Kunden, Rechnungen, Maßnahmen und weiteren Stammdaten.

---

## ⚙️ Setup & Umgebung

### 🧱 Projektstruktur
```
Abrechnungssoftware/
│
├── venv/                    # Virtuelle Python-Umgebung
├── db_connection.py         # Verbindung zur PostgreSQL-Datenbank
├── kunden_app.py            # Streamlit-Modul für Kundenverwaltung
├── ER-Diagramm_Abrechnung.erd
└── README.md                # Dieses Dokument
```

### 🧩 Installierte Software
| Komponente | Version / Beschreibung |
|-------------|------------------------|
| **macOS** | Entwicklungssystem |
| **Python** | 3.12 (Homebrew) |
| **PostgreSQL** | 14.x |
| **DBeaver** | DB-Management-Tool |
| **Streamlit** | 1.50.0 |
| **Python-Pakete** | psycopg2, pandas, sqlalchemy, streamlit-aggrid |

---

## 🚀 Start der Anwendung

1. **PostgreSQL starten:**
   ```bash
   brew services start postgresql@14
   ```

2. **Virtuelle Umgebung aktivieren:**
   ```bash
   cd ~/Desktop/Abrechnungssoftware
   source venv/bin/activate
   ```

3. **App starten:**
   ```bash
   streamlit run kunden_app.py
   ```

4. **Browser öffnen:**
   → [http://localhost:8501](http://localhost:8501)

---

## 🧾 Datenbank

Die Anwendung basiert auf einer relationalen **PostgreSQL-Datenbank**.  
Das Schema enthält rund 25 Tabellen (siehe `ER-Diagramm_Abrechnung.erd`).  
Wichtige Tabellen:

| Tabelle | Zweck |
|----------|-------|
| `partners` | Kunden / Lieferanten |
| `contacts` | Ansprechpartner |
| `invoices` | Ausgangsrechnungen |
| `invoice_items` | Rechnungspositionen |
| `measures` | Maßnahmen (z. B. Schulungen) |
| `appointments` | Termine |
| `fundings` | Fördermittel |

---

## 🧮 Aktuelles Modul: Kundenverwaltung

Funktionen:
- Kundenliste (Filterbar, Suchfunktion, „Nur aktive Kunden“)
- Klickbare Tabelle (via AgGrid)
- Formulare für **Erstellen, Bearbeiten, Löschen**
- Direkte Anbindung an Tabelle `partners`

---

## 🔧 To-Do / Nächste Schritte
- [ ] Integration von **st-aggrid** für interaktive Tabellen
- [ ] Layout-Upgrade (rechtsseitige Aktionsleiste)
- [ ] Implementierung „Bearbeiten“ & „Löschen“ (mit Bestätigung)
- [ ] Modul „Rechnungen“ beginnen
- [ ] Login / Benutzerverwaltung ergänzen

---

## 🧠 Hinweise
- Datenbankname: `Abrechnung`
- Verbindung erfolgt lokal über `localhost:5432`
- Backup & Export über DBeaver empfohlen

---

**Autor:** Momme Grewe  
**Technischer Mentor:** ChatGPT (Full-Stack-Entwicklungsassistenz)
