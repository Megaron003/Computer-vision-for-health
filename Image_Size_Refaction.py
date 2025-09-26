from PIL import Image
import os
from pathlib import Path

def redimensionar_imagens_avancado(pasta_origem, pasta_destino, largura=512, altura=512, 
                                 manter_proporcao=True, preencher_fundo=False, cor_fundo='white'):
    """
    Redimensiona imagens com opções avançadas
    
    Args:
        pasta_origem (str): Pasta com imagens originais
        pasta_destino (str): Pasta para imagens redimensionadas
        largura (int): Largura desejada
        altura (int): Altura desejada
        manter_proporcao (bool): Se True, mantém proporção original
        preencher_fundo (bool): Se True, preenche áreas vazias com cor de fundo
        cor_fundo (str): Cor para preenchimento ('white', 'black', etc.)
    """
    
    # Criar pasta de destino
    Path(pasta_destino).mkdir(parents=True, exist_ok=True)
    
    # Extensões suportadas
    extensoes_suportadas = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
    
    for arquivo in Path(pasta_origem).iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_suportadas:
            try:
                with Image.open(arquivo) as img:
                    if manter_proporcao:
                        # Redimensionar mantendo proporção
                        img_redimensionada = redimensionar_com_proporcao(img, largura, altura, preencher_fundo, cor_fundo)
                    else:
                        # Redimensionar forçando 512x512 (pode distorcer)
                        img_redimensionada = img.resize((largura, altura), Image.Resampling.LANCZOS)
                    
                    # Salvar imagem
                    caminho_destino = Path(pasta_destino) / f"{arquivo.stem}_512x512{arquivo.suffix}"
                    img_redimensionada.save(caminho_destino, optimize=True, quality=95)
                    
                    print(f"✓ {arquivo.name} → {caminho_destino.name}")
                    
            except Exception as e:
                print(f"✗ Erro em {arquivo.name}: {e}")

def redimensionar_com_proporcao(img, largura_alvo, altura_alvo, preencher=False, cor_fundo='white'):
    """
    Redimensiona imagem mantendo proporção
    """
    # Calcular ratio de redimensionamento
    ratio = min(largura_alvo/img.width, altura_alvo/img.height)
    nova_largura = int(img.width * ratio)
    nova_altura = int(img.height * ratio)
    
    # Redimensionar
    img_redimensionada = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
    
    if preencher:
        # Criar nova imagem com fundo
        nova_imagem = Image.new('RGB', (largura_alvo, altura_alvo), cor_fundo)
        # Centralizar a imagem redimensionada
        x = (largura_alvo - nova_largura) // 2
        y = (altura_alvo - nova_altura) // 2
        nova_imagem.paste(img_redimensionada, (x, y))
        return nova_imagem
    else:
        return img_redimensionada

# Interface de uso
def main():
    print("=== REDIMENSIONADOR DE IMAGENS 512x512 ===")
    
    pasta_origem = input("Pasta com as imagens: ").strip()
    pasta_destino = input("Pasta de destino: ").strip()
    
    if not pasta_destino:
        pasta_destino = pasta_origem + "_redimensionadas"
    
    print("\nOpções de redimensionamento:")
    print("1. Redimensionar forçando 512x512 (pode distorcer)")
    print("2. Manter proporção e cortar para 512x512")
    print("3. Manter proporção com fundo branco")
    
    opcao = input("Escolha (1/2/3) [padrão: 1]: ").strip()
    
    if opcao == "2":
        redimensionar_imagens_avancado(pasta_origem, pasta_destino, manter_proporcao=True, preencher_fundo=False)
    elif opcao == "3":
        redimensionar_imagens_avancado(pasta_origem, pasta_destino, manter_proporcao=True, preencher_fundo=True)
    else:
        redimensionar_imagens_avancado(pasta_origem, pasta_destino, manter_proporcao=False)

if __name__ == "__main__":
    main()