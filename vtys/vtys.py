import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# veritabanı bağlantısı:
def connect_to_db():
    return psycopg2.connect(
        database="kütüphaneOtomasyon",
        user="postgres",
        password="Elifarzu1.",
        host="localhost",
        port="5432"
    )

#anasayfa
def main():
    root = tk.Tk()
    root.title("Kütüphane Otomasyonu")
    root.geometry("600x400")

    def open_member_page():
        MemberPage(root)

    def open_book_page():
        BookPage(root)

    def open_lend_page():
        LendPage(root)

    def open_personnel_page():
        PersonnelPage(root)

    def open_add_book_page():
        AddBookPage(root)

    tk.Label(root, text="Kütüphane Otomasyonu", font=("Arial", 20)).pack(pady=20)

    tk.Button(root, text="Üye Ekle", width=20, command=open_member_page).pack(pady=5)
    tk.Button(root, text="Kitap Görüntüle", width=20, command=open_book_page).pack(pady=5)
    tk.Button(root, text="Ödünç Ver", width=20, command=open_lend_page).pack(pady=5)
    tk.Button(root, text="Personel Ekle", width=20, command=open_personnel_page).pack(pady=5)
    tk.Button(root, text="Kitap Ekle", width=20, command=open_add_book_page).pack(pady=5)

    root.mainloop()

# üyegiriş
class MemberPage:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Üye Ekle")
        self.master.geometry("400x300")

        tk.Label(self.master, text="Ad:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Soyad:").grid(row=1, column=0, padx=10, pady=10)
        self.surname_entry = tk.Entry(self.master)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Kaydet", command=self.save_member).grid(row=3, column=0, columnspan=2, pady=20)

    def save_member(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO uye (ad, soyad, mail) VALUES (%s, %s, %s)", (name, surname, email))

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarı", "Üye başarıyla kaydedildi.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

# mevcut kitap liste
class BookPage:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Kitaplar")
        self.master.geometry("600x400")

        self.tree = ttk.Treeview(self.master, columns=("#1", "#2", "#3"), show="headings")
        self.tree.heading("#1", text="Kitap No")
        self.tree.heading("#2", text="Yazar İsim")
        self.tree.heading("#3", text="Sayfa Sayısı")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_books()

    def load_books(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT kitapNo, yazarİsim, sayfaSayisi FROM kitap")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

#ödünç işlemleri
class LendPage:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Ödünç Ver")
        self.master.geometry("400x300")

        tk.Label(self.master, text="Üye No:").grid(row=0, column=0, padx=10, pady=10)
        self.member_id_entry = tk.Entry(self.master)
        self.member_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Kitap No:").grid(row=1, column=0, padx=10, pady=10)
        self.book_id_entry = tk.Entry(self.master)
        self.book_id_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Kaydet", command=self.lend_book).grid(row=2, column=0, columnspan=2, pady=20)

    def lend_book(self):
        member_id = self.member_id_entry.get()
        book_id = self.book_id_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO odunc (kisiNo, odunNo) VALUES (%s, %s)", (member_id, book_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarı", "Ödünç başarıyla kaydedildi.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

# personel sayfası
class PersonnelPage:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Personel Ekle")
        self.master.geometry("400x300")

        tk.Label(self.master, text="Ad:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Soyad:").grid(row=1, column=0, padx=10, pady=10)
        self.surname_entry = tk.Entry(self.master)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Kaydet", command=self.save_personnel).grid(row=2, column=0, columnspan=2, pady=20)

    def save_personnel(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO personel (ad, soyad) VALUES (%s, %s)", (name, surname))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarı", "Personel başarıyla kaydedildi.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

# Add Book Page
class AddBookPage:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Kitap Ekle")
        self.master.geometry("400x300")

        tk.Label(self.master, text="Kitap Adı:").grid(row=0, column=0, padx=10, pady=10)
        self.book_name_entry = tk.Entry(self.master)
        self.book_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Yazar İsim:").grid(row=1, column=0, padx=10, pady=10)
        self.author_entry = tk.Entry(self.master)
        self.author_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Sayfa Sayısı:").grid(row=2, column=0, padx=10, pady=10)
        self.page_count_entry = tk.Entry(self.master)
        self.page_count_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Kaydet", command=self.save_book).grid(row=3, column=0, columnspan=2, pady=20)

    def save_book(self):
        book_name = self.book_name_entry.get()
        author = self.author_entry.get()
        page_count = self.page_count_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kitap (ad, yazarİsim, sayfaSayisi) VALUES (%s, %s, %s)", (book_name, author, page_count))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Başarı", "Kitap başarıyla kaydedildi.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    main()
