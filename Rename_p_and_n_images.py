import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import threading
from PIL import Image, ImageTk
import sys

class RenomeadorImagens:
    def __init__(self, root):
        self.root = root
        self.root.title("Renomeador de Imagens - Negative/Positive")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variáveis
        self.pasta_negative = tk.StringVar()
        self.pasta_positive = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Renomeador de Imagens", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção NEGATIVE
        negative_frame = ttk.LabelFrame(main_frame, text="Imagens Negative", padding="10")
        negative_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        negative_frame.columnconfigure(1, weight=1)
        
        ttk.Label(negative_frame, text="Pasta Negative:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        negative_entry = ttk.Entry(negative_frame, textvariable=self.pasta_negative, width=50)
        negative_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(negative_frame, text="Procurar", 
                  command=lambda: self.selecionar_pasta(self.pasta_negative)).grid(row=0, column=2, padx=(10, 0))
        
        ttk.Button(negative_frame, text="Visualizar", 
                  command=lambda: self.visualizar_imagens('negative')).grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(negative_frame, text="Renomear Negative", 
                  command=lambda: self.renomear_imagens('negative')).grid(row=1, column=1, pady=(10, 0))
        
        # Seção POSITIVE
        positive_frame = ttk.LabelFrame(main_frame, text="Imagens Positive", padding="10")
        positive_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        positive_frame.columnconfigure(1, weight=1)
        
        ttk.Label(positive_frame, text="Pasta Positive:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        positive_entry = ttk.Entry(positive_frame, textvariable=self.pasta_positive, width=50)
        positive_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(positive_frame, text="Procurar", 
                  command=lambda: self.selecionar_pasta(self.pasta_positive)).grid(row=0, column=2, padx=(10, 0))
        
        ttk.Button(positive_frame, text="Visualizar", 
                  command=lambda: self.visualizar_imagens('positive')).grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(positive_frame, text="Renomear Positive", 
                  command=lambda: self.renomear_imagens('positive')).grid(row=1, column=1, pady=(10, 0))
        
        # Botão para renomear ambos
        ttk.Button(main_frame, text="RENOMEAR AMBOS", 
                  command=self.renomear_ambos, style="Accent.TButton").grid(row=3, column=0, columnspan=3, pady=20)
        
        # Área de status
        self.status_var = tk.StringVar(value="Pronto para renomear imagens...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Configurar estilo para botão destacado
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        
    def selecionar_pasta(self, variavel_pasta):
        pasta = filedialog.askdirectory(title="Selecione a pasta com as imagens")
        if pasta:
            variavel_pasta.set(pasta)
    
    def visualizar_imagens(self, tipo):
        pasta = self.pasta_negative.get() if tipo == 'negative' else self.pasta_positive.get()
        
        if not pasta or not os.path.exists(pasta):
            messagebox.showwarning("Aviso", f"Selecione uma pasta válida para {tipo}!")
            return
        
        imagens = self.listar_imagens(pasta)
        
        if not imagens:
            messagebox.showinfo("Info", f"Nenhuma imagem encontrada na pasta {tipo}!")
            return
        
        # Criar janela de visualização
        self.criar_janela_visualizacao(tipo, pasta, imagens)
    
    def criar_janela_visualizacao(self, tipo, pasta, imagens):
        janela = tk.Toplevel(self.root)
        janela.title(f"Visualizar Imagens - {tipo.capitalize()}")
        janela.geometry("400x300")
        
        frame = ttk.Frame(janela, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox com scrollbar
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for i, img in enumerate(imagens[:50]):  # Limitar a 50 para performance
            listbox.insert(tk.END, f"{i+1:03d}. {img}")
        
        if len(imagens) > 50:
            listbox.insert(tk.END, f"... e mais {len(imagens) - 50} imagens")
        
        total_label = ttk.Label(frame, text=f"Total de imagens: {len(imagens)}")
        total_label.pack(pady=(10, 0))
    
    def listar_imagens(self, pasta):
        extensoes = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif')
        imagens = []
        
        try:
            for arquivo in os.listdir(pasta):
                if arquivo.lower().endswith(extensoes):
                    imagens.append(arquivo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao acessar a pasta: {e}")
        
        return sorted(imagens)
    
    def renomear_imagens(self, tipo):
        pasta = self.pasta_negative.get() if tipo == 'negative' else self.pasta_positive.get()
        
        if not pasta or not os.path.exists(pasta):
            messagebox.showwarning("Aviso", f"Selecione uma pasta válida para {tipo}!")
            return
        
        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=self.executar_renomeacao, args=(tipo, pasta))
        thread.daemon = True
        thread.start()
    
    def renomear_ambos(self):
        if not self.pasta_negative.get() or not self.pasta_positive.get():
            messagebox.showwarning("Aviso", "Selecione ambas as pastas!")
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_renomeacao_ambos)
        thread.daemon = True
        thread.start()
    
    def executar_renomeacao(self, tipo, pasta):
        self.progress.start()
        self.status_var.set(f"Renomeando imagens {tipo}...")
        
        try:
            imagens = self.listar_imagens(pasta)
            total_renomeadas = 0
            
            for i, nome_arquivo in enumerate(imagens):
                extensao = Path(nome_arquivo).suffix
                novo_nome = f"{tipo}_{i:04d}{extensao}"
                
                caminho_antigo = os.path.join(pasta, nome_arquivo)
                caminho_novo = os.path.join(pasta, novo_nome)
                
                # Renomear arquivo
                os.rename(caminho_antigo, caminho_novo)
                total_renomeadas += 1
            
            self.status_var.set(f"Concluído! {total_renomeadas} imagens {tipo} renomeadas.")
            messagebox.showinfo("Sucesso", f"{total_renomeadas} imagens {tipo} renomeadas com sucesso!")
            
        except Exception as e:
            self.status_var.set(f"Erro ao renomear imagens {tipo}!")
            messagebox.showerror("Erro", f"Erro ao renomear imagens {tipo}: {e}")
        
        finally:
            self.progress.stop()
    
    def executar_renomeacao_ambos(self):
        self.progress.start()
        self.status_var.set("Renomeando ambas as pastas...")
        
        try:
            # Renomear negative
            imagens_negative = self.listar_imagens(self.pasta_negative.get())
            for i, nome_arquivo in enumerate(imagens_negative):
                extensao = Path(nome_arquivo).suffix
                novo_nome = f"negative_{i:04d}{extensao}"
                caminho_antigo = os.path.join(self.pasta_negative.get(), nome_arquivo)
                caminho_novo = os.path.join(self.pasta_negative.get(), novo_nome)
                os.rename(caminho_antigo, caminho_novo)
            
            # Renomear positive
            imagens_positive = self.listar_imagens(self.pasta_positive.get())
            for i, nome_arquivo in enumerate(imagens_positive):
                extensao = Path(nome_arquivo).suffix
                novo_nome = f"positive_{i:04d}{extensao}"
                caminho_antigo = os.path.join(self.pasta_positive.get(), nome_arquivo)
                caminho_novo = os.path.join(self.pasta_positive.get(), novo_nome)
                os.rename(caminho_antigo, caminho_novo)
            
            total = len(imagens_negative) + len(imagens_positive)
            self.status_var.set(f"Concluído! {total} imagens renomeadas.")
            messagebox.showinfo("Sucesso", 
                              f"Renomeação completa!\n"
                              f"Negative: {len(imagens_negative)} imagens\n"
                              f"Positive: {len(imagens_positive)} imagens")
            
        except Exception as e:
            self.status_var.set("Erro ao renomear imagens!")
            messagebox.showerror("Erro", f"Erro durante a renomeação: {e}")
        
        finally:
            self.progress.stop()

def main():
    # Verificar se Pillow está instalado
    try:
        from PIL import Image
    except ImportError:
        print("Instalando biblioteca Pillow...")
        os.system(f"{sys.executable} -m pip install pillow")
    
    root = tk.Tk()
    app = RenomeadorImagens(root)
    root.mainloop()

if __name__ == "__main__":
    main()