import tkinter as tk
from tkinter import messagebox

#  KNOWLEDGE BASE
database_kerusakan = {
    "RAM Rusak": {
        "gejala"  : ["blue_screen", "bunyi_beep", "ram_tidak_terdeteksi"],
        "solusi"  : "Bersihkan pin RAM dengan penghapus, lalu pasang kembali dengan kuat."
    },
    "Overheat (CPU Kepanasan)": {
        "gejala"  : ["mati_mendadak", "sangat_panas", "kipas_berisik"],
        "solusi"  : "Bersihkan debu heatsink dan ganti thermal paste pada prosesor."
    },
    "Hardisk Rusak / Corrupt": {
        "gejala"  : ["file_hilang", "bunyi_klik", "disk_tidak_terdeteksi"],
        "solusi"  : "Backup data segera, jalankan chkdsk /f /r, ganti hardisk jika perlu."
    },
    "VGA / GPU Bermasalah": {
        "gejala"  : ["layar_bergaris", "resolusi_error", "artefak_visual"],
        "solusi"  : "Update atau reinstall driver VGA dari situs resmi NVIDIA/AMD/Intel."
    },
    "PSU (Power Supply) Lemah": {
        "gejala"  : ["tidak_menyala", "mati_hidup_sendiri", "bau_terbakar"],
        "solusi"  : "Ukur tegangan PSU dengan multimeter, ganti PSU jika voltase tidak stabil."
    },
    "OS (Sistem Operasi) Corrupt": {
        "gejala"  : ["gagal_booting", "sering_crash", "blue_screen"],
        "solusi"  : "Jalankan sfc /scannow di CMD, atau lakukan install ulang sistem operasi."
    },
}

#  DAFTAR SEMUA GEJALA
semua_gejala = {
    "blue_screen"          : "Layar biru (Blue Screen of Death)",
    "bunyi_beep"           : "Bunyi beep berulang saat dinyalakan",
    "ram_tidak_terdeteksi" : "RAM tidak terdeteksi / kapasitas berkurang",
    "mati_mendadak"        : "Komputer mati mendadak sendiri",
    "sangat_panas"         : "Badan laptop/PC sangat panas",
    "kipas_berisik"        : "Kipas berbunyi berisik / tidak berputar",
    "file_hilang"          : "File sering hilang / corrupt tiba-tiba",
    "bunyi_klik"           : "Bunyi 'klik-klik' dari dalam casing",
    "disk_tidak_terdeteksi": "Hardisk tidak terbaca di BIOS",
    "layar_bergaris"       : "Tampilan layar bergaris / kacau",
    "resolusi_error"       : "Resolusi layar tidak bisa diubah",
    "artefak_visual"       : "Muncul kotak-kotak aneh di layar",
    "tidak_menyala"        : "Komputer tidak bisa menyala sama sekali",
    "mati_hidup_sendiri"   : "Komputer mati lalu menyala sendiri",
    "bau_terbakar"         : "Ada bau terbakar dari dalam casing",
    "gagal_booting"        : "Tidak bisa masuk ke sistem operasi",
    "sering_crash"         : "Aplikasi sering crash / not responding",
}

#  MESIN INFERENSI
def diagnosa(gejala_dipilih):
    hasil = []
    for nama, data in database_kerusakan.items():
        cocok = [g for g in data["gejala"] if g in gejala_dipilih]
        if len(cocok) >= 1:  # minimal 1 gejala cocok
            hasil.append((nama, data["solusi"], len(cocok)))
    hasil.sort(key=lambda x: x[2], reverse=True)
    return hasil

#  GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Diagnosa Komputer")
        self.root.geometry("520x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F5")

        self.var_gejala = {kode: tk.BooleanVar() for kode in semua_gejala}
        self._build()

    def _build(self):
        # JUDUL
        tk.Label(
            self.root, text="Sistem Pakar Diagnosa Kerusakan Komputer",
            font=("Arial", 13, "bold"), bg="#F5F5F5"
        ).pack(pady=(16, 2))

        tk.Label(
            self.root, text="Centang gejala yang dialami, lalu klik Diagnosa",
            font=("Arial", 9), bg="#F5F5F5", fg="gray"
        ).pack(pady=(0, 10))

        # FRAME GEJALA (scrollable)
        frame_luar = tk.LabelFrame(
            self.root, text="  Daftar Gejala  ",
            font=("Arial", 10), bg="#F5F5F5", padx=10, pady=8
        )
        frame_luar.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        canvas = tk.Canvas(frame_luar, bg="#F5F5F5", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_luar, orient="vertical", command=canvas.yview)
        self.frame_cb = tk.Frame(canvas, bg="#F5F5F5")

        self.frame_cb.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.frame_cb, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        for kode, label in semua_gejala.items():
            tk.Checkbutton(
                self.frame_cb, text=label,
                variable=self.var_gejala[kode],
                font=("Arial", 10), bg="#F5F5F5",
                anchor="w", cursor="hand2"
            ).pack(fill="x", pady=2)

        # TOMBOL
        btn_frame = tk.Frame(self.root, bg="#F5F5F5")
        btn_frame.pack(pady=(0, 16))

        tk.Button(
            btn_frame, text="🔍 Diagnosa", width=14,
            font=("Arial", 10, "bold"), bg="#2563EB", fg="white",
            relief="flat", cursor="hand2", pady=6,
            command=self._diagnosa
        ).pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="🔄 Reset", width=10,
            font=("Arial", 10), bg="#E5E7EB", fg="#374151",
            relief="flat", cursor="hand2", pady=6,
            command=self._reset
        ).pack(side="left", padx=6)

    def _diagnosa(self):
        dipilih = [k for k, v in self.var_gejala.items() if v.get()]

        if not dipilih:
            messagebox.showwarning("Peringatan", "Pilih minimal 1 gejala terlebih dahulu!")
            return

        hasil = diagnosa(dipilih)

        if not hasil:
            messagebox.showinfo(
                "Hasil Diagnosa",
                "❓ Kerusakan tidak dapat diidentifikasi.\n\n"
                "Coba pilih gejala lain atau bawa ke teknisi."
            )
        else:
            pesan = ""
            for i, (nama, solusi, _) in enumerate(hasil, 1):
                pesan += f"{i}. {nama}\n"
                pesan += f"   ➤ {solusi}\n\n"
            messagebox.showinfo("Hasil Diagnosa", pesan.strip())

    def _reset(self):
        for var in self.var_gejala.values():
            var.set(False)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
