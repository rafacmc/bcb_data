# bcb_data
Dados da Pesquisa de Expectativas de Mercado do Banco Central - BCB.

No Jupyter Notebook comece por:
`%run focus.py`
`fc = Focus(time_expect="annual")`
`focus = fc.get()`

Veja alguns exemplos de uso em Boletim_Focus.ipynb.


### Indicadores disponíveis:

**Anual e mensal**
- IGP-DI
- IGP-M
- INP-C
- IPA-DI
- IPA-M
- IPCA
- IPCA-15
- IPC-FIPE
- SELIC - Selic Meta
- INDUSTRIA - Produção Industrial
- USDBRL

**Anual**
- BC - Balança Comercial
- BP - Balanço de Pagamentos
- FISCAL - Fiscal
- PIB_AGRO - PIB Agropecuária
- PIB_INDU - PIB Industrial
- PIB_SERV - PIB Serviços
- PIB - PIB Total
- PADM - Preços Administrados
