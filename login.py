import customtkinter as ctk
import subprocess
import sys
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Portal")
        self.after(0, lambda: self.state("zoomed"))
        self.configure(fg_color="#C9B8F0")
        self._last_size = (0, 0)
        self._build_card()
        self.bind("<Configure>", self._on_resize)

    def _draw_gradient_bg(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        if hasattr(self, "bg_canvas"):
            self.bg_canvas.destroy()
        self.bg_canvas = ctk.CTkCanvas(self, width=w, height=h, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        for i in range(h):
            r1, g1, b1 = 0xE0, 0xC3, 0xFC
            r2, g2, b2 = 0x8E, 0xC5, 0xFC
            t = i / max(h, 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            self.bg_canvas.create_line(0, i, w, i, fill=f"#{r:02x}{g:02x}{b:02x}")
        if hasattr(self, "card"):
            self.card.lift()

    def _on_resize(self, event):
        new_size = (self.winfo_width(), self.winfo_height())
        if new_size != self._last_size and new_size[0] > 2:
            self._last_size = new_size
            self._draw_gradient_bg()

    def _build_card(self):
        self.card = ctk.CTkFrame(
            self, width=420, height=580,
            corner_radius=30, fg_color="white", border_width=0,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        inner = ctk.CTkFrame(self.card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)

        avatar_frame = ctk.CTkFrame(inner, width=80, height=80, corner_radius=40, fg_color="#EDE7F6")
        avatar_frame.pack(pady=(10, 0))
        avatar_frame.pack_propagate(False)
        ctk.CTkLabel(avatar_frame, text="👤", font=("Segoe UI Emoji", 36),
                     fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text="Welcome Back",
                     font=("Georgia", 24, "bold"), text_color="#3D1A78").pack(pady=(14, 2))
        ctk.CTkLabel(inner, text="Sign in to your account",
                     font=("Segoe UI", 12), text_color="#9E9E9E").pack(pady=(0, 20))

        user_row = ctk.CTkFrame(inner, fg_color="#F5F5F5", corner_radius=12, height=48)
        user_row.pack(fill="x", pady=6)
        user_row.pack_propagate(False)
        ctk.CTkLabel(user_row, text="  👤 ", font=("Segoe UI Emoji", 14),
                     fg_color="transparent", text_color="#9E9E9E").pack(side="left", padx=(8, 0))
        self.username_entry = ctk.CTkEntry(
            user_row, placeholder_text="Username or Email",
            border_width=0, fg_color="transparent",
            font=("Segoe UI", 13), text_color="#333333",
            placeholder_text_color="#BDBDBD", height=40
        )
        self.username_entry.pack(side="left", fill="both", expand=True, padx=(4, 8))

        pass_row = ctk.CTkFrame(inner, fg_color="#F5F5F5", corner_radius=12, height=48)
        pass_row.pack(fill="x", pady=6)
        pass_row.pack_propagate(False)
        ctk.CTkLabel(pass_row, text="  🔒 ", font=("Segoe UI Emoji", 14),
                     fg_color="transparent", text_color="#9E9E9E").pack(side="left", padx=(8, 0))
        self.password_entry = ctk.CTkEntry(
            pass_row, placeholder_text="Password",
            border_width=0, fg_color="transparent",
            font=("Segoe UI", 13), text_color="#333333",
            placeholder_text_color="#BDBDBD", height=40, show="●"
        )
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(4, 0))
        self.show_pass = False
        self.eye_btn = ctk.CTkButton(
            pass_row, text="🙈", width=36, height=36,
            fg_color="transparent", hover_color="#EEEEEE",
            text_color="#9E9E9E", font=("Segoe UI Emoji", 16),
            command=self._toggle_password
        )
        self.eye_btn.pack(side="right", padx=4)

        rem_row = ctk.CTkFrame(inner, fg_color="transparent")
        rem_row.pack(fill="x", pady=(8, 4))
        self.remember_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            rem_row, text="Remember me", variable=self.remember_var,
            font=("Segoe UI", 12), text_color="#666666",
            fg_color="#8A2BE2", hover_color="#9370DB",
            checkmark_color="white", border_color="#BDBDBD", corner_radius=4
        ).pack(side="left")

        ctk.CTkButton(
            inner, text="Log In", height=48, corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            fg_color="#8A2BE2", hover_color="#7B1FA2",
            text_color="white", command=self._on_login
        ).pack(fill="x", pady=(16, 8))

        ctk.CTkButton(
            inner, text="Forgot Password?", fg_color="transparent",
            hover_color="#F3E5F5", text_color="#8A2BE2",
            font=("Segoe UI", 12), height=28, command=lambda: None
        ).pack()

        self.status_label = ctk.CTkLabel(
            inner, text="", font=("Segoe UI", 11),
            text_color="#E53935", fg_color="transparent"
        )
        self.status_label.pack(pady=(4, 0))

    def _toggle_password(self):
        self.show_pass = not self.show_pass
        if self.show_pass:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="👁")
        else:
            self.password_entry.configure(show="●")
            self.eye_btn.configure(text="🙈")

    def _on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.status_label.configure(text="Please fill in all fields.")
            return
        if username == "admin" and password == "admin123":
            self.destroy()
            subprocess.Popen([sys.executable,
                              os.path.join(os.path.dirname(__file__), "dashboard.py")])
        else:
            self.status_label.configure(text="Invalid username or password.")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
