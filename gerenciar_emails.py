import streamlit as st
import os
import datetime

# --- Configuração dos Nomes (não mudou) ---
NOME_ARQUIVO_MESTRE = "emails_unicos_MESTRE.txt"
PASTA_HISTORICO_LOTES = "historico_lotes"
LIMITE_HISTORICO = 5
# -----------------------------

# --- Funções do "Motor" (exatamente as mesmas do v3, não mudei nada) ---

def carregar_emails_salvos():
    """Carrega os e-mails do arquivo MESTRE para um set."""
    # Garante que o arquivo mestre exista, mesmo que vazio
    if not os.path.exists(NOME_ARQUIVO_MESTRE):
        open(NOME_ARQUIVO_MESTRE, 'w').close()
        
    emails_unicos_mestre = set()
    try:
        with open(NOME_ARQUIVO_MESTRE, "r") as f:
            for linha in f:
                email = linha.strip()
                if email:
                    emails_unicos_mestre.add(email)
    except FileNotFoundError:
        pass # Já cuidamos disso
    
    return emails_unicos_mestre

def salvar_lista_em_arquivo(set_de_emails, nome_arquivo_completo):
    """Função genérica para salvar um set em um arquivo de texto."""
    with open(nome_arquivo_completo, "w") as f:
        for email in sorted(list(set_de_emails)):
            f.write(email + "\n")

def gerenciar_historico_lotes():
    """Verifica a pasta de histórico e remove o mais antigo se o limite foi atingido."""
    if not os.path.exists(PASTA_HISTORICO_LOTES):
        os.makedirs(PASTA_HISTORICO_LOTES)
        return
    
    arquivos_historico = sorted([os.path.join(PASTA_HISTORICO_LOTES, f) for f in os.listdir(PASTA_HISTORICO_LOTES)], key=os.path.getmtime)
    
    if len(arquivos_historico) >= LIMITE_HISTORICO:
        arquivo_para_deletar = arquivos_historico[0]
        try:
            os.remove(arquivo_para_deletar)
            st.toast(f"Histórico cheio. Removendo lote: {os.path.basename(arquivo_para_deletar)}")
        except OSError:
            pass # Ignora se não conseguir deletar

# --- A MÁGICA DO STREAMLIT COMEÇA AQUI ---
# Esta parte substitui a sua antiga função "main()"

# --- 1. Configuração da Barra Lateral (Sidebar) ---
st.sidebar.title("Navegação")
st.sidebar.markdown("---")

st.sidebar.header("Ver E-mails Mestre")
if st.sidebar.button("Carregar Lista Mestre"):
    emails_mestre = carregar_emails_salvos()
    st.sidebar.success(f"Total de {len(emails_mestre)} e-mails únicos.")
    # st.dataframe exibe uma tabela. st.text_area exibe um texto copiável.
    st.sidebar.dataframe(sorted(list(emails_mestre)), height=300)

st.sidebar.markdown("---")
st.sidebar.header("Ver Lotes Antigos")

# Garante que a pasta exista para não dar erro
if not os.path.exists(PASTA_HISTORICO_LOTES):
    os.makedirs(PASTA_HISTORICO_LOTES)

# Lista os arquivos no histórico, do mais novo para o mais velho
arquivos_no_historico = sorted(os.listdir(PASTA_HISTORICO_LOTES), reverse=True)

if not arquivos_no_historico:
    st.sidebar.info("Nenhum lote no histórico ainda.")
else:
    # Cria um menu dropdown para selecionar um lote
    lote_selecionado = st.sidebar.selectbox("Selecione um lote do histórico:", arquivos_no_historico)
    
    if lote_selecionado:
        # Lê o conteúdo do arquivo selecionado e exibe
        with open(os.path.join(PASTA_HISTORICO_LOTES, lote_selecionado), "r") as f:
            emails_do_lote = f.read()
        st.sidebar.dataframe(emails_do_lote.split('\n'), height=300)


# --- 2. Configuração da Página Principal ---
st.title("⚙️ Gerenciador de E-mails para Campanhas")
st.write("Cole um lote de e-mails abaixo para filtrá-los contra a lista mestre.")

# Em vez de input(), usamos st.text_area()
lote_colado = st.text_area("Cole os e-mails (um por linha):", height=250, placeholder="email1@exemplo.com\nemail2@exemplo.com")

st.markdown("---")

# Em vez de rodar direto, esperamos o clique no botão
if st.button("Processar e Filtrar Lote"):
    
    if not lote_colado:
        st.warning("Por favor, cole os e-mails na caixa de texto.")
    else:
        # 1. Transformar o texto colado em uma lista
        # .strip() remove espaços extras, .split('\n') quebra por linha
        lote_atual_lista = [email.strip() for email in lote_colado.strip().split('\n') if email.strip()]
        
        # 2. Carregar o mestre
        emails_mestre = carregar_emails_salvos()
        
        # 3. Processar (igual ao v3)
        lote_atual_set_unico = set(lote_atual_lista)
        novos_emails_para_enviar = lote_atual_set_unico.difference(emails_mestre)
        
        # 4. Mostrar Resultados (em vez de print())
        st.header("Resultados do Processamento")
        st.metric(label="Total de e-mails colados", value=len(lote_atual_lista))
        st.metric(label="E-mails únicos *neste lote*", value=len(lote_atual_set_unico))
        st.metric(label="E-mails que já estavam no mestre (ignorados)", value=len(lote_atual_set_unico) - len(novos_emails_para_enviar))
        st.metric(label="✅ E-mails NOVOS para Enviar", value=len(novos_emails_para_enviar))
        
        # 5. Salvar os arquivos (se houver novos)
        if not novos_emails_para_enviar:
            st.info("Nenhum e-mail novo encontrado. Nada foi salvo.")
        else:
            # A. Gerencia o histórico (apaga o mais antigo se > 5)
            gerenciar_historico_lotes()
            
            # B. Cria nome e caminho do novo arquivo de lote
            agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_novo_arquivo = f"lote_{agora}.txt"
            caminho_completo_novo_arquivo = os.path.join(PASTA_HISTORICO_LOTES, nome_novo_arquivo)
            
            # C. Salva o novo lote filtrado
            salvar_lista_em_arquivo(novos_emails_para_enviar, caminho_completo_novo_arquivo)
            
            # D. Atualiza e salva o mestre
            emails_mestre.update(novos_emails_para_enviar)
            salvar_lista_em_arquivo(emails_mestre, NOME_ARQUIVO_MESTRE)
            
            st.success(f"Lista de novos e-mails salva em: '{caminho_completo_novo_arquivo}'")
            st.balloons() # Comemoração!
            
            # 6. Mostrar a lista nova para copiar
            st.subheader("Lista de E-mails Novos (Pronta para copiar):")
            # Converte o set para uma lista, depois para texto (um por linha)
            texto_para_copiar = "\n".join(sorted(list(novos_emails_para_enviar)))
            st.text_area("E-mails Novos:", value=texto_para_copiar, height=200)