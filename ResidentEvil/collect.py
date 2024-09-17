# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def get_content(url):
    resp = requests.get(url)
    return resp

# Buscando os dados na webpage
def get_basic_infos(soup):
    # Buscando no site a DIV da classe para filtrar os dados solicitados
    div_page = soup.find("div", class_="td-page-content")
    # Buscando na DIV o parágrafo referente aos dados
    paragrafo = div_page.find_all("p")[1]
    # Separando os dados
    ems = paragrafo.find_all("em")
    data = {} # criando um dicionário para visualização e fatiar o texto no ':'
    for i in ems:
        print(i)
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    return data

# Buscando o h4 para os dados de "Aparições em títulos da série"
def get_aparicoes(soup):
    lis = (soup.find("div", class_="td-page-content")
        .find("h4")
        .find_next()
        .find_all("li"))
    
    aparicoes = [i.text for i in lis]
    return aparicoes

# Buscando as infos dos personagens
def get_personagens_info(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível acessar ou obter os dados!")
        return{}
    else:    
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url)
    soup_personagens = BeautifulSoup(resp.text)

    ancoras = (soup_personagens.find("div", class_="td-page-content")
                            .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links

# %%

links = get_links()
data = []
for i in tqdm(links):
    print(i)
    d = get_personagens_info(i)
    d["link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)
#%%

df = pd.DataFrame(data)
df[~df["de nascimento"].isna()]

#%%
# Exportando/Salvando a lista em arquivo em .csv
df.to_csv("dados_resident_evil.csv", index=False, sep=";")

# Exportando/Salvando a lista em arquivo em .parquet
df.to_parquet("dados_resident_evil.parquet", index=False)

# Exportando/Salvando a lista em arquivo em .pickle
df.to_pickle("dados_resident_evil.pkl")