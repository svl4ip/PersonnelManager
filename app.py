# -*- coding: utf-8 -*-
"""
Personnel Manager - Offline bilingual desktop starter
Designed for Windows 10/11 x64. Uses only Python standard library.
"""
import csv, os, sys, shutil, sqlite3, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

APP_NAME = "Personnel Manager"
DB_NAME = "personnel.db"

TABLES = {
    "people": {
        "en": ("Personnel", ["Full name", "Personnel number", "Category", "Rank / Title", "Unit", "Date of birth", "Appointment date", "Last promotion", "Phone", "Status", "Notes"]),
        "ar": ("الأفراد", ["الاسم الكامل", "الرقم الوظيفي/العسكري", "الصنف", "الرتبة / العنوان", "الوحدة", "تاريخ الميلاد", "تاريخ التعيين", "آخر ترقية", "الهاتف", "الحالة", "ملاحظات"]),
    },
    "attendance": {
        "en": ("Attendance & Absence", ["Personnel number", "Date", "Status", "Arrival time", "Departure time", "Notes"]),
        "ar": ("الحضور والغياب", ["الرقم الوظيفي/العسكري", "التاريخ", "الحالة", "وقت الحضور", "وقت الانصراف", "ملاحظات"]),
    },
    "leaves": {
        "en": ("Leaves", ["Personnel number", "Leave type", "Start date", "End date", "Days", "Status", "Notes"]),
        "ar": ("الإجازات", ["الرقم الوظيفي/العسكري", "نوع الإجازة", "من تاريخ", "إلى تاريخ", "عدد الأيام", "الحالة", "ملاحظات"]),
    },
    "penalties": {
        "en": ("Penalties", ["Personnel number", "Penalty type", "Order number", "Date", "Details"]),
        "ar": ("العقوبات", ["الرقم الوظيفي/العسكري", "نوع العقوبة", "رقم الأمر الإداري", "التاريخ", "التفاصيل"]),
    },
    "commendations": {
        "en": ("Commendations", ["Personnel number", "Letter number", "Date", "Issuing authority", "Details"]),
        "ar": ("كتب الشكر", ["الرقم الوظيفي/العسكري", "رقم الكتاب", "التاريخ", "الجهة المانحة", "التفاصيل"]),
    },
    "promotions": {
        "en": ("Promotions", ["Personnel number", "Current rank", "Next rank", "Eligibility date", "Order number", "Status", "Notes"]),
        "ar": ("الترقيات والترفيعات", ["الرقم الوظيفي/العسكري", "الرتبة الحالية", "الرتبة القادمة", "تاريخ الاستحقاق", "رقم الأمر", "الحالة", "ملاحظات"]),
    },
}

TEXT = {
 "en": {
  "title":"Personnel Affairs Management", "subtitle":"Offline personnel records", "language":"العربية",
  "add":"Add", "edit":"Edit", "delete":"Delete", "search":"Search", "backup":"Backup", "restore":"Restore",
  "export":"Export CSV", "about":"About", "select":"Select a record first.", "confirm":"Delete the selected record?",
  "saved":"Record saved.", "deleted":"Record deleted.", "backup_ok":"Backup created successfully.",
  "restore_ok":"Database restored. Restart the program to refresh all views.", "all":"All",
  "footer":"Designed and developed by Hussein Rahim | © 2026 All rights reserved",
  "note":"This local starter is not an officially approved Ministry of Defence system. Do not enter classified or real sensitive personnel data until security controls are independently reviewed.",
  "required":"Full name is required.", "new":"New record", "save":"Save", "cancel":"Cancel",
  "no_data":"No records yet.", "records":"Records"
 },
 "ar": {
  "title":"نظام إدارة شؤون الأفراد", "subtitle":"إدارة محلية بدون إنترنت", "language":"English",
  "add":"إضافة", "edit":"تعديل", "delete":"حذف", "search":"بحث", "backup":"نسخة احتياطية", "restore":"استعادة",
  "export":"تصدير CSV", "about":"حول النظام", "select":"حدد سجلاً أولاً.", "confirm":"متأكد تريد حذف السجل المحدد؟",
  "saved":"تم حفظ السجل.", "deleted":"تم حذف السجل.", "backup_ok":"تم إنشاء النسخة الاحتياطية بنجاح.",
  "restore_ok":"تمت استعادة قاعدة البيانات. أعد تشغيل البرنامج لتحديث الجداول.", "all":"الكل",
  "footer":"تصميم وتطوير حسين رحيم | جميع الحقوق محفوظة © 2026",
  "note":"هذه نسخة أولية محلية وليست نظاماً معتمداً رسمياً من وزارة الدفاع. لا تدخل بيانات عسكرية سرية أو بيانات شخصية حقيقية حساسة قبل مراجعة وسائل الحماية بشكل مستقل.",
  "required":"الاسم الكامل مطلوب.", "new":"سجل جديد", "save":"حفظ", "cancel":"إلغاء",
  "no_data":"لا توجد سجلات حالياً.", "records":"السجلات"
 }
}

