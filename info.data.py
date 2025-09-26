# corrigir_info_dat.py
import os
import re

def corrigir_info_dat():
    print("=== CORRIGINDO ARQUIVO info.dat ===\n")
    
    # Caminhos corretos
    pasta_positivas = r"C:\Users\Guilherme\Desktop\Computer_Vision_For_Health\Haarcascade_Bengin\p"
    pasta_negativas = r"C:\Users\Guilherme\Desktop\Computer_Vision_For_Health\Haarcascade_Bengin\n"
    
    # Verificar se as pastas existem
    if not os.path.exists(pasta_positivas):
        print(f"❌ Pasta de positivas não existe: {pasta_positivas}")
        return False
    
    if not os.path.exists(pasta_negativas):
        print(f"❌ Pasta de negativas não existe: {pasta_negativas}")
        return False
    
    # Listar imagens positivas
    extensoes = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    imagens_positivas = []
    
    for arquivo in os.listdir(pasta_positivas):
        if arquivo.lower().endswith(extensoes):
            caminho_completo = os.path.join(pasta_positivas, arquivo)
            imagens_positivas.append(caminho_completo)
    
    print(f"📁 Encontradas {len(imagens_positivas)} imagens positivas")
    
    if len(imagens_positivas) == 0:
        print("❌ Nenhuma imagem positiva encontrada!")
        return False
    
    # Criar novo info.dat com caminhos absolutos
    with open('info.dat', 'w', encoding='utf-8') as f:
        for caminho_imagem in imagens_positivas:
            # Formato: caminho_imagem quantidade_obj x y width height
            f.write(f"{caminho_imagem} 1 0 0 512 512\n")
    
    print("✅ info.dat criado com caminhos absolutos")
    print("📝 Primeiras linhas do novo arquivo:")
    
    with open('info.dat', 'r', encoding='utf-8') as f:
        for i, linha in enumerate(f.readlines()[:3]):
            print(f"   {i+1}: {linha.strip()}")
    
    # Também criar/corrigir o bg.txt
    imagens_negativas = []
    for arquivo in os.listdir(pasta_negativas):
        if arquivo.lower().endswith(extensoes):
            caminho_completo = os.path.join(pasta_negativas, arquivo)
            imagens_negativas.append(caminho_completo)
    
    print(f"\n📁 Encontradas {len(imagens_negativas)} imagens negativas")
    
    with open('bg.txt', 'w', encoding='utf-8') as f:
        for caminho_imagem in imagens_negativas:
            f.write(f"{caminho_imagem}\n")
    
    print("✅ bg.txt criado com caminhos absolutos")
    return True

def verificar_arquivos():
    """Verifica se os arquivos foram criados corretamente"""
    print("\n=== VERIFICAÇÃO FINAL ===")
    
    if os.path.exists('info.dat'):
        with open('info.dat', 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        print(f"✅ info.dat: {len(linhas)} linhas")
        
        # Verificar se os caminhos existem
        caminho_valido = 0
        for linha in linhas[:5]:  # Verificar apenas as primeiras 5
            caminho = linha.split()[0]
            if os.path.exists(caminho):
                caminho_valido += 1
        
        print(f"   {caminho_valido}/5 primeiros caminhos são válidos")
    
    if os.path.exists('bg.txt'):
        with open('bg.txt', 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        print(f"✅ bg.txt: {len(linhas)} linhas")

if __name__ == "__main__":
    if corrigir_info_dat():
        verificar_arquivos()
        
        print("\n🎯 AGORA EXECUTE:")
        print(r'C:\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info info.dat -num 120 -w 512 -h 512 -vec positives.vec')
    else:
        print("❌ Correção falhou")