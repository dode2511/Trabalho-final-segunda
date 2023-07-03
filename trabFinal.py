from bs4 import BeautifulSoup
import requests
from tabulate import tabulate


def titulos(msg, traco="-"):
    print()
    print(msg)
    print(traco*50)





produto = input("Produto: ")
url_dafiti = "https://www.dafiti.com.br/catalog/?q=" + produto + "&wtqs=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


pagina_daifiti = requests.get(url_dafiti, headers=headers)
html_daifit = BeautifulSoup(pagina_daifiti.content, "html.parser")

div_produtos_daifiti = html_daifit.find("div", class_="l-full-content l-container")
produtos_daifiti = div_produtos_daifiti.find_all("p", class_="product-box-title")
preco_descontos_daifiti = div_produtos_daifiti.find_all("span", class_="product-box-price-to")
preco_original_daifiti = div_produtos_daifiti.find_all("span", class_="product-box-price-from")

produtos_com_desconto = []

for i in range(len(produtos_daifiti)):
    titulo = produtos_daifiti[i].get_text().strip()
    preco = preco_original_daifiti[i].get_text().strip()
    desconto = produtos_com_desconto[i].get_text().strip() if i < len(produtos_com_desconto) else "Sem desconto"
    produtos_com_desconto.append({"titulo": titulo, "desconto": desconto, "preco": preco})



def lista_daifiti():
    titulos("Produtos da daifiti")
    table_data = []
    headers = ["Nome do produto", "Valor sem Desconto", "Valor com Desconto"]

    for produto in produtos_com_desconto:
        tituloo = produto['titulo']
        desconto = produto['desconto']
        preco = produto['preco']
        table_data.append([tituloo, desconto, preco])

    print(tabulate(table_data, headers, tablefmt="grid"))


##########################################################################################################################################################################################################################################################



url_kanui = "https://www.kanui.com.br/catalog/?q=" + produto + "&wtqs=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


pagina_kanui = requests.get(url_kanui, headers=headers)
html_kanui = BeautifulSoup(pagina_kanui.content, "html.parser")

div_produtos_kanui = html_kanui.find("div", class_="l-full-content l-container")
produtos_kanui = div_produtos_kanui.find_all("p", class_="product-box-title")
preco_descontos_kanui = div_produtos_kanui.find_all("span", class_="product-box-price-to")
preco_original_kanui = div_produtos_kanui.find_all("span", class_="product-box-price-from")

produtos2 = []





for i in range(len(produtos_kanui)):
    titulo = produtos_kanui[i].get_text().strip()
    preco = preco_original_kanui[i].get_text().strip()
    desconto = preco_descontos_kanui[i].get_text().strip() if i < len(preco_descontos_kanui) else "Sem desconto"
    produtos2.append({"titulo": titulo, "desconto": desconto, "preco": preco})


def lista_kanui():
    titulos("Produtos da Kanui")
    table_data = []
    headers = ["Nome do produto", "Valor sem Desconto", "Valor com Desconto"]

    for produto in produtos2:
        tituloo = produto['titulo']
        desconto = produto['desconto']
        preco = produto['preco']
        table_data.append([tituloo, desconto, preco])

    print(tabulate(table_data, headers, tablefmt="grid"))


produtos_total = produtos_com_desconto + produtos2

def lista_todos():

    produtos_total = produtos_com_desconto + produtos2

    titulos("Todos os produtos")
    table_data = []
    headers = ["Nome do produto", "Valor sem Desconto", "Valor com Desconto"]

    for produto in produtos_total:
        titulo = produto['titulo']
        desconto = produto['desconto']
        preco = produto['preco']
        table_data.append([titulo, desconto, preco])

    print(tabulate(table_data, headers, tablefmt="grid"))
   

def apenas_daifiti():
    set_daifiti = set()     
    set_kanui = set()

    for produtos in produtos2:
        set_kanui.add(produtos['titulo'])

    for produtos in produtos_com_desconto:
        set_daifiti.add(produtos['titulo'])

    only_daifiti = set_daifiti.difference(set_kanui)

    titulos("Produtos Disponiveis Apenas na Daifiti")

    if len(only_daifiti) == 0:
        print("Obs.: * Não há produtos ")
    else:
        for produtos in only_daifiti:
            print(produtos)

def apenas_kanui():

    set_daifiti = set()     
    set_kanui = set()

    for produtos in produtos_com_desconto:
        set_kanui.add(produtos['titulo'])

    for produtos in produtos2:
        set_daifiti.add(produtos['titulo'])

    only_kanui = set_kanui.symmetric_difference(set_daifiti)
    titulos("Produtos Disponiveis Apenas na Kanui")

    if len(only_kanui) == 0:
        print("Obs.: * Não há produtos ")
    else:
        for produtos in only_kanui:
            print(produtos)


def lista_comuns():

    set_daifiti = set()     
    set_kanui = set()

    for produtos in produtos_com_desconto:
        set_daifiti.add(produtos['titulo'])

    for produtos in produtos2:
        set_kanui.add(produtos['titulo'])

    comuns = set_daifiti.intersection(set_kanui)

    titulos("Produtos disponiveis em ambos os sites")

    if len(comuns) == 0:
        print("Obs.: * Não há produtos comuns aos dois sites")
    else:
        for produtos in comuns:
            print(produtos)

def totalizacao_precos():
    total_preco = 0  

    for produto in produtos_total:
        preco = produto['preco']
        preco_numerico = float(preco.replace("R$", "").replace(",", "."))  

        total_preco += preco_numerico

    titulos("Totalização de preços Daifiti e Kanui")
    print(f"Total de Preços: R$ {total_preco:2f}")



def preco_maximo():
    valor_maximo = float(input("Valor máximo: "))
    produtos = []

    for produto in produtos_total:
        preco = float(produto["preco"].replace("R$", "").replace(".", "").replace(",", "."))

        if preco <= valor_maximo:
            produtos.append(produto)

    if len(produtos) == 0:
        print("Nenhum produto encontrado dentro do valor máximo.")
    else:
        print(f"Produtos com preço até R${valor_maximo:.2f}:")
        for produto in produtos:
            print(f"Produto: {produto['titulo']}")
            print(f" Preço com desconto: {produto['preco']}")
            print()





while True:
    titulos("Produtos")    
    print("1. Daifiti")
    print("2. Kanui ")
    print("3. Todos os produtos")
    print("4. Apenas na Daifiti")
    print("5. Apenas na Kanui")
    print("6. Presente em ambos os sites")
    print("7. Total de preços em ambos")    
    print("8. Produtos sem deconto")    
    print("9. Pesquisa produtos por valor")    
    opcao = int(input("Opção: "))
    if opcao == 1:
        lista_daifiti()
    elif opcao == 2:
        lista_kanui()
    elif opcao == 3:
        lista_todos()
    elif opcao == 4:
        apenas_daifiti()
    elif opcao == 5:
        apenas_kanui()
    elif opcao == 6:
        lista_comuns()
    elif opcao == 7:
        totalizacao_precos()
    elif opcao == 8:
        pass
    elif opcao == 9:
        preco_maximo()
    else:
        break



