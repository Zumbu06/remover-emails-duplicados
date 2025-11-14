# ⚙️ Gerenciador de E-mails para Campanhas

Este é um aplicativo web simples, feito em Streamlit, para ajudar na higienização e gerenciamento de listas de e-mail para campanhas de marketing.

Ele filtra novos lotes de e-mails contra uma lista mestre, garantindo que você envie campanhas apenas para e-mails únicos e novos, evitando duplicatas.

## ✨ Funcionalidades (Features)

* **Interface Web com Streamlit:** Fácil de usar, rodando direto no navegador.
* **Processamento de Lotes:** Cole centenas de e-mails de uma vez para processamento.
* **Higienização Automática:** Remove duplicatas do lote colado e filtra e-mails que já existem na lista mestre.
* **Lista Mestre Persistente:** O arquivo `emails_unicos_MESTRE.txt` guarda o histórico de TODOS os e-mails únicos já processados.
* **Histórico de Lotes:** Salva os últimos 5 lotes filtrados na pasta `historico_lotes/` para consulta.
* **Visualizador Embutido:** A barra lateral permite visualizar a lista mestre e os lotes antigos sem sair do app.

Já deixei publico no Streamlit Cloud: https://limpar-emails.streamlit.app/
Mas se for ter um uso continuo recomendo que utilize local host pois atualmente nao esta ligado a nenhum banco de dados entao os emails registrados não irão ficar salvos por muito tempo.
