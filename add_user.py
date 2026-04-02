import customtkinter as ctk


class AddUserModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.title("Add New User")
        self.resizable(False, False)
        self.configure(fg_color="#F0ECFF")
        self.transient(parent)

        # Center modal over the parent window after it renders
        self.after(10, lambda: self._center_on_parent(parent))
        self.after(20, self.lift)
        self._build_ui()

    def _center_on_parent(self, parent):
        w, h = 440, 370
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=24)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.90)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)

        ctk.CTkLabel(inner, text="Add New User",
                     font=("Georgia", 20, "bold"), text_color="#5B2D8E").pack(pady=(0, 4))
        ctk.CTkLabel(inner, text="Fill in the details below",
                     font=("Segoe UI", 11), text_color="#BDBDBD").pack(pady=(0, 18))

        ctk.CTkLabel(inner, text="Full Name", font=("Segoe UI", 12, "bold"),
                     text_color="#555555", anchor="w").pack(fill="x")
        self.name_entry = ctk.CTkEntry(
            inner, placeholder_text="e.g. Juan dela Cruz",
            height=42, corner_radius=10,
            border_width=1, border_color="#DDD0F5",
            fg_color="#FAFAFA", font=("Segoe UI", 12),
            text_color="#333333", placeholder_text_color="#BDBDBD"
        )
        self.name_entry.pack(fill="x", pady=(4, 12))

        ctk.CTkLabel(inner, text="RFID UID", font=("Segoe UI", 12, "bold"),
                     text_color="#555555", anchor="w").pack(fill="x")
        self.rfid_entry = ctk.CTkEntry(
            inner, placeholder_text="e.g. A3F2B901",
            height=42, corner_radius=10,
            border_width=1, border_color="#DDD0F5",
            fg_color="#FAFAFA", font=("Courier New", 12),
            text_color="#333333", placeholder_text_color="#BDBDBD"
        )
        self.rfid_entry.pack(fill="x", pady=(4, 6))

        self.error_label = ctk.CTkLabel(inner, text="", font=("Segoe UI", 11),
                                         text_color="#E53935", fg_color="transparent")
        self.error_label.pack(pady=(0, 8))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row, text="Cancel", height=42, corner_radius=10,
            fg_color="white", hover_color="#F3E5F5",
            text_color="#8A2BE2", border_width=1, border_color="#DDD0F5",
            font=("Segoe UI", 13), command=self.destroy
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            btn_row, text="Add User", height=42, corner_radius=10,
            fg_color="#8A2BE2", hover_color="#7B1FA2",
            text_color="white", font=("Segoe UI", 13, "bold"),
            command=self._on_submit
        ).pack(side="right", expand=True, fill="x", padx=(6, 0))

    def _on_submit(self):
        name = self.name_entry.get().strip()
        rfid = self.rfid_entry.get().strip()
        if not name:
            self.error_label.configure(text="Full Name is required.")
            return
        if not rfid:
            self.error_label.configure(text="RFID UID is required.")
            return
        if self.callback:
            self.callback(name, rfid)
        self.destroy()
