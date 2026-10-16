import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📈 Growth Markkinoinnin ROI & LTV -Analysaattori")
st.write("Työkalu yhdistää markkinointidatan ja taloushallinnon tunnusluvut.")

api_key = st.text_input("Syötä Gemini API-avain:", type="password")

@st.cache_data
def load_data():
    df = pd.read_csv("markkinointidata.csv")
    df["LTV_CAC_Suhde"] = (df["Keskiarvo_LTV_EUR"] / df["CAC_EUR"]).round(2)
    return df

try:
    df = load_data()
    st.subheader("Markkinointikanavien raakadata")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error("Virhe: markkinointidata.csv -tiedostoa ei löytynyt samasta kansiosta.")
    st.stop()

st.subheader("Tekoälyn strateginen suositus")

# Kaikki tämän alla oleva on sisennetty tiukasti napin taakse
if st.button("Analysoi kannattavuus ja allokoi budjetti"):
    if not api_key:
        st.warning("Syötä ensin API-avain yllä olevaan kenttään!")
    else:
        with st.spinner("Analysoidaan tunnuslukuja..."):
            genai.configure(api_key=api_key)
            # Päivitetty malli, jota olet käyttänyt
            model = genai.GenerativeModel('gemini-3.8-flash')
            
            data_string = df.to_string(index=False)
            prompt = f"Olet Growth Strategist. Maksimoi kannattavuus analysoimalla asiakashankinnan kustannuksia (CAC) ja asiakkaan elinkaariarvoa (LTV).\n\nAnalysoi seuraava data ja kerro mistä leikkaamme ja mihin panostamme:\n{data_string}"
            
            try:
                response = model.generate_content(prompt)
                st.success("Analyysi valmis!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Virhe analyysissä: {e}")