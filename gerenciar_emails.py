import os  
import datetime  #criar nomes de arquivo com data e hora

NOME_ARQUIVO_MESTRE = "emails_unicos_MESTRE.txt"
PASTA_HISTORICO_LOTES = "historico_lotes"  
LIMITE_HISTORICO = 5

def carregar_emails_salvos():
    """Carrega os e-mails do arquivo MESTRE para um set."""
    emails_unicos_mestre = set()
    try:
        with open(NOME_ARQUIVO_MESTRE, "r") as f:
            for linha in f:
                email = linha.strip()
                if email:
                    emails_unicos_mestre.add(email)
        print(f"INFO: Carregados {len(emails_unicos_mestre)} e-mails únicos do arquivo MESTRE.")
    except FileNotFoundError:
        print(f"INFO: Arquivo '{NOME_ARQUIVO_MESTRE}' não encontrado. Um novo será criado.")
    
    return emails_unicos_mestre

def salvar_lista_em_arquivo(set_de_emails, nome_arquivo_completo):
    """Função genérica para salvar um set em um arquivo de texto."""
    with open(nome_arquivo_completo, "w") as f:
        # Salva em ordem alfabética
        for email in sorted(list(set_de_emails)):
            f.write(email + "\n")
    print(f"INFO: {len(set_de_emails)} e-mails salvos em '{nome_arquivo_completo}'.")

def gerenciar_historico_lotes():
    """Verifica a pasta de histórico, garante que ela exista e remove o mais antigo se o limite foi atingido."""
    
    # 1. Garante que a pasta de histórico exista
    if not os.path.exists(PASTA_HISTORICO_LOTES):
        os.makedirs(PASTA_HISTORICO_LOTES)
        print(f"INFO: Pasta de histórico '{PASTA_HISTORICO_LOTES}' criada.")
        return # Não há nada para excluir ainda

    # 2. Pega a lista de arquivos de lote salvos
    #    os.listdir() lista todos os arquivos na pasta
    arquivos_historico = sorted(os.listdir(PASTA_HISTORICO_LOTES))
    
    # 3. Verifica se o limite foi atingido
    if len(arquivos_historico) >= LIMITE_HISTORICO:
        # Se sim, o arquivo mais antigo é o primeiro da lista (pois estão em ordem)
        arquivo_para_deletar = arquivos_historico[0]
        caminho_completo_delecao = os.path.join(PASTA_HISTORICO_LOTES, arquivo_para_deletar)
        
        try:
            os.remove(caminho_completo_delecao)
            print(f"INFO: Histórico cheio. Removendo o lote mais antigo: {arquivo_para_deletar}")
        except OSError as e:
            print(f"ERRO: Não foi possível deletar o arquivo antigo: {e}")

def main():
    # 1. Carrega a lista MESTRE de e-mails
    emails_mestre = carregar_emails_salvos()
    
    # 2. Recebe o novo lote de e-mails do usuário
    print("\n--- Adicionar Novo Lote de E-mails ---")
    print("Digite ou cole os e-mails (um por linha).")
    print("Quando terminar, digite 'fim' em uma linha nova e pressione Enter:")
    
    lote_atual_lista = []
    while True:
        try:
            entrada = input()
            if entrada.lower() == 'fim':
                break
            if entrada.strip():
                lote_atual_lista.append(entrada.strip())
        except EOFError:
            break
            
    if not lote_atual_lista:
        print("\nNenhum e-mail novo foi digitado.")
        return

    # 3. Processa os e-mails
    lote_atual_set_unico = set(lote_atual_lista)
    novos_emails_para_enviar = lote_atual_set_unico.difference(emails_mestre)

    # 4. Feedback do Processamento
    print("\n--- Processamento do Lote ---")
    print(f"Total de e-mails recebidos neste lote: {len(lote_atual_lista)}")
    print(f"E-mails únicos *neste lote*: {len(lote_atual_set_unico)}")
    print(f"E-mails que *já estavam* no mestre (ignorados): {len(lote_atual_set_unico) - len(novos_emails_para_enviar)}")
    print(f"E-mails *NOVOS* para enviar: {len(novos_emails_para_enviar)}")

    # 5. Salva os arquivos
    
    if not novos_emails_para_enviar:
        print("\nINFO: Nenhum e-mail novo para salvar. O histórico não será atualizado.")
    else:
        # limpa o histórico se necessário
        gerenciar_historico_lotes()
        
        # Cria um nome de arquivo único
        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_novo_arquivo = f"lote_{agora}.txt"
        caminho_completo_novo_arquivo = os.path.join(PASTA_HISTORICO_LOTES, nome_novo_arquivo)
        
        # Salva o novo lote filtrado nesse arquivo
        salvar_lista_em_arquivo(novos_emails_para_enviar, caminho_completo_novo_arquivo)
        
        # Atualiza o mestre
        emails_mestre.update(novos_emails_para_enviar)
        salvar_lista_em_arquivo(emails_mestre, NOME_ARQUIVO_MESTRE)
    
    print(f"\nTotal de e-mails na lista MESTRE agora: {len(emails_mestre)}")

    # 6. Retorna a lista do NOVO LOTE filtrado no console
    print(f"\n--- Lista do Lote Filtrado (salvo em '{caminho_completo_novo_arquivo}') ---")
    if novos_emails_para_enviar:
        for email in sorted(list(novos_emails_para_enviar)):
            print(email)
    else:
        print("(Nenhum e-mail novo neste lote)")

if __name__ == "__main__":
    main()