import re
from datetime import datetime, timedelta

def srt_to_timedelta(time_str):
    """Converte o formato HH:MM:SS,mmm para um objeto timedelta."""
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    return timedelta(hours=int(hours), minutes=int(minutes), 
                     seconds=int(seconds), milliseconds=int(milliseconds))

def timedelta_to_srt(td):
    """Converte um objeto timedelta de volta para o formato HH:MM:SS,mmm."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def corrigir_sobreposicoes(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    novas_linhas = []
    i = 0
    # Regex para capturar o padrão de tempo do SRT
    padrao_tempo = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    # Armazenar blocos de tempo para comparação
    indices_tempo = []
    for idx, linha in enumerate(linhas):
        if padrao_tempo.match(linha):
            indices_tempo.append(idx)

    for n in range(len(indices_tempo)):
        idx_atual = indices_tempo[n]
        match_atual = padrao_tempo.match(linhas[idx_atual])
        inicio_atual = srt_to_timedelta(match_atual.group(1))
        fim_atual = srt_to_timedelta(match_atual.group(2))

        # Se não for a última legenda, verifica a próxima
        if n < len(indices_tempo) - 1:
            idx_proximo = indices_tempo[n+1]
            match_proximo = padrao_tempo.match(linhas[idx_proximo])
            inicio_proximo = srt_to_timedelta(match_proximo.group(1))

            # Lógica de correção: Se o fim atual invade o início da próxima
            if fim_atual > inicio_proximo:
                fim_atual = inicio_proximo

        # Reconstrói a linha de tempo corrigida
        linhas[idx_atual] = f"{timedelta_to_srt(inicio_atual)} --> {timedelta_to_srt(fim_atual)}\n"

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.writelines(linhas)

    print(f"Sucesso! Arquivo corrigido salvo como: {arquivo_saida}")

# Uso:
corrigir_sobreposicoes('legenda_original.srt', 'legenda_corrigida.srt')