class PersonnelApp:
    def __init__(self, root):
        self.root = root
        self.lang = "ar"
        self.current_table = "people"
        base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, DB_NAME)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.init_db()
        self.setup_style()
        self.build_ui()
        self.refresh()

    def init_db(self):
        for key, spec in TABLES.items():
            cols = spec["en"][1]
            fields = ", ".join('"%s" TEXT' % c.replace('"','""') for c in cols)
            self.conn.execute(f'CREATE TABLE IF NOT EXISTS "{key}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {fields})')
        self.conn.commit()

    def setup_style(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", padding=6)

    def t(self, key): return TEXT[self.lang][key]
    def fields(self): return TABLES[self.current_table][self.lang][1]
    def title_for(self, key): return TABLES[key][self.lang][0]

    def build_ui(self):
        self.root.geometry("1180x720")
        self.root.minsize(900, 580)
        self.root.configure(bg="#f2f5f8")
        self.header = tk.Frame(self.root, bg="#12334a", padx=18, pady=14)
        self.header.pack(fill="x")
        self.heading = tk.Label(self.header, bg="#12334a", fg="white", font=("Segoe UI", 18, "bold"))
        self.heading.pack(side="right", anchor="e")
        self.subheading = tk.Label(self.header, bg="#12334a", fg="#c8d8e3", font=("Segoe UI", 10))
        self.subheading.pack(side="right", padx=18, anchor="e")
        self.lang_btn = ttk.Button(self.header, command=self.toggle_language)
        self.lang_btn.pack(side="left")

        self.toolbar = tk.Frame(self.root, bg="#f2f5f8", padx=12, pady=10)
        self.toolbar.pack(fill="x")
        self.tabs = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        self.tabs.pack(fill="x")
        self.tab_buttons = {}
        for key in TABLES:
            b = ttk.Button(self.tabs, command=lambda k=key: self.select_table(k))
            b.pack(side="right", padx=3, pady=3)
            self.tab_buttons[key] = b

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.toolbar, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="right", padx=4)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh())
        self.search_label = tk.Label(self.toolbar, bg="#f2f5f8")
        self.search_label.pack(side="right", padx=5)
        self.action_buttons = {}
        for key, command in [("add", self.add_record), ("edit", self.edit_record), ("delete", self.delete_record),
                             ("export", self.export_csv), ("backup", self.backup), ("restore", self.restore)]:
            b = ttk.Button(self.toolbar, command=command)
            b.pack(side="left", padx=3)
            self.action_buttons[key] = b

        self.table_frame = tk.Frame(self.root, bg="white", padx=8, pady=8)
        self.table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        self.tree = None
        self.footer = tk.Label(self.root, bg="#12334a", fg="white", font=("Segoe UI", 9), pady=9)
        self.footer.pack(fill="x", side="bottom")
        self.render_text()

    def render_text(self):
        self.root.title(self.t("title"))
        self.heading.config(text=self.t("title"))
        self.subheading.config(text=self.t("subtitle"))
        self.lang_btn.config(text=self.t("language"))
        self.search_label.config(text=self.t("search"))
        for key, b in self.action_buttons.items(): b.config(text=self.t(key))
        for key, b in self.tab_buttons.items(): b.config(text=self.title_for(key))
        self.footer.config(text=self.t("footer"))
        self.refresh()

    def toggle_language(self):
        self.lang = "en" if self.lang == "ar" else "ar"
        self.render_text()

    def select_table(self, key):
        self.current_table = key
        self.search_var.set("")
        self.refresh()

    def refresh(self):
        if not hasattr(self, "table_frame"): return
        for w in self.table_frame.winfo_children(): w.destroy()
        cols = self.fields()
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=145, minwidth=90, anchor="center")
        y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        x = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        y.grid(row=0, column=1, sticky="ns")
        x.grid(row=1, column=0, sticky="ew")
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)
        rows = self.conn.execute(f'SELECT * FROM "{self.current_table}" ORDER BY id DESC').fetchall()
        query = self.search_var.get().strip().lower()
        for row in rows:
            values = row[1:]
            if query and query not in " ".join(str(v or "") for v in values).lower(): continue
            self.tree.insert("", "end", iid=str(row[0]), values=values)

    def record_dialog(self, record_id=None):
        cols = self.fields()
        old = None
        if record_id:
            old = self.conn.execute(f'SELECT * FROM "{self.current_table}" WHERE id=?', (record_id,)).fetchone()
        win = tk.Toplevel(self.root)
        win.title(self.t("edit") if old else self.t("new"))
        win.transient(self.root); win.grab_set()
        win.geometry("540x650")
        win.configure(bg="#f4f6f8")
        canvas = tk.Canvas(win, bg="#f4f6f8", highlightthickness=0)
        scroll = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="#f4f6f8", padx=18, pady=14)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw", width=500)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        vars_ = []
        for i, col in enumerate(cols):
            tk.Label(inner, text=col, bg="#f4f6f8", font=("Segoe UI", 10, "bold"), anchor="e").pack(fill="x", pady=(7,2))
            v = tk.StringVar(value=(old[i+1] if old and old[i+1] else ""))
            ent = ttk.Entry(inner, textvariable=v, justify="right" if self.lang=="ar" else "left")
            ent.pack(fill="x", ipady=5)
            vars_.append(v)
        def save():
            values = [v.get().strip() for v in vars_]
            if self.current_table == "people" and not values[0]:
                messagebox.showwarning(self.t("title"), self.t("required"), parent=win); return
            quoted = ", ".join('"%s"' % c.replace('"','""') for c in cols)
            if record_id:
                assignments = ", ".join(f'"{c}"=?' for c in cols)
                self.conn.execute(f'UPDATE "{self.current_table}" SET {assignments} WHERE id=?', (*values, record_id))
            else:
                marks = ",".join("?" for _ in cols)
                self.conn.execute(f'INSERT INTO "{self.current_table}" ({quoted}) VALUES ({marks})', values)
            self.conn.commit(); win.destroy(); self.refresh()
            messagebox.showinfo(self.t("title"), self.t("saved"))
        bar = tk.Frame(inner, bg="#f4f6f8"); bar.pack(fill="x", pady=18)
        ttk.Button(bar, text=self.t("save"), command=save).pack(side="right", padx=4)
        ttk.Button(bar, text=self.t("cancel"), command=win.destroy).pack(side="right", padx=4)

    def selected_id(self):
        if not self.tree: return None
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def add_record(self): self.record_dialog()
    def edit_record(self):
        rid = self.selected_id()
        if rid is None: messagebox.showinfo(self.t("title"), self.t("select")); return
        self.record_dialog(rid)
    def delete_record(self):
        rid = self.selected_id()
        if rid is None: messagebox.showinfo(self.t("title"), self.t("select")); return
        if messagebox.askyesno(self.t("title"), self.t("confirm")):
            self.conn.execute(f'DELETE FROM "{self.current_table}" WHERE id=?', (rid,))
            self.conn.commit(); self.refresh()
            messagebox.showinfo(self.t("title"), self.t("deleted"))

    def backup(self):
        path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite database","*.db")], initialfile="personnel_backup.db")
        if not path: return
        self.conn.commit()
        shutil.copy2(self.db_path, path)
        messagebox.showinfo(self.t("title"), self.t("backup_ok"))

    def restore(self):
        path = filedialog.askopenfilename(filetypes=[("SQLite database","*.db"),("All files","*.*")])
        if not path: return
        if not messagebox.askyesno(self.t("title"), self.t("confirm")): return
        self.conn.close()
        shutil.copy2(path, self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        messagebox.showinfo(self.t("title"), self.t("restore_ok"))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile=f"{self.current_table}.csv")
        if not path: return
        cols = self.fields()
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f); writer.writerow(cols)
            for item in self.tree.get_children(): writer.writerow(self.tree.item(item, "values"))
        messagebox.showinfo(self.t("title"), "CSV exported." if self.lang=="en" else "تم تصدير الملف.")

    def close(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonnelApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
