import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import cv2
import numpy as np

class HaarCascadeTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Comandos Haar Cascade")
        self.root.geometry("800x600")
        
        # Variáveis
        self.positive_folder = tk.StringVar()
        self.negative_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.num_pos = tk.IntVar(value=120)
        self.num_neg = tk.IntVar(value=977)
        self.num_stages = tk.IntVar(value=10)
        self.width = tk.IntVar(value=50)
        self.height = tk.IntVar(value=50)
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Gerador de Comandos Haar Cascade", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção de pastas
        folder_frame = ttk.LabelFrame(main_frame, text="Configuração de Pastas", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(folder_frame, text="Pasta com Imagens Positivas:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.positive_folder, width=60).grid(row=0, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_positive_folder).grid(row=0, column=2, pady=2)
        
        ttk.Label(folder_frame, text="Pasta com Imagens Negativas:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.negative_folder, width=60).grid(row=1, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_negative_folder).grid(row=1, column=2, pady=2)
        
        ttk.Label(folder_frame, text="Pasta de Saída:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.output_folder, width=60).grid(row=2, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_output_folder).grid(row=2, column=2, pady=2)
        
        # Parâmetros
        param_frame = ttk.LabelFrame(main_frame, text="Parâmetros", padding="10")
        param_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(param_frame, text="Nº Positivas:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_pos, width=10).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(param_frame, text="Nº Negativas:").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_neg, width=10).grid(row=0, column=3, pady=2, padx=5)
        
        ttk.Label(param_frame, text="Nº Estágios:").grid(row=0, column=4, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_stages, width=10).grid(row=0, column=5, pady=2, padx=5)
        
        ttk.Label(param_frame, text="Largura:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.width, width=10).grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(param_frame, text="Altura:").grid(row=1, column=2, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.height, width=10).grid(row=1, column=3, pady=2, padx=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Comandos e Instruções", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Gerar Arquivos e Comandos", 
                  command=self.generate_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sair", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def browse_positive_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta com imagens positivas")
        if folder:
            self.positive_folder.set(folder)
            
    def browse_negative_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta com imagens negativas")
        if folder:
            self.negative_folder.set(folder)
            
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta de saída")
        if folder:
            self.output_folder.set(folder)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def generate_files(self):
        try:
            if not all([self.positive_folder.get(), self.negative_folder.get(), self.output_folder.get()]):
                messagebox.showerror("Erro", "Selecione todas as pastas")
                return
            
            self.log("=== GERANDO ARQUIVOS PARA TREINAMENTO HAAR CASCADE ===\n")
            
            # 1. Criar info.dat para imagens positivas
            self.log("1. Criando info.dat para imagens positivas...")
            positive_files = []
            for file in os.listdir(self.positive_folder.get()):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    positive_files.append(file)
            
            with open('info.dat', 'w') as f:
                for img_file in positive_files:
                    f.write(f"{os.path.join(self.positive_folder.get(), img_file)} 1 0 0 {self.width.get()} {self.height.get()}\n")
            
            self.log(f"   ✓ {len(positive_files)} imagens positivas processadas")
            
            # 2. Criar bg.txt para imagens negativas
            self.log("2. Criando bg.txt para imagens negativas...")
            negative_files = []
            for file in os.listdir(self.negative_folder.get()):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    negative_files.append(file)
            
            with open('bg.txt', 'w') as f:
                for img_file in negative_files:
                    f.write(f"{os.path.join(self.negative_folder.get(), img_file)}\n")
            
            self.log(f"   ✓ {len(negative_files)} imagens negativas processadas")
            
            # 3. Gerar comandos
            self.log("\n3. COMANDOS PARA EXECUTAR NO CMD (como Administrador):\n")
            self.log("="*60)
            
            # Comando para criar samples
            cmd1 = f'opencv_createsamples -info info.dat -num {self.num_pos.get()} -w {self.width.get()} -h {self.height.get()} -vec positives.vec'
            self.log(f"COMANDO 1 (criar .vec):\n{cmd1}\n")
            
            # Comando para treinar
            cmd2 = f'opencv_traincascade -data {self.output_folder.get()} -vec positives.vec -bg bg.txt -numPos {self.num_pos.get()} -numNeg {self.num_neg.get()} -numStages {self.num_stages.get()} -w {self.width.get()} -h {self.height.get()} -featureType HAAR'
            self.log(f"COMANDO 2 (treinar):\n{cmd2}\n")
            
            self.log("="*60)
            self.log("\n4. INSTRUÇÕES:")
            self.log("   a) Baixe o OpenCV completo: https://opencv.org/releases/")
            self.log("   b) Extraia em C:\\opencv")
            self.log("   c) Abra o Prompt de Comando como Administrador")
            self.log("   d) Navegue até a pasta deste script")
            self.log("   e) Execute os comandos acima na ordem")
            self.log("   f) O cascade.xml será salvo na pasta de saída")
            
            messagebox.showinfo("Sucesso", "Arquivos gerados! Verifique as instruções na área de texto.")
            
        except Exception as e:
            self.log(f"ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = tk.Tk()
    app = HaarCascadeTrainer(root)
    root.mainloop()

if __name__ == "__main__":
    main()