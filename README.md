# Techno
simple ui in technopreneurship




rfid_attendance_system/
│
├── main.py                 # Ang "Puso" ng app. Dito nag-uumpisa ang lahat.
├── requirements.txt        # Listahan ng libraries (customtkinter, pyserial, etc.)
│
├── core/                   # Dito nakatira ang Logic (Non-UI)
│   ├── __init__.py
│   ├── database.py         # SQLite CRUD (Create, Read, Update, Delete)
│   ├── serial_manager.py   # Connector para sa Arduino (The Listener)
│   └── voice_engine.py     # PyTTSX3 wrapper para sa pagsasalita ng laptop
│
├── ui/                     # Lahat ng may kinalaman sa "Ganda" ng app
│   ├── __init__.py
│   ├── app_window.py       # Main Root Window (CustomTkinter)
│   ├── components/         # Small reusable parts (Buttons, Navbars)
│   ├── views/              # Full Screens
│   │   ├── login_page.py
│   │   ├── dashboard.py    # Listahan ng employees at Attendance logs
│   │   └── register_page.py # Form para sa pag-input ng pangalan
│   └── assets/             # Images, Icons (.png/.ico), and Themes (.json)
│
└── data/                   # Dito itatabi ang Database file
    └── system_records.db   # Ang SQLite file mo



arduino_rfid_node/
│
├── arduino_rfid_node.ino   # Ang main sketch (Setup at Loop)
├── config.h                # Dito mo ilalagay ang Pin Definitions (e.g., SS_PIN, RST_PIN)
└── README.md               # Wiring diagram guide (Para 'di malimutan ang saksakan ng pins)


