from PIL import Image
import os
from pathlib import Path

<<<<<<< HEAD
def redimensionar_imagens_512x512(pasta_origem, pasta_destino, metodo_redimensionamento='preencher', cor_fundo='white'):
    """
    Redimensiona TODAS as imagens para exatamente 512x512 pixels
=======
def redimensionar_imagens_avancado(pasta_origem, pasta_destino, largura=512, altura=512, 
                                 manter_proporcao=True, preencher_fundo=False, cor_fundo='white'):
    """
    Redimensiona imagens com opções avançadas
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3
    
    Args:
        pasta_origem (str): Pasta com imagens originais
        pasta_destino (str): Pasta para imagens redimensionadas
<<<<<<< HEAD
        metodo_redimensionamento (str): 'preencher', 'cortar', ou 'distorcer'
=======
        largura (int): Largura desejada
        altura (int): Altura desejada
        manter_proporcao (bool): Se True, mantém proporção original
        preencher_fundo (bool): Se True, preenche áreas vazias com cor de fundo
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3
        cor_fundo (str): Cor para preenchimento ('white', 'black', etc.)
    """
    
    # Criar pasta de destino
    Path(pasta_destino).mkdir(parents=True, exist_ok=True)
    
    # Extensões suportadas
    extensoes_suportadas = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
    
<<<<<<< HEAD
    # Tamanho fixo
    LARGURA = 512
    ALTURA = 512
    
    imagens_processadas = 0
    erros = 0
    
=======
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3
    for arquivo in Path(pasta_origem).iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_suportadas:
            try:
                with Image.open(arquivo) as img:
<<<<<<< HEAD
                    # Converter para RGB se necessário
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Aplicar redimensionamento conforme o método escolhido
                    if metodo_redimensionamento == 'cortar':
                        img_redimensionada = redimensionar_cortando(img, LARGURA, ALTURA)
                    elif metodo_redimensionamento == 'distorcer':
                        img_redimensionada = redimensionar_distorcendo(img, LARGURA, ALTURA)
                    else:  # 'preencher' (padrão)
                        img_redimensionada = redimensionar_preenchendo(img, LARGURA, ALTURA, cor_fundo)
                    
                    # Garantir que está exatamente 512x512
                    if img_redimensionada.size != (LARGURA, ALTURA):
                        img_redimensionada = img_redimensionada.resize((LARGURA, ALTURA), Image.Resampling.LANCZOS)
=======
                    if manter_proporcao:
                        # Redimensionar mantendo proporção
                        img_redimensionada = redimensionar_com_proporcao(img, largura, altura, preencher_fundo, cor_fundo)
                    else:
                        # Redimensionar forçando 512x512 (pode distorcer)
                        img_redimensionada = img.resize((largura, altura), Image.Resampling.LANCZOS)
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3
                    
                    # Salvar imagem
                    caminho_destino = Path(pasta_destino) / f"{arquivo.stem}_512x512{arquivo.suffix}"
                    img_redimensionada.save(caminho_destino, optimize=True, quality=95)
                    
<<<<<<< HEAD
                    print(f"✓ {arquivo.name} ({img.size[0]}x{img.size[1]}) → 512x512")
                    imagens_processadas += 1
                    
            except Exception as e:
                print(f"✗ Erro em {arquivo.name}: {e}")
                erros += 1
    
    print(f"\n=== RESUMO ===")
    print(f"Imagens processadas: {imagens_processadas}")
    print(f"Erros: {erros}")
    print(f"Todas as imagens salvas em: {pasta_destino}")

def redimensionar_preenchendo(img, largura_alvo, altura_alvo, cor_fundo='white'):
    """
    Redimensiona mantendo proporção e preenche o restante com cor de fundo
=======
                    print(f"✓ {arquivo.name} → {caminho_destino.name}")
                    
            except Exception as e:
                print(f"✗ Erro em {arquivo.name}: {e}")

def redimensionar_com_proporcao(img, largura_alvo, altura_alvo, preencher=False, cor_fundo='white'):
    """
    Redimensiona imagem mantendo proporção
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3
    """
    # Calcular ratio de redimensionamento
    ratio = min(largura_alvo/img.width, altura_alvo/img.height)
    nova_largura = int(img.width * ratio)
    nova_altura = int(img.height * ratio)
    
<<<<<<< HEAD
    # Redimensionar mantendo proporção
    img_redimensionada = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
    
    # Criar nova imagem com fundo
    nova_imagem = Image.new('RGB', (largura_alvo, altura_alvo), cor_fundo)
    
    # Centralizar a imagem redimensionada
    x = (largura_alvo - nova_largura) // 2
    y = (altura_alvo - nova_altura) // 2
    nova_imagem.paste(img_redimensionada, (x, y))
    
    return nova_imagem

def redimensionar_cortando(img, largura_alvo, altura_alvo):
    """
    Redimensiona mantendo proporção e corta o excesso
    """
    # Calcular ratio de redimensionamento (cobre toda a área)
    ratio = max(largura_alvo/img.width, altura_alvo/img.height)
    nova_largura = int(img.width * ratio)
    nova_altura = int(img.height * ratio)
    
    # Redimensionar
    img_redimensionada = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
    
    # Calcular coordenadas para cortar o centro
    esquerda = (nova_largura - largura_alvo) // 2
    topo = (nova_altura - altura_alvo) // 2
    direita = esquerda + largura_alvo
    inferior = topo + altura_alvo
    
    # Cortar imagem
    img_cortada = img_redimensionada.crop((esquerda, topo, direita, inferior))
    
    return img_cortada

def redimensionar_distorcendo(img, largura_alvo, altura_alvo):
    """
    Redimensiona forçando 512x512 (pode distorcer a imagem)
    """
    return img.resize((largura_alvo, altura_alvo), Image.Resampling.LANCZOS)

def mostrar_exemplos_metodos():
    """
    Mostra exemplos visuais dos métodos de redimensionamento
    """
    print("\n=== MÉTODOS DE REDIMENSIONAMENTO ===")
    print("1. PREENCHER - Mantém proporção, adiciona fundo")
    print("   • Ideal para preservar imagem completa")
    print("   • Ex: 800x600 → 512x512 (com barras pretas)")
    
    print("\n2. CORTAR - Mantém proporção, corta excesso")
    print("   • Ideal quando o centro é importante")
    print("   • Ex: 800x600 → 512x512 (corta laterais)")
    
    print("\n3. DISTORCER - Força 512x512")
    print("   • Mais rápido, mas distorce imagem")
    print("   • Ex: 800x600 → 512x512 (estica/achata)")

# Interface de uso
def main():
    print("=== REDIMENSIONADOR PARA 512x512 PIXELS ===")
    print("Garante que TODAS as imagens terão exatamente 512x512 pixels\n")
    
    pasta_origem = input("Pasta com as imagens: ").strip()
    
    if not os.path.exists(pasta_origem):
        print("❌ Pasta de origem não existe!")
        return
    
    pasta_destino = input("Pasta de destino [padrão: pasta_origem_512]: ").strip()
    if not pasta_destino:
        pasta_destino = pasta_origem + "_512"
    
    # Mostrar métodos disponíveis
    mostrar_exemplos_metodos()
    
    print("\nEscolha o método:")
    print("1 - Preencher com fundo (RECOMENDADO)")
    print("2 - Cortar o excesso")
    print("3 - Distorcer (forçar 512x512)")
    
    opcao = input("Sua escolha [1]: ").strip()
    
    if opcao == "2":
        metodo = 'cortar'
        cor_fundo = 'white'
    elif opcao == "3":
        metodo = 'distorcer'
        cor_fundo = 'white'
    else:
        metodo = 'preencher'
        print("\nCor do fundo para áreas vazias:")
        print("1 - Branco (padrão)")
        print("2 - Preto")
        print("3 - Cinza")
        cor_opcao = input("Escolha [1]: ").strip()
        
        if cor_opcao == "2":
            cor_fundo = 'black'
        elif cor_opcao == "3":
            cor_fundo = 'gray'
        else:
            cor_fundo = 'white'
    
    print(f"\n⚙️  Configuração:")
    print(f"• Método: {metodo.upper()}")
    print(f"• Tamanho: 512x512 pixels")
    print(f"• Fundo: {cor_fundo}")
    print(f"• Origem: {pasta_origem}")
    print(f"• Destino: {pasta_destino}")
    
    confirmar = input("\nConfirmar e processar? (s/N): ").strip().lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        print("\n🔄 Processando imagens...")
        redimensionar_imagens_512x512(pasta_origem, pasta_destino, metodo, cor_fundo)
    else:
        print("Operação cancelada.")
=======
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
>>>>>>> eeaf442a1f5b0a47dcf49b7a06f4ed0bdba929c3

if __name__ == "__main__":
    main()