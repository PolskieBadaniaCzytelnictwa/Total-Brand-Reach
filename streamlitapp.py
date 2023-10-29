import streamlit as st
import pandas as pd

pd.set_option('display.float_format', '{:.0f}'.format)

df = pd.read_excel('C:/Users/lapto/OneDrive/Pulpit/TBR_1-9.2023/TBR_9m.xlsx')
tematyka = pd.read_excel('C:/Users/lapto/OneDrive/Pulpit/TBR_1-9.2023/kat.xlsx')

tematyka_lista = tematyka['kat'].unique()
wskaźniki_lista = ['druk+e-wydania', 'www', 'TBR']
miesiące_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

st.title("Total Reach 2023")

selected_miesiace = st.sidebar.slider("Wybierz okres czasu (miesiące):", min_value=min(miesiące_lista), max_value=max(miesiące_lista), value=(min(miesiące_lista), max(miesiące_lista)))
selected_tematyki = st.sidebar.multiselect("Wybierz rodzaje pism:", tematyka_lista, default=tematyka_lista)
if not selected_tematyki:
        selected_tematyki = tematyka_lista

wyniki = pd.DataFrame()
for i in selected_tematyki:
    pisma_lista = tematyka[tematyka['kat'] == i]['tytuł'].to_list()
    for j in pisma_lista:
        for k in wskaźniki_lista:
            if k != 'TBR':
                wyniki.loc[j, k] = df[(df['tytuł'] == j) & (df['wskaźnik'] == k) & (df['miesiąc'].between(selected_miesiace[0], selected_miesiace[1]))]['wynik'].mean()
            else:
                wyniki.loc[j, k] = (1 - float(df.loc[(df['tytuł'] == j) & (df['wskaźnik'] == 'współczytelnictwo'), 'wynik'].iloc[0])) * wyniki.loc[j, 'druk+e-wydania'] + wyniki.loc[j, 'www']


wyniki = wyniki[wyniki['www'] == wyniki['www']]
wyniki = wyniki.fillna(0)
wyniki = wyniki.sort_values('TBR', ascending=False)
wyniki_sformatowane = wyniki.applymap(lambda x: '{:,.0f}'.format(x).replace(',', ' '))

st.table(wyniki_sformatowane)
