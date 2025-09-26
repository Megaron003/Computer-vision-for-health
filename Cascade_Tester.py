import cv2
import os

def carregar_classificador():
    """Carrega o classificador Haar Cascade treinado"""
    print("🔍 Carregando classificador treinado...")
    
    classifier_path = "C:\Users\Guilherme\Desktop\Computer_Vision_For_Health\Haarcascade_Bengin\classifier\cascade.xml"
    
    if not os.path.exists(classifier_path):
        print("❌ Classificador não encontrado!")
        print("💡 Certifique-se de que o arquivo classifier/cascade.xml existe")
        return None
    
    classifier = cv2.CascadeClassifier(classifier_path)
    
    if classifier.empty():
        print("❌ Erro ao carregar classificador!")
        return None
    
    print("✅ Classificador carregado com sucesso!")
    return classifier

def testar_imagem(caminho_imagem, classifier, salvar_resultado=True):
    """Testa o classificador em uma imagem específica"""
    print(f"🎯 Testando imagem: {caminho_imagem}")
    
    # Carregar imagem
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print(f"❌ Imagem não encontrada: {caminho_imagem}")
        return
    
    # Criar cópia para desenhar os resultados
    imagem_resultado = imagem.copy()
    
    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    print("🔍 Detectando tumores...")
    
    # Detectar tumores com diferentes parâmetros para melhor precisão
    parametros = [
        {'scaleFactor': 1.1, 'minNeighbors': 3, 'minSize': (20, 20)},
        {'scaleFactor': 1.05, 'minNeighbors': 5, 'minSize': (24, 24)},
        {'scaleFactor': 1.2, 'minNeighbors': 7, 'minSize': (30, 30)}
    ]
    
    total_tumores = 0
    
    for i, params in enumerate(parametros):
        tumores = classifier.detectMultiScale(cinza, **params)
        print(f"   Config {i+1}: {len(tumores)} tumores detectados")
        
        # Desenhar retângulos (cada configuração com cor diferente)
        cores = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]  # Verde, Azul, Vermelho
        
        for (x, y, w, h) in tumores:
            cv2.rectangle(imagem_resultado, (x, y), (x + w, y + h), cores[i], 2)
            cv2.putText(imagem_resultado, f'Config {i+1}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, cores[i], 1)
            print(f"      Tumor {total_tumores + 1}: posição({x}, {y}), tamanho({w}x{h})")
            total_tumores += 1
    
    print(f"📊 Total de detecções: {total_tumores}")
    
    # Salvar resultado
    if salvar_resultado and total_tumores > 0:
        caminho_resultado = "resultado_detecao.jpg"
        cv2.imwrite(caminho_resultado, imagem_resultado)
        print(f"💾 Resultado salvo em: {caminho_resultado}")
    
    # Mostrar imagem original e resultado
    if total_tumores > 0:
        # Redimensionar imagens para caber na tela (opcional)
        altura, largura = imagem_resultado.shape[:2]
        if largura > 1200:
            escala = 1200 / largura
            nova_largura = 1200
            nova_altura = int(altura * escala)
            imagem_redim = cv2.resize(imagem_resultado, (nova_largura, nova_altura))
            imagem_orig_redim = cv2.resize(imagem, (nova_largura, nova_altura))
        else:
            imagem_redim = imagem_resultado
            imagem_orig_redim = imagem
        
        # Mostrar lado a lado
        imagem_comparacao = cv2.hconcat([imagem_orig_redim, imagem_redim])
        
        cv2.imshow('Comparação: Original (esq) vs Detecção (dir)', imagem_comparacao)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("🔴 Nenhum tumor detectado na imagem")
        
        # Mostrar apenas a imagem original
        cv2.imshow('Imagem Original - Nenhum Tumor Detectado', imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return total_tumores

def testar_multiplas_imagens(pasta_imagens, classifier):
    """Testa o classificador em todas as imagens de uma pasta"""
    if not os.path.exists(pasta_imagens):
        print(f"❌ Pasta não encontrada: {pasta_imagens}")
        return
    
    extensoes = ('.jpg', '.jpeg', '.png', '.bmp')
    imagens = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(extensoes)]
    
    print(f"📁 Encontradas {len(imagens)} imagens na pasta")
    
    for i, arquivo in enumerate(imagens):
        print(f"\n--- Testando imagem {i+1}/{len(imagens)}: {arquivo} ---")
        caminho_completo = os.path.join(pasta_imagens, arquivo)
        testar_imagem(caminho_completo, classifier, salvar_resultado=False)

def menu_interativo():
    """Menu interativo para testar o classificador"""
    classifier = carregar_classificador()
    if classifier is None:
        return
    
    while True:
        print("\n" + "="*50)
        print("🎯 DETECTOR DE TUMORES PULMONARES")
        print("="*50)
        print("1. Testar imagem específica")
        print("2. Testar todas as imagens de uma pasta") 
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            caminho_imagem = input("Digite o caminho da imagem: ").strip()
            
            # Se vazio, usar o caminho padrão
            if not caminho_imagem:
                caminho_imagem = r"C:\Users\Guilherme\Downloads\The IQ-OTHNCCD lung cancer dataset\The IQ-OTHNCCD lung cancer dataset\Bengin cases\Bengin case (3).jpg"
            
            testar_imagem(caminho_imagem, classifier)
            
        elif opcao == "2":
            pasta_imagens = input("Digite o caminho da pasta: ").strip()
            if pasta_imagens:
                testar_multiplas_imagens(pasta_imagens, classifier)
            else:
                print("❌ Caminho da pasta não pode ser vazio")
                
        elif opcao == "3":
            print("👋 Encerrando programa...")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    # Caminho da imagem de teste (já configurado)
    caminho_imagem_teste = r"C:\Users\Guilherme\Downloads\The IQ-OTHNCCD lung cancer dataset\The IQ-OTHNCCD lung cancer dataset\Bengin cases\Bengin case (3).jpg"
    
    # Carregar classificador
    classifier = carregar_classificador()
    
    if classifier is not None:
        print("\n🚀 TESTE AUTOMÁTICO INICIADO")
        print(f"📷 Imagem de teste: {caminho_imagem_teste}")
        
        # Testar a imagem específica
        tumores_detectados = testar_imagem(caminho_imagem_teste, classifier)
        
        print(f"\n{'='*50}")
        if tumores_detectados > 0:
            print(f"🎉 TESTE CONCLUÍDO: {tumores_detectados} tumor(es) detectado(s)!")
        else:
            print("🔍 TESTE CONCLUÍDO: Nenhum tumor detectado")
        print("="*50)
        
        # Oferecer menu interativo após o teste automático
        continuar = input("\nDeseja testar mais imagens? (s/n): ").strip().lower()
        if continuar in ['s', 'sim', 'y', 'yes']:
            menu_interativo()
    else:
        print("❌ Não foi possível carregar o classificador")