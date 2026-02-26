import re

def limpar_legenda(arquivo_entrada, arquivo_saida):
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # 1. Remove os números das legendas (sozinhos em uma linha)
        # 2. Remove os timestamps (00:00:00,000 --> 00:00:00,000)
        # O regex abaixo identifica esses padrões
        padrao_tempo = r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
        
        # Substitui os padrões por uma string vazia
        texto_limpo = re.sub(padrao_tempo, '', conteudo)

        # Remove linhas em branco extras que sobraram
        linhas = [linha.strip() for linha in texto_limpo.split('\n') if linha.strip()]
        
        # Junta tudo em um texto corrido
        resultado = '\n'.join(linhas)

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(resultado)
            
        print(f"Sucesso! O texto limpo foi salvo em: {arquivo_saida}")

    except FileNotFoundError:
        print("Erro: O arquivo de entrada não foi encontrado.")

# Uso do programa:
limpar_legenda('legenda_corrigida.srt', 'texto_final.txt')