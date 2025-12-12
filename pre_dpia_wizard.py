import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class PreDPIAWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pre-DPIA Cogas Duurzaam")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        self.answers = {
            "project_name": tk.StringVar(),
            "project_leader": tk.StringVar(),
            "processes_personal_data": tk.StringVar(value=""),
            "triggers": [],
            "processing_purpose": tk.StringVar(value="Facturatie"),
            "processor_agreement": tk.StringVar(value="Ja"),
        }

        self.trigger_options = [
            "Maken we gebruik van Open Source / Gratis software?",
            "Worden gegevens opgeslagen buiten de EER (bijv. VS/Cloud)?",
            "Worden databases/systemen aan elkaar gekoppeld?",
            "Gaat het om financiële gegevens, BSN of verbruiksdata?",
            "Gaat het om grote aantallen (>5000 personen)?",
        ]

        self._build_style()
        self.frames = []
        self.current_step = 0

        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill="both")

        self._build_frames(container)
        self._build_navigation(container)
        self._show_frame(0)

    def _build_style(self):
        self.option_add("*Font", ("Segoe UI", 11))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#333333")
        style.configure("Heading.TLabel", font=("Segoe UI", 16, "bold"), foreground="#333333")
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), background="#66b512", foreground="#ffffff")
        style.map(
            "Accent.TButton",
            background=[("active", "#5aa110"), ("pressed", "#4c8f0d")],
            foreground=[("disabled", "#e6e6e6")],
        )

    def _build_frames(self, container):
        self.frames.append(self._build_start_frame(container))
        self.frames.append(self._build_risk_frame(container))
        self.frames.append(self._build_details_frame(container))
        self.frames.append(self._build_conclusion_frame(container))

    def _build_navigation(self, container):
        nav_frame = ttk.Frame(container, padding=(0, 10, 0, 0))
        nav_frame.pack(side="bottom", fill="x")

        self.prev_button = ttk.Button(nav_frame, text="Vorige", command=self._prev_step)
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(nav_frame, text="Volgende", style="Accent.TButton", command=self._next_step)
        self.next_button.pack(side="right")

    def _show_frame(self, index: int):
        for frame in self.frames:
            frame.pack_forget()

        self.frames[index].pack(expand=True, fill="both")
        self.current_step = index
        self._update_nav_buttons()

        if index == 3:
            self._update_conclusion()

    def _update_nav_buttons(self):
        self.prev_button.state(["!disabled"] if self.current_step > 0 else ["disabled"])

        if self.current_step == len(self.frames) - 1:
            self.next_button.state(["disabled"])
        else:
            self.next_button.state(["!disabled"])

    def _next_step(self):
        if self.current_step == 0 and not self._validate_start():
            return

        if self.current_step < len(self.frames) - 1:
            self._show_frame(self.current_step + 1)

    def _prev_step(self):
        if self.current_step > 0:
            self._show_frame(self.current_step - 1)

    def _validate_start(self) -> bool:
        if not self.answers["project_name"].get().strip():
            messagebox.showwarning("Ontbrekende invoer", "Vul de projectnaam in.")
            return False

        if not self.answers["project_leader"].get().strip():
            messagebox.showwarning("Ontbrekende invoer", "Vul de naam van de projectleider in.")
            return False

        choice = self.answers["processes_personal_data"].get()
        if choice == "Ja":
            return True

        if choice == "Nee":
            messagebox.showinfo("Geen actie nodig", "Geen actie nodig.")
            self.destroy()
            return False

        messagebox.showwarning("Ontbrekende keuze", "Selecteer of er persoonsgegevens worden verwerkt.")
        return False

    def _build_start_frame(self, parent):
        frame = ttk.Frame(parent, padding=20)

        ttk.Label(frame, text="Pre-DPIA Cogas Duurzaam", style="Heading.TLabel").pack(anchor="w", pady=(0, 20))

        form = ttk.Frame(frame)
        form.pack(fill="x", pady=5)

        ttk.Label(form, text="Projectnaam").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(form, textvariable=self.answers["project_name"], width=40).grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Naam Projectleider").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(form, textvariable=self.answers["project_leader"], width=40).grid(row=1, column=1, sticky="ew", pady=5)

        question_frame = ttk.Frame(frame, padding=(0, 10, 0, 0))
        question_frame.pack(anchor="w")

        ttk.Label(question_frame, text="Worden er persoonsgegevens verwerkt?").pack(anchor="w", pady=(10, 5))
        ttk.Radiobutton(question_frame, text="Ja", value="Ja", variable=self.answers["processes_personal_data"]).pack(anchor="w")
        ttk.Radiobutton(question_frame, text="Nee", value="Nee", variable=self.answers["processes_personal_data"]).pack(anchor="w")

        form.columnconfigure(1, weight=1)
        return frame

    def _build_risk_frame(self, parent):
        frame = ttk.Frame(parent, padding=20)
        ttk.Label(frame, text="Risico Analyse (Triggers)", style="Heading.TLabel").pack(anchor="w", pady=(0, 20))

        self.trigger_vars = []
        for option in self.trigger_options:
            var = tk.BooleanVar()
            ttk.Checkbutton(frame, text=option, variable=var).pack(anchor="w", pady=5)
            self.trigger_vars.append(var)

        return frame

    def _build_details_frame(self, parent):
        frame = ttk.Frame(parent, padding=20)
        ttk.Label(frame, text="Details", style="Heading.TLabel").pack(anchor="w", pady=(0, 20))

        ttk.Label(frame, text="Doel van verwerking?").pack(anchor="w", pady=5)
        purpose_menu = ttk.Combobox(
            frame,
            textvariable=self.answers["processing_purpose"],
            values=["Facturatie", "Beheer", "Marketing", "Anders"],
            state="readonly",
            width=30,
        )
        purpose_menu.pack(anchor="w", pady=5)

        ttk.Label(frame, text="Is er een verwerkersovereenkomst?").pack(anchor="w", pady=(15, 5))
        for label in ["Ja", "Nee", "Weet ik niet"]:
            ttk.Radiobutton(frame, text=label, value=label, variable=self.answers["processor_agreement"]).pack(anchor="w")

        return frame

    def _build_conclusion_frame(self, parent):
        frame = ttk.Frame(parent, padding=20)
        ttk.Label(frame, text="Conclusie", style="Heading.TLabel").pack(anchor="w", pady=(0, 20))

        self.conclusion_label = ttk.Label(frame, text="", wraplength=540, font=("Segoe UI", 12, "bold"))
        self.conclusion_label.pack(fill="x", pady=10)

        ttk.Button(frame, text="Rapport Opslaan", style="Accent.TButton", command=self._save_report).pack(anchor="e", pady=(20, 0))
        return frame

    def _update_conclusion(self):
        self.answers["triggers"] = [
            option for option, var in zip(self.trigger_options, self.trigger_vars) if var.get()
        ]
        has_risk = bool(self.answers["triggers"])

        if has_risk:
            text = (
                "LET OP: Er zijn risico-indicatoren. Een volledige DPIA is waarschijnlijk verplicht. "
                "Neem contact op met Privacy Officer Melanie Holtkamp."
            )
            self.conclusion_label.configure(foreground="#b00020")
        else:
            text = "Geen verhoogd risico gedetecteerd. Sla dit rapport op voor het register."
            self.conclusion_label.configure(foreground="#2e7d32")

        self.conclusion_label.configure(text=text)

    def _save_report(self):
        self._update_conclusion()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Tekstbestand", "*.txt")],
            title="Rapport Opslaan",
        )

        if not file_path:
            return

        content = self._build_report_content()
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Opgeslagen", "Het rapport is succesvol opgeslagen.")
        except OSError as exc:
            messagebox.showerror("Fout bij opslaan", f"Het rapport kon niet worden opgeslagen: {exc}")

    def _build_report_content(self) -> str:
        now = datetime.now().strftime("%d-%m-%Y %H:%M")
        risk_level = "HOOG RISICO" if self.answers["triggers"] else "LAAG RISICO"

        lines = [
            "Pre-DPIA Cogas Duurzaam - Rapport",
            f"Datum: {now}",
            "",
            f"Projectnaam: {self.answers['project_name'].get()}",
            f"Projectleider: {self.answers['project_leader'].get()}",
            f"Verwerken persoonsgegevens: {self.answers['processes_personal_data'].get()}",
            "",
            "Risico Triggers:",
        ]

        if self.answers["triggers"]:
            lines.extend([f"- {trigger}" for trigger in self.answers["triggers"]])
        else:
            lines.append("- Geen triggers geselecteerd")

        lines.extend(
            [
                "",
                f"Doel van verwerking: {self.answers['processing_purpose'].get()}",
                f"Verwerkersovereenkomst: {self.answers['processor_agreement'].get()}",
                "",
                f"Risico-advies: {risk_level}",
            ]
        )

        if self.answers["triggers"]:
            lines.append(
                "Advies: LET OP: Er zijn risico-indicatoren. Een volledige DPIA is waarschijnlijk verplicht. "
                "Neem contact op met Privacy Officer Melanie Holtkamp."
            )
        else:
            lines.append("Advies: Geen verhoogd risico gedetecteerd. Sla dit rapport op voor het register.")

        return "\n".join(lines)


if __name__ == "__main__":
    app = PreDPIAWizard()
    app.mainloop()
