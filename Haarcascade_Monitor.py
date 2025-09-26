# monitorar_treinamento.py
import os
import time
import subprocess

def executar_treinamento_com_monitoramento():
    print("🎯 INICIANDO TREINAMENTO HAAR CASCADE")
    print("⏰ Este processo pode levar VÁRIAS HORAS ou DIAS")
    print("📊 Acompanhe o progresso abaixo:\n")
    
    comando = [
        r"C:\opencv\build\x64\vc15\bin\opencv_traincascade.exe",
        "-data", "classifier",
        "-vec", "positives.vec", 
        "-bg", "bg.txt",
        "-numPos", "120",
        "-numNeg", "977", 
        "-numStages", "10",
        "-w", "512",
        "-h", "512",
        "-featureType", "HAAR"
    ]
    
    try:
        # Executar o processo
        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, text=True, 
                                  encoding='utf-8', errors='ignore')
        
        # Monitorar a saída em tempo real
        while True:
            output = processo.stdout.readline()
            if output == '' and processo.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Verificar resultado
        if processo.returncode == 0:
            print("\n🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
            if os.path.exists("classifier/cascade.xml"):
                print("📁 Classificador salvo em: classifier/cascade.xml")
                print("\n🚀 PARA USAR O CLASSIFICADOR:")
                print("""
import cv2

# Carregar o classificador treinado
classifier = cv2.CascadeClassifier('classifier/cascade.xml')

# Usar para detecção
imagem = cv2.imread('sua_imagem.jpg')
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
tumores = classifier.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5)

# Desenhar retângulos nos tumores detectados
for (x, y, w, h) in tumores:
    cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)
                """)
        else:
            print(f"\n❌ Treinamento falhou com código: {processo.returncode}")
            
    except KeyboardInterrupt:
        print("\n⏹️ Treinamento interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = ['positives.vec', 'bg.txt']
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo necessário não encontrado: {arquivo}")
            exit(1)
    
    print("✅ Todos os arquivos necessários encontrados")
    executar_treinamento_com_monitoramento()