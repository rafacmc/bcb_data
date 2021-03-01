import pandas as pd
import requests
import io, re

from datetime import date, timedelta, datetime

class Focus:
    
    def __init__(self, time_expect="monthly"):
        
        self.time_expect = time_expect
        
        def period(period):
            
            switcher = {
                "monthly": "ExpectativaMercadoMensais",
                "mensal": "ExpectativaMercadoMensais",
                "m": "ExpectativaMercadoMensais",
                "annual": "ExpectativasMercadoAnuais",
                "anual": "ExpectativasMercadoAnuais",
                "a": "ExpectativasMercadoAnuais"
            }
            
            return switcher.get(period, "Invalid argument.")
        
        def rename(name):
            if re.search(r"(?i)selic", str(name)):
                return "SELIC"
            elif re.search(r"(?i)câmbio", str(name)):
                return "USDBRL"
            elif re.search(r"(?i)produção industrial", str(name)):
                return "INDUSTRIA"
            elif re.search(r"(?i)balança comercial", str(name)):
                return "BC"
            elif re.search(r"(?i)pagamentos", str(name)):
                return "BP"
            elif re.search(r"(?i)fiscal", str(name)):
                return "FISCAL"
            elif re.search(r"(?i)pib agropec", str(name)):
                return "PIB_AGRO"
            elif re.search(r"(?i)pib industrial", str(name)):
                return "PIB_INDU"
            elif re.search(r"(?i)pib serviços", str(name)):
                return "PIB_SERV"
            elif re.search(r"(?i)pib total", str(name)):
                return "PIB"
            elif re.search(r"(?i)administrados", str(name)):
                return "PADM"
            else:
                return name
        
        url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"+str(period(self.time_expect))+"?$top=1000000&$format=text/csv&$select=Indicador,Data,DataReferencia,Media,Mediana,DesvioPadrao,CoeficienteVariacao,Minimo,Maximo,numeroRespondentes,baseCalculo"
            
        request = requests.get(url)
        data = io.StringIO(request.text)
        self.df = pd.read_csv(data)
        
        self.df.columns = ["indicator", "date", "reference_date", "mean", "median", "sd",
                           "var_coeficient", "min", "max", "respondents_number", "calc_base"]
        
        for col in ["mean", "median", "sd", "var_coeficient", "min", "max"]:
            self.df[col] = self.df[col].apply(lambda x: float(str(x).replace(",", ".")))
            
        self.df["date"] = self.df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        self.df["reference_date"] = self.df["reference_date"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        self.df["indicator"] = self.df["indicator"].apply(rename)
        
        if period(self.time_expect) == "ExpectativaMercadoMensais":
            self.df["reference_date"] = self.df["reference_date"].apply(lambda x: datetime.strptime(str(x), "%m/%Y"))
            self.df.insert(3, "reference_year", self.df["reference_date"].apply(lambda x: x.year))
            self.df.insert(4, "reference_month", self.df["reference_date"].apply(lambda x: x.month))
        
    
    def get(self, indicator=["IGP-M", "IPCA", "SELIC", "USDBRL"], start_date="2000-01-03"):
        
        self.indicator = list(indicator)
        self.start_date = start_date
        
        self.filter_df = self.df[(self.df["indicator"].isin(self.indicator))&(self.df["date"]>=self.start_date)]
        
        return self.filter_df.set_index("indicator")


class FocusTop5:
    
    def __init__(self, time_expect="monthly"):

        self.time_expect = time_expect
        
        def period(period):
            
            swither = {
                "monthly": "ExpectativasMercadoTop5Mensais",
                "mensal": "ExpectativasMercadoTop5Mensais",
                "m": "ExpectativasMercadoTop5Mensais",
                "annual": "ExpectativasMercadoTop5Anuais",
                "anual": "ExpectativasMercadoTop5Anuais",
                "a": "ExpectativasMercadoTop5Anuais"
            }
            
            return swither.get(period, "Invalid argument.")
        
        def rename(name):
            if re.search(r"(?i)selic", str(name)):
                return "Selic"
            elif re.search(r"(?i)câmbio", str(name)):
                return "USDBRL"
            else:
                return name
            
        url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"+str(period(self.time_expect))+"?$top=2000000&$format=text/csv&$select=Indicador,Data,DataReferencia,Media,Mediana,DesvioPadrao,CoeficienteVariacao,Minimo,Maximo"
            
        request = requests.get(url)
        data = io.StringIO(request.text)
        self.df = pd.read_csv(data)
        
        self.df.columns = ["indicator", "date", "reference_date", "mean", "median", "sd", "var_coeficient", "min", "max"]
        
        self.df["indicator"] = self.df["indicator"].apply(rename)
        
        if period(self.time_expect) == "ExpectativasMercadoTop5Mensais":
            self.df["reference_date"] = self.df["reference_date"].apply(lambda x: datetime.strptime(str(x), "%m/%Y"))
            self.df.insert(3, "reference_year", self.df["reference_date"].apply(lambda x: x.year))
            self.df.insert(4, "reference_month", self.df["reference_date"].apply(lambda x: x.month))
    
    
    def get(self, indicator=["IGP-M", "IPCA", "SELIC", "USDBRL"], start_date="2000-01-03"):
        
        self.indicator = list(indicator)
        self.start_date = start_date
        
        self.filter_df = self.df[(self.df["indicator"].isin(self.indicator))&(self.df["date"]>=self.start_date)]
        
        return self.filter_df.set_index("indicator")


class FocusPIB:
    
    def __init__(self):
        
        url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoTrimestrais?$top=2000000&$format=text/csv"
        
        request = requests.get(url)
        data = io.StringIO(request.text)
        self.df = pd.read_csv(data, sep=",")
        
        self.df.columns = ["indicator", "date", "reference_date", "mean", "median", "sd", "var_coeficient",
                           "min", "max", "respondents_number"]

        self.df["reference_date"] = self.df["reference_date"].apply(lambda x: datetime.strptime(str(x), "%m/%Y"))
        
        
    def get(self):
        
        return self.df.set_index("indicator")


