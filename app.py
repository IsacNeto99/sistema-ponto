from datetime import datetime
import gspread
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Sistema de Ponto", page_icon="📸", layout="centered"
)

st.title("🕒 Registro de Ponto - Empresa")
st.markdown("Digite seu código de **4 dígitos** e tire a foto para registrar.")

# Entrada do Código
codigo = st.text_input(
    "Código do Funcionário", max_chars=4, type="default", placeholder="Ex: 1234"
)

# Câmera nativa do Streamlit
foto_capturada = st.camera_input("Tire a foto para comprovar presença")


def salvar_no_google_sheets(codigo_func, data_hora_str):
  try:
    # Pega as credenciais direto do cofre seguro do Streamlit Cloud
    creds_dict = dict(st.secrets["gcp_service_account"])

    client = gspread.service_account_from_dict(creds_dict)
    # Substitua "Nome_Da_Sua_Planilha" pelo nome exato da sua planilha no Google Sheets
    sheet = client.open("Nome_Da_Sua_Planilha").sheet1

    sheet.append_row([data_hora_str, codigo_func])
    return True
  except Exception as e:
    st.error(f"Erro ao salvar na planilha: {e}")
    return False


if foto_capturada and codigo:
  if len(codigo) == 4:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with st.spinner("Salvando registro..."):
      sucesso = salvar_no_google_sheets(codigo, agora)

      if sucesso:
        st.success(f"✅ Ponto registrado com sucesso às {agora}!")
  else:
    st.warning("⚠️ O código deve ter exatamente 4 dígitos.")
elif foto_capturada and not codigo:
  st.warning("⚠️ Por favor, digite o código de 4 dígitos antes de tirar a foto.")