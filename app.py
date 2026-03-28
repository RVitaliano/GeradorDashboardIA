# app.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from leitor import ler_planilha
from analisador import analisar_e_sugerir
from dashboard import gerar_figura

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Inteligente com IA")
        self.geometry("1200x750")
        self.df = None
        self.canvas_widget = None

        self._build_ui()

    def _build_ui(self):
        # Painel esquerdo (controles)
        self.painel = ctk.CTkFrame(self, width=260)
        self.painel.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.painel, text="📊 Dashboard IA",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.btn_arquivo = ctk.CTkButton(
            self.painel, text="📁 Selecionar CSV/Excel",
            command=self.selecionar_arquivo)
        self.btn_arquivo.pack(pady=10, padx=15, fill="x")

        self.label_arquivo = ctk.CTkLabel(
            self.painel, text="Nenhum arquivo selecionado",
            wraplength=220, text_color="gray")
        self.label_arquivo.pack(pady=5)

        ctk.CTkLabel(self.painel, text="Observações para a IA:").pack(pady=(15, 5))
        self.txt_obs = ctk.CTkTextbox(self.painel, height=80)
        self.txt_obs.pack(padx=15, fill="x")

        self.btn_gerar = ctk.CTkButton(
            self.painel, text="✨ Gerar Dashboard",
            command=self.gerar_dashboard,
            state="disabled", fg_color="#4361ee")
        self.btn_gerar.pack(pady=20, padx=15, fill="x")

        self.label_status = ctk.CTkLabel(
            self.painel, text="", text_color="#4cc9f0", wraplength=220)
        self.label_status.pack(pady=10)

        # Área de insights
        ctk.CTkLabel(self.painel, text="💡 Insights da IA:").pack(pady=(10, 5))
        self.txt_insights = ctk.CTkTextbox(
            self.painel, height=200, state="disabled")
        self.txt_insights.pack(padx=15, fill="both", expand=True, pady=(0, 10))

        # Área principal (gráficos)
        self.area_graficos = ctk.CTkFrame(self)
        self.area_graficos.pack(side="right", fill="both",
                                 expand=True, padx=10, pady=10)

    def selecionar_arquivo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Planilhas", "*.csv *.xlsx *.xls")])
        if path:
            self.df = ler_planilha(path)
            nome = path.split("/")[-1]
            self.label_arquivo.configure(text=f"✅ {nome}", text_color="green")
            self.btn_gerar.configure(state="normal")

    def gerar_dashboard(self):
        self.btn_gerar.configure(state="disabled")
        self.label_status.configure(text="⏳ Consultando IA...")
        threading.Thread(target=self._processar, daemon=True).start()

    def _processar(self):
        try:
            sugestoes = analisar_e_sugerir(self.df)
            fig = gerar_figura(self.df, sugestoes)

            # Atualiza UI na thread principal
            self.after(0, lambda: self._exibir(fig, sugestoes))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro", str(e)))
            self.after(0, lambda: self.btn_gerar.configure(state="normal"))

    def _exibir(self, fig, sugestoes):
        # Remove canvas antigo se existir
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.area_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas_widget = canvas

        # Exibe insights
        self.txt_insights.configure(state="normal")
        self.txt_insights.delete("1.0", "end")
        for g in sugestoes:
            self.txt_insights.insert("end",
                f"📌 {g['titulo']}\n→ {g['insight']}\n\n")
        self.txt_insights.configure(state="disabled")

        self.label_status.configure(text="✅ Dashboard gerado!")
        self.btn_gerar.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()