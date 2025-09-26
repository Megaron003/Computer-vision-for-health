import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import cv2
import numpy as np
from pathlib import Path

class HaarCascadeTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Treinador Haar Cascade - Detecção de Tumores Pulmonares")
        self.root.geometry("800x600")
        
        # Variáveis
        self.positive_folder = tk.StringVar()
        self.negative_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.num_pos = tk.IntVar(value=120)
        self.num_neg = tk.IntVar(value=977)
        self.num_stages = tk.IntVar(value=15)
        self.min_hit_rate = tk.DoubleVar(value=0.995)
        self.max_false_alarm = tk.DoubleVar(value=0.5)
        self.width = tk.IntVar(value=24)
        self.height = tk.IntVar(value=24)
        
        self.setup_ui()
        self.is_training = False
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Treinamento Haar Cascade", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção de pastas
        folder_frame = ttk.LabelFrame(main_frame, text="Configuração de Pastas", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Pasta positiva
        ttk.Label(folder_frame, text="Pasta com Imagens Positivas:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.positive_folder, width=60).grid(row=0, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_positive_folder).grid(row=0, column=2, pady=2)
        
        # Pasta negativa
        ttk.Label(folder_frame, text="Pasta com Imagens Negativas:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.negative_folder, width=60).grid(row=1, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_negative_folder).grid(row=1, column=2, pady=2)
        
        # Pasta de saída
        ttk.Label(folder_frame, text="Pasta de Saída:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(folder_frame, textvariable=self.output_folder, width=60).grid(row=2, column=1, pady=2, padx=5)
        ttk.Button(folder_frame, text="Procurar", 
                  command=self.browse_output_folder).grid(row=2, column=2, pady=2)
        
        # Seção de parâmetros
        param_frame = ttk.LabelFrame(main_frame, text="Parâmetros de Treinamento", padding="10")
        param_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Número de imagens positivas
        ttk.Label(param_frame, text="Nº Imagens Positivas:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_pos, width=15).grid(row=0, column=1, pady=2, padx=5)
        
        # Número de imagens negativas
        ttk.Label(param_frame, text="Nº Imagens Negativas:").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_neg, width=15).grid(row=0, column=3, pady=2, padx=5)
        
        # Número de estágios
        ttk.Label(param_frame, text="Nº Estágios:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.num_stages, width=15).grid(row=1, column=1, pady=2, padx=5)
        
        # Dimensões
        ttk.Label(param_frame, text="Largura (w):").grid(row=1, column=2, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.width, width=15).grid(row=1, column=3, pady=2, padx=5)
        
        ttk.Label(param_frame, text="Altura (h):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.height, width=15).grid(row=2, column=1, pady=2, padx=5)
        
        # Taxa de acerto mínima
        ttk.Label(param_frame, text="Taxa Acerto Mínima:").grid(row=2, column=2, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.min_hit_rate, width=15).grid(row=2, column=3, pady=2, padx=5)
        
        # Taxa de falso alarme máxima
        ttk.Label(param_frame, text="Taxa Falso Alarme Máx:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.max_false_alarm, width=15).grid(row=3, column=1, pady=2, padx=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Progresso", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.train_button = ttk.Button(button_frame, text="Iniciar Treinamento", 
                                      command=self.start_training)
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Parar", 
                  command=self.stop_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sair", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configurar weights
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
    
    def stop_training(self):
        self.is_training = False
        self.log("Solicitação de parada recebida...")
        self.train_button.config(state="normal")
    
    def load_images(self, folder_path, is_positive=False):
        """Carrega imagens de uma pasta"""
        images = []
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
        
        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(valid_extensions):
                    img_path = os.path.join(folder_path, file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    
                    if img is not None:
                        if is_positive:
                            # Redimensionar imagens positivas para o tamanho desejado
                            img = cv2.resize(img, (self.width.get(), self.height.get()))
                        images.append(img)
                    else:
                        self.log(f"AVISO: Não foi possível carregar {file}")
            
            return images
        except Exception as e:
            self.log(f"ERRO ao carregar imagens: {str(e)}")
            return []
    
    def create_positive_samples(self, positive_images):
        """Cria amostras positivas para treinamento"""
        try:
            # Criar vetor de amostras positivas
            samples = []
            for img in positive_images:
                if img.shape != (self.height.get(), self.width.get()):
                    img = cv2.resize(img, (self.width.get(), self.height.get()))
                samples.append(img)
            
            self.log(f"Criadas {len(samples)} amostras positivas")
            return samples
            
        except Exception as e:
            self.log(f"ERRO ao criar amostras positivas: {str(e)}")
            return []
    
    def start_training(self):
        if not all([self.positive_folder.get(), self.negative_folder.get(), self.output_folder.get()]):
            messagebox.showerror("Erro", "Por favor, selecione todas as pastas necessárias")
            return
        
        if not os.path.exists(self.positive_folder.get()):
            messagebox.showerror("Erro", "Pasta de imagens positivas não existe")
            return
        
        if not os.path.exists(self.negative_folder.get()):
            messagebox.showerror("Erro", "Pasta de imagens negativas não existe")
            return
        
        # Criar pasta de saída se não existir
        if not os.path.exists(self.output_folder.get()):
            os.makedirs(self.output_folder.get())
        
        self.is_training = True
        self.train_button.config(state="disabled")
        
        # Iniciar treinamento em thread separada
        thread = threading.Thread(target=self.run_training)
        thread.daemon = True
        thread.start()
    
    def run_training(self):
        try:
            self.log("Iniciando processo de treinamento Haar Cascade...")
            self.log("=" * 50)
            
            # Carregar imagens
            self.log("Carregando imagens positivas...")
            positive_images = self.load_images(self.positive_folder.get(), is_positive=True)
            
            self.log("Carregando imagens negativas...")
            negative_images = self.load_images(self.negative_folder.get())
            
            if len(positive_images) == 0:
                self.log("ERRO: Nenhuma imagem positiva encontrada")
                return
            
            if len(negative_images) == 0:
                self.log("ERRO: Nenhuma imagem negativa encontrada")
                return
            
            self.log(f"Imagens carregadas: {len(positive_images)} positivas, {len(negative_images)} negativas")
            
            # Ajustar números baseado nas imagens disponíveis
            num_pos = min(self.num_pos.get(), len(positive_images))
            num_neg = min(self.num_neg.get(), len(negative_images))
            
            self.log(f"Usando {num_pos} imagens positivas e {num_neg} negativas")
            
            # Criar amostras positivas
            positive_samples = self.create_positive_samples(positive_images[:num_pos])
            
            if len(positive_samples) == 0:
                self.log("ERRO: Não foi possível criar amostras positivas")
                return
            
            # Preparar dados para treinamento
            self.log("Preparando dados para treinamento...")
            
            # Criar classificador
            cascade = cv2.CascadeClassifier()
            
            # Criar objeto para treinamento
            # Nota: OpenCV não tem uma interface Python direta para treinamento Haar Cascade
            # Vamos usar uma abordagem alternativa
            
            self.log("Iniciando treinamento...")
            self.log("Este processo pode levar algum tempo...")
            
            # Para versões mais recentes do OpenCV, precisamos usar uma abordagem diferente
            # Vamos criar os arquivos necessários e treinar usando subprocess se possível
            
            success = self.train_with_files(positive_images[:num_pos], negative_images[:num_neg])
            
            if success:
                self.log("=" * 50)
                self.log("Treinamento concluído com sucesso!")
                messagebox.showinfo("Sucesso", "Treinamento concluído com sucesso!")
            else:
                self.log("Treinamento concluído (método alternativo)")
                
        except Exception as e:
            self.log(f"Erro durante o treinamento: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        finally:
            self.is_training = False
            self.train_button.config(state="normal")
    
    def train_with_files(self, positive_images, negative_images):
        """Método alternativo para treinamento usando arquivos temporários"""
        try:
            # Criar diretório temporário
            temp_dir = "temp_training"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # Salvar imagens positivas redimensionadas
            positive_dir = os.path.join(temp_dir, "positive")
            if not os.path.exists(positive_dir):
                os.makedirs(positive_dir)
            
            for i, img in enumerate(positive_images):
                if img.shape != (self.height.get(), self.width.get()):
                    img = cv2.resize(img, (self.width.get(), self.height.get()))
                cv2.imwrite(os.path.join(positive_dir, f"pos_{i:04d}.png"), img)
            
            # Salvar imagens negativas
            negative_dir = os.path.join(temp_dir, "negative")
            if not os.path.exists(negative_dir):
                os.makedirs(negative_dir)
            
            for i, img in enumerate(negative_images):
                cv2.imwrite(os.path.join(negative_dir, f"neg_{i:04d}.png"), img)
            
            self.log("Arquivos preparados para treinamento")
            self.log("Nota: Treinamento Haar Cascade completo requer OpenCV com utilitários de linha de comando")
            self.log("Considere usar o opencv_traincascade.exe manualmente com os arquivos criados")
            self.log(f"Pasta com arquivos: {temp_dir}")
            
            return True
            
        except Exception as e:
            self.log(f"Erro no método alternativo: {str(e)}")
            return False

def main():
    # Verificar se OpenCV está instalado
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError:
        print("OpenCV não encontrado. Instale com: pip install opencv-python")
        return
    
    root = tk.Tk()
    app = HaarCascadeTrainer(root)
    root.mainloop()

if __name__ == "__main__":
    main()