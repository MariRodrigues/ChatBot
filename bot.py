import requests
import json
import re
import time
import datetime
from datetime import datetime



class Bot:
    def __init__(self):
        self.nome = "Dona Lourdes"
        self.status = False
        self.aeroporto = False
        self.cidadeAtual = ""
        self.cidadeDestino = ""
        self.dataPartida = ""
        self.dataVolta = ""
        
    def processamento(self, mensagem):
        generics = ["oi", "olá", "hello", "hi", "oie", "oe", "oii", "oiii", "iai", "eae"]

        horaAtual = datetime.now().hour

        if mensagem in generics:
            print(horaAtual)
            if horaAtual > 5 and horaAtual < 12:
                return "Olá, bom dia! Diga <strong>INICIAR</strong> para começarmos a planejar sua viagem!"
            elif horaAtual >= 12 and horaAtual < 18:
                return "Olá, boa tarde! Diga <strong>INICIAR</strong> para começarmos a planejar sua viagem!"
            elif horaAtual > 18:
                return "Olá, boa noite! Diga <strong>INICIAR</strong> para começarmos a planejar sua viagem!"

        # -------------- VIAGENS CONVERSA -------------------------
        
        elif mensagem == "iniciar":
            self.status = True
            return "Em qual cidade vocês está? <br> Responda nesse formato: <strong>'em X'</strong> para que eu possa te compreender."

        elif re.findall('em', mensagem) and self.status == True:
            cidadeAtual = re.findall("[^em].*", mensagem)
            cidadeAtual = cidadeAtual[0].strip()
            return self.siglaAeroporto(cidadeAtual, "embarque")

        
        elif re.findall('para', mensagem) and self.status == True and self.aeroporto == False:
            cidadeDestino = re.findall("[^para].*", mensagem)
            cidadeDestino = cidadeDestino[0].strip()
            return self.siglaAeroporto(cidadeDestino, "destino")

        # fazer regex melhor para pegar datas no formato desejado
        elif re.findall('data', mensagem) and self.status == True:
            dataPartida = re.findall("[^data].*", mensagem)
            self.dataPartida = dataPartida[0].strip()
            self.dataVolta = ""
            return self.viagem("somente ida")

        elif re.findall('ida', mensagem) and self.status == True:
            dataPartida = re.findall("[^ida].*", mensagem)
            self.dataPartida = dataPartida[0].strip()
            return "E qual a data de volta? <br> Digite <strong>volta AAAA-MM-DD</strong>"

        elif re.findall('volta', mensagem) and self.status == True:
            dataVolta = re.findall("[^volta].*", mensagem)
            self.dataVolta = dataVolta[0].strip()
            return self.viagem("ida e volta")

        # ----------
        
        elif re.findall('no', mensagem) and self.aeroporto == True:
            sigla = re.findall("[^no].*", mensagem)
            sigla = sigla[0].strip().upper()
            return self.atribuirSigla(sigla, "embarque")

        elif re.findall('para', mensagem) and self.aeroporto == True:
            sigla = re.findall("[^para].*", mensagem)
            sigla = sigla[0].strip().upper()
            return self.atribuirSigla(sigla, "destino")

        else:
            return "Desculpe, eu não entendi"

    def atribuirSigla(self, sigla, identificacao):
        if identificacao == "embarque":
            self.cidadeAtual = sigla
            self.aeroporto = False
            return "Registrado. Para qual cidade deseja ir?<br> Diga <strong>'para X'</strong>"
        elif identificacao == "destino":
            self.cidadeDestino = sigla
            self.aeroporto = False
            return "Ok. Caso você tenha data de ida e volta, digite assim: <strong>ida AAAA-MM-DD</strong>. Caso só tenha data de ida, digite: <strong>data AAAA-MM-DD</strong> para que eu possa te entender."  
    
    def siglaAeroporto(self, cidade, identificacao):
        aeroportos = []
        siglas = []
        with open('iata.json', encoding='utf-8-sig') as arquivo:
            iata = json.load(arquivo)
            for aeroporto in iata['Aeroportos']:
                if aeroporto['Localização'].lower() == cidade:
                    aeroportos.append(aeroporto['Nome'])
                    siglas.append(aeroporto['IATA'])
                    
        nomeAeroporto = str(aeroportos).strip('[]')
        sigla = str(siglas).strip("'[]")

        if len(aeroportos) == 0:
            if identificacao == "embarque":
                return "Não há nenhum aeroporto nessa cidade. Diga outra cidade, assim: <strong>'em XXX'</strong>"
            else:
                return "Não há nenhum aeroporto nessa cidade. Diga outra cidade, assim: <strong>'para XXX'</strong>"

        elif len(aeroportos) == 1:
            if identificacao == "embarque":
                self.cidadeAtual = sigla
                return "Nessa cidade tem apenas o " + str(nomeAeroporto).strip("'") + "! Irei registrar como seu local de embarque! Para qual cidade você deseja ir? <br> Diga <strong>'para X'</strong>"
            else:
                self.cidadeDestino = sigla
                return "Nessa cidade tem o " + str(nomeAeroporto).strip("'") + "! Vou registrar como destino! Caso você tenha data de ida e volta, digite assim: <strong>ida AAAA-MM-DD</strong>. Caso só tenha data de ida, digite: <strong>data AAAA-MM-DD</strong> para que eu possa te entender."
            
        elif len(aeroportos) > 1:
            self.aeroporto = True
            if identificacao == "embarque":
                return "Temos o " + str(nomeAeroporto).strip("'") + "! Irá embarcar em qual? Responda com a sigla, assim: <strong>'no XXX'</strong>"
            else:
                return "Temos o " + str(nomeAeroporto).strip("'") + "! Irá desembarcar em qual? Responda com a sigla, assim: <strong>'para XXX'</strong>"

    def viagem (self, mensagem):
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/BR/BRL/pt-BR/"+self.cidadeAtual+"/"+self.cidadeDestino+"/"+self.dataPartida+"/"+self.dataVolta

        headers = {
            'x-rapidapi-key': "a6a5da70edmshc16822384a00f0ep1c0361jsn7e587e7d3abb",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        
        viagem = response.json()
        valorMinimo = str(viagem['Quotes'][0]['MinPrice'])

        if mensagem == "ida e volta":
            print("erro")
            dataVolta = datetime.strptime(self.dataVolta, '%Y-%m-%d')
            dataIda = datetime.strptime(self.dataPartida, '%Y-%m-%d')
            quantidadeDias = abs((dataVolta-dataIda).days)

            seguroViagemMinimo = str(quantidadeDias*70)
            seguroViagemMaximo = str(quantidadeDias*300)

            return "O voo mais barato para esse destino na data informada é de <strong>R$ "+ valorMinimo+"</strong><br>Você pode querer também contratar um <strong>seguro de viagem</strong>, que tal? É recomendado por muitas pessoas para uma viagem mais tranquila. Para a quantidade de dias que você irá ficar lá ("+str(quantidadeDias)+" dias), o preço médio pode variar de <strong>R$"+seguroViagemMinimo+"</strong> até <strong>R$"+seguroViagemMaximo+"</strong>."
        else:
            return "O voo mais barato para esse destino na data informada é de <strong>R$ "+ valorMinimo+"</strong>. Você sabia que pode contratar também um seguro viagem? É recomendado por muitas pessoas para que tenha uma viagem mais tranquila. A média de preço é de <strong>R$70</strong> a <strong>R$300</strong> por dia, dependendo da cobertura. Vale a pena dar uma olhada."
        