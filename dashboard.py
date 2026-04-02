import customtkinter as ctk
import json
import os
import sys

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DATA_FILE = os.path.join(os.path.dirname(__file__), "employees.json")

# Column config: (label, weight, min_width, anchor)
COLUMNS = [
    ("#",             0,  50,  "center"),
    ("Employee Name", 3, 200,  "w"),
    ("RFID UID",      2, 160,  "w"),
    ("Action",        1, 110,  "center"),
]


def load_employees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_employees(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Register Management")
        self.after(0, lambda: self.state("zoomed"))
        self.configure(fg_color="#F0ECFF")
        self.employees = load_employees()
        self._build_ui()

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="white", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="Register Management",
            font=("Georgia", 22, "bold"), text_color="#5B2D8E"
        ).pack(side="left", padx=32, pady=18)

        # ── Main card ──────────────────────────────────────────────
        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.card.pack(fill="both", expand=True, padx=28, pady=20)

        # ── Toolbar ────────────────────────────────────────────────
        toolbar = ctk.CTkFrame(self.card, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=(18, 10))

        search_frame = ctk.CTkFrame(toolbar, fg_color="#F5F5F5", corner_radius=10, height=40)
        search_frame.pack(side="left", fill="x", expand=True)
        search_frame.pack_propagate(False)
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI Emoji", 14),
                     fg_color="transparent", text_color="#9E9E9E").pack(side="left", padx=(10, 0))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._refresh_table())
        ctk.CTkEntry(
            search_frame, placeholder_text="Search employee or RFID...",
            textvariable=self.search_var,
            border_width=0, fg_color="transparent",
            font=("Segoe UI", 12), text_color="#333333",
            placeholder_text_color="#BDBDBD", height=36
        ).pack(side="left", fill="both", expand=True, padx=6)

        ctk.CTkButton(
            toolbar, text="＋ Add", width=90, height=40,
            corner_radius=10, font=("Segoe UI", 13, "bold"),
            fg_color="#8A2BE2", hover_color="#7B1FA2",
            text_color="white", command=self._open_add_modal
        ).pack(side="right", padx=(12, 0))

        # ── Table header (grid-based) ──────────────────────────────
        col_frame = ctk.CTkFrame(self.card, fg_color="#F3EEFF", corner_radius=8, height=40)
        col_frame.pack(fill="x", padx=20, pady=(0, 4))
        col_frame.pack_propagate(False)
        self._configure_grid(col_frame)
        for i, (label, weight, min_w, anchor) in enumerate(COLUMNS):
            ctk.CTkLabel(
                col_frame, text=label,
                font=("Segoe UI", 12, "bold"), text_color="#5B2D8E",
                anchor=anchor
            ).grid(row=0, column=i, sticky="nsew", padx=(16 if i == 0 else 12, 12), pady=8)

        # ── Scrollable rows ────────────────────────────────────────
        self.rows_frame = ctk.CTkScrollableFrame(
            self.card, fg_color="transparent", corner_radius=0
        )
        self.rows_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        self._configure_grid(self.rows_frame)

        self._refresh_table()

    def _configure_grid(self, frame):
        """Apply the same column weight config to any frame used as a row."""
        for i, (_, weight, min_w, _anchor) in enumerate(COLUMNS):
            frame.grid_columnconfigure(i, weight=weight, minsize=min_w)

    def _refresh_table(self):
        for w in self.rows_frame.winfo_children():
            w.destroy()
        query = self.search_var.get().lower()
        filtered = [e for e in self.employees
                    if query in e["name"].lower() or query in e["rfid"].lower()]
        if not filtered:
            ctk.CTkLabel(self.rows_frame, text="No employees found.",
                         font=("Segoe UI", 13), text_color="#BDBDBD").grid(
                row=0, column=0, columnspan=4, pady=40)
            return
        for idx, emp in enumerate(filtered):
            self._build_row(idx, emp)

    def _build_row(self, idx, emp):
        bg = "white" if idx % 2 == 0 else "#FAF9FF"
        row = ctk.CTkFrame(self.rows_frame, fg_color=bg, corner_radius=8, height=46)
        row.grid(row=idx, column=0, columnspan=4, sticky="ew", pady=2)
        row.pack_propagate(False)
        self._configure_grid(row)

        ctk.CTkLabel(row, text=str(idx + 1), font=("Segoe UI", 12),
                     text_color="#888888", anchor="center"
                     ).grid(row=0, column=0, sticky="nsew", padx=(16, 12), pady=8)

        ctk.CTkLabel(row, text=emp["name"], font=("Segoe UI", 12),
                     text_color="#333333", anchor="w"
                     ).grid(row=0, column=1, sticky="nsew", padx=12, pady=8)

        ctk.CTkLabel(row, text=emp["rfid"], font=("Courier New", 12),
                     text_color="#555555", anchor="w"
                     ).grid(row=0, column=2, sticky="nsew", padx=12, pady=8)

        ctk.CTkButton(
            row, text="Remove", width=80, height=28, corner_radius=8,
            fg_color="#FFEBEE", hover_color="#FFCDD2",
            text_color="#E53935", font=("Segoe UI", 11, "bold"),
            border_width=0, command=lambda e=emp: self._remove_employee(e)
        ).grid(row=0, column=3, padx=12, pady=8)

    def _remove_employee(self, emp):
        self.employees = [e for e in self.employees if e["rfid"] != emp["rfid"]]
        save_employees(self.employees)
        self._refresh_table()

    def _open_add_modal(self):
        from add_user import AddUserModal
        modal = AddUserModal(self, callback=self._on_user_added)
        modal.grab_set()

    def _on_user_added(self, name, rfid):
        self.employees.append({"name": name, "rfid": rfid})
        save_employees(self.employees)
        self._refresh_table()


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
