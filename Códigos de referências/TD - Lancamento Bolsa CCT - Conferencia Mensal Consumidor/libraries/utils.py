import os
import re
import math
import unidecode
import datetime
import shutil
import requests
import traceback
import variables
import pandas as pd
import pymongo
from Connections.MongoConnect import MongoConnect
from dateutil.relativedelta import relativedelta
from funcoesEmail import EmailMsal
from bs4 import BeautifulSoup
import numpy as np

def capturar_token_prime():
    try:
        email = EmailMsal(variables.CLIENT_ID,
                             variables.CLIENT_SECRET,
                             variables.TENANT_ID,
                             variables.USER_ID,
                             variables.USERNAME_EMAIL,
                             variables.PASSWORD_EMAIL)
        email.set_authority()
        email.set_condidential_client_application()
        token = email.get_access_token()
        retorno = email.get_emails_mailbox(token[1])
        mensagem_body = retorno[1]['value'][0]['bodyPreview']
        lista_codigos = re.findall("[0-9]{8}", mensagem_body)
    except Exception:
        return (False, traceback.format_exc())
    return (True, lista_codigos[0])


def capturar_data_corrente() -> (bool, list):
    """

    :return: _description_
    :rtype: str
    """
    try:
        data_corrente = datetime.date.today()
        data_d1 = data_corrente - datetime.timedelta(1)
        data_corrente_formatada = datetime.datetime.strftime(data_corrente, "%d/%m/%Y")
        data_d1_formatada = datetime.datetime.strftime(data_d1, "%d/%m/%Y")
        return (True, [data_d1_formatada, data_corrente_formatada])
    except Exception:
        return (False, traceback.format_exc())

def calcular_execucao(tempo_init, tempo_fim):
    try:
        return tempo_fim - tempo_init
    except:
        raise

def recupera_registro_pendente() -> (bool, str):
    """ recupera registro com status invalidado, reprovado, bolsa lançada, erro dados e cancelado

    :param str: [description]
    :type str: [type]
    :return: [description]
    :rtype: [type]
    """
    try:
        banco = MongoConnect()
        banco.open_connections()
        # colocar analise_bolsas_descontos
        collection = banco.get_collection(variables.BOLSAS_CONCEDIDAS_COLLECTION_MONGO)
        registro = list(collection.find({"Status da Correção" : "Pendente"}))
        if len(registro) == 0:
            registro = list(collection.find({"Status da Correção" : "Contrato modificado"}))
        if len(registro) > 0:
            registro = registro[0]
            return (True, registro)
        else:
             return (False, "Não existe registros pendentes")
    except Exception:
        print(False, traceback.format_exc())
        return (False, traceback.format_exc())
    finally:
        banco.close_connections()
def verifica_tipo_curso(curso):

    if "Grad. Pres" in curso:
        return "Cursos de Graduação Presencial"
    elif "Grad. Onl" in curso:
        return "Cursos de Graduação Online"
    return None

def verifica_estabelecimento(estabelecimento):

    if "CURITIBA" in estabelecimento:
        return "Pontifícia Universidade Católica do Paraná - Curitiba (PUCPR - CURITIBA)"
    elif "LONDRINA" in estabelecimento:
        return "Pontifícia Universidade Católica do Paraná - Londrina (PUCPR - LONDRINA)"
    elif "MARINGA" in estabelecimento or "MARINGÁ" in estabelecimento:
        return "Pontifícia Universidade Católica do Paraná - Maringá (PUCPR - MARINGÁ)"
    elif "TOLEDO" in estabelecimento:
        return "Pontifícia Universidade Católica do Paraná - Toledo (PUCPR - TOLEDO)"
    else:
        return None

def extrair_ano_semestre(texto):
    padrao = r'\d{4}/\d'
    resultado = re.findall(padrao, texto)
    if resultado:
        return resultado[0]
    else:
        return None

def definir_contrato(registro, status):
    try:
        banco = MongoConnect()
        banco.open_connections()
        colecao_registros = banco.get_collection(variables.BOLSAS_CONCEDIDAS_COLLECTION_MONGO)

        print(status)
        if status != 'Sem Contrato':
            path_contratos = os.path.join(variables.DOWNLOAD_DIRECTORY, "relacao_contratos.xls")
            df = pd.read_excel(path_contratos)
            # Filtra pelo curso do aluno
            # df = df.loc[(df['Tipo de Curso'] == tipo_curso) & (df['Curso'] == registro['Curso do aluno'])]
            # df =  df[df['Tipo de Curso'].isin([registro['Curso']]).values[0]]
            # Aplicar a função aos valores da Grade Curricular e Turma
            df['Ano/Semestre Grade'] = df['Grade Curricular'].apply(extrair_ano_semestre)
            df['Ano/Semestre Turma'] = df['Turma'].apply(extrair_ano_semestre)
            # Ordena valores e seleciona o primeiro registro
            semestres = obter_semestres()
            df = df[df['Ano/Semestre Turma'].isin(semestres)]
            df = df.sort_values(['Ano/Semestre Turma','Ano/Semestre Grade'], ascending=False)
            print(df['Ano/Semestre Turma'])
            if len(df) > 0:
                df = df.iloc[0]
                contrato = df.to_dict()
                print(contrato)
                colecao_registros.update_one({'_id':registro['_id']},
                                            {"$set":{
                                                'Contrato': contrato['Contrato'],
                                                'Grade Curricular': contrato['Grade Curricular'],
                                                'Situação Contrato': contrato['Situação Contrato'],
                                                'Turma Contrato': contrato['Turma'],
                                            }})
                return (True, contrato['Contrato'], contrato['Situação Contrato'], contrato['Turma'])
 
            
            print('Erro ao definir contrato')
        return (False, 'Erro ao definir contrato')
    except Exception:
        print(traceback.format_exc())
        return (False, traceback.format_exc())
    finally:
        banco.close_connections()

def obter_semestres():
    # Obter a data atual
    data_atual = datetime.datetime.now()

    # Obter o ano e o mês atual
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    # Definir o semestre atual com base no mês atual
    if mes_atual >= 1 and mes_atual <= 6:
        semestre_atual = f"{ano_atual}/1"
    else:
        semestre_atual = f"{ano_atual}/2"

    # Definir o próximo semestre com base no semestre atual
    if semestre_atual.endswith("/1"):
        proximo_semestre = f"{ano_atual}/2"
    else:
        proximo_semestre = f"{ano_atual + 1}/1"

    # Definir o próximo do próximo semestre
    if proximo_semestre.endswith("/1"):
        proximo_do_proximo = f"{ano_atual + 1}/2"
    else:
        proximo_do_proximo = f"{ano_atual + 1}/1"

    # Retornar os semestres em uma lista
    semestres = [semestre_atual, proximo_semestre, proximo_do_proximo]
    return semestres

def atualizar_bd(registro, status):
    try:
        banco = MongoConnect()
        banco.open_connections()
        collection = banco.get_collection(variables.BOLSAS_CONCEDIDAS_COLLECTION_MONGO)
        now = datetime.datetime.now()
        hoje = now.strftime("%d-%m-%Y-%H-%M-%S")
        data = hoje.split('-')

        if status[0]:
            if 'contrato' in status[1].lower():
                collection.update_one({"_id" : registro["_id"]},
                                {'$set':{"Status da Correção": 'Contrato modificado', 
                                "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                                }})
            elif 'alunos' in status[1].lower() and 'excluída imediatamente' in status[1].lower():
                collection.update_one({"_id" : registro["_id"]},
                                {'$set':{"Status da Correção": 'Bolsa Excluída', 
                                "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                                }})
            elif 'alunos' in status[1].lower() and 'excluída próximo semestre' in status[1].lower():
                collection.update_one({"_id" : registro["_id"]},
                                {'$set':{"Status da Correção": 'Bolsa Excluída Próximo Semestre', 
                                "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                                }})
            elif 'porcentagem da bolsa' in status[1].lower():
                collection.update_one({"_id" : registro["_id"]},
                                {'$set':{"Status da Correção": 'Alterado porcentagem da bolsa', 
                                "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                                }})
        else:
            if 'contrato válido' in status[1].lower() or 'bolsa encontrada' in status[1].lower() or 'em contratos' in status[1].lower() or 'excluir contrato' in status[1].lower() or 'em alunos' in status[1].lower():
                collection.update_one({"_id" : registro["_id"]},
                            {'$set':{"Status da Correção":  status[1], 
                            "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                            }})
            else:
                collection.update_one({"_id" : registro["_id"]},
                            {'$set':{"Status da Correção": 'Exceção desconhecida na tela de contratos', 
                            "Execução": datetime.datetime(int(data[2]), int(data[1]), int(data[0]), int(data[3]), int(data[4]), int(data[5]))
                            }})
        return (True, 'Atualizado status do documento.')
    except Exception:
        print(False, traceback.format_exc())
        return (False, traceback.format_exc())
    finally:
        banco.close_connections()

def verificar_existencia_bolsa_contrato_confirmado(html_text, tipo_bolsa):
    try:
        bs= BeautifulSoup(html_text, 'html.parser')
        table = bs.find_all('table', {'width': '*','cellspacing': '1', 'cellpadding': '5', 'class': 'table-padrao'})
        dados = tableDataText(table[1])
        df = pd.DataFrame(dados)
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        tamanho_df = len(df) - 1
        print(df)
        # df.to_excel('teste.xlsx')
        filtro = (df['Tipo Bolsa'] == tipo_bolsa) & (df['Percentual'] != '0,00 %')
        df_filtrado = df[filtro]
        print(df_filtrado)
        if len(df_filtrado) == 1:
            index = df_filtrado.index[0]
            percentual_bolsa = str(df_filtrado['Percentual'].values[0])
            percentual_bolsa = percentual_bolsa.replace(' %', '')
            percentual_bolsa = percentual_bolsa.replace(',', '.')
            print(True, percentual_bolsa)
            return True, index, percentual_bolsa
        else:
            return False, 'Erro'

    except:
        print(False, traceback.format_exc())
        return False, traceback.format_exc()


def tableDataText(table):    
    """ Parses a html segment started with tag <table> followed 
    by multiple <tr> (table rows) and inner <td> (table data) tags. 
    It returns a list of rows with inner columns. 
    Accepts only one <th> (table header/data) in the first row.
    Args:
        table (_type_): str contendo a tabela

    Returns:
        List: Retorna lista contendo a tabela
    """

    try:
        rows = []
        trs = table.find_all('tr')
        headerow = rowgetDataText(trs[0], 'th')
        if headerow: # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs: # for every table row
            line = rowgetDataText(tr, 'td')
            if len(line) > 0:
                rows.append(line) # data row
        return rows
    except:
        raise

def rowgetDataText(tr, coltag='td'): # td (data) or th (header)
    """ Separa a str de origem em uma lista. Separador é o td
    Args:
        tr (_type_): str completa
        coltag (str, optional): separador
    Returns:
        List: Lista contendo a str separada por "colunas".
    """
    try:   
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    except:
        raise

def get_datas_alteracao_contrato(turma, data_de, data_ate):
    try:
        data_atual = datetime.datetime.now()
        lista_semestres = obter_semestres()
        ano_turma = extrair_ano_semestre(turma)
        ano, turma = ano_turma.split('/')
        if (ano_turma == lista_semestres[1] or ano_turma == lista_semestres[2]) and int(ano) >= int(data_atual.year):
            return True, data_de, data_ate, 'Contrato'
        else:
            if data_atual.day <= 18:
                mes = data_atual.month + 1
                if mes > int(data_ate.split('/')[1]):
                    return False, 'Erro'
                if len(str(mes)) == 1:
                    mes = f"0{mes}"
                data_de = f"01/{mes}/{ano}"
                return True, data_de, data_ate, 'Período'
            else:
                mes = data_atual.month + 2
                if mes > int(data_ate.split('/')[1]):
                    return False, 'Erro'
                if len(str(mes)) == 1:
                    mes = f"0{mes}"
                data_de = f"01/{mes}/{ano}"
                return True, data_de, data_ate, 'Período'
    except:
        print(False, traceback.format_exc())
        return False, traceback.format_exc()

def get_valor_mensalidade(html_text) -> (bool, str):
    try:
        bs= BeautifulSoup(html_text, 'html.parser')
        table = bs.find_all('table', {'width': '*','cellspacing': '1', 'cellpadding': '5', 'class': 'edit'})
        dados = tableDataText(table[5])
        df = pd.DataFrame(dados)
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])


        filtered_df = df[df['Vlr.Bruto'].str.contains(',' , na=False)]
        filtered_df = filtered_df.reset_index(drop=True)

        sub_total_row = filtered_df[filtered_df['Vcto'] == 'Sub-Total:']
        print(sub_total_row)
        if not sub_total_row.empty:
            target_index = sub_total_row.index[0]
            target_index = target_index - 1
            if target_index >= 0:
                return True, filtered_df.iloc[target_index]['Vlr.Bruto']

        return False, 'Não encontrado'

    except:
        print(False, traceback.format_exc())
        return False, traceback.format_exc()

def compara_saldo_final_bolsa(html_text, valor_mensalidade) -> (bool, str):
    try:
        valor_limite = 8
        valor_mensalidade_acima = 0
        valor_mensalidade_abaixo = 0
        bs = BeautifulSoup(html_text, 'html.parser')
        table = bs.find_all('table', {'class': 'edit'})
        dados = tableDataText(table[1])
        df = pd.DataFrame(dados)
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        ultima_linha = df.iloc[-2]
        saldo_titulo = (ultima_linha['Saldo do Título'])
        saldo_titulo = float(ultima_linha['Saldo do Título'].replace('.', '')[:-3])
        
        valor_mensalidade = float(valor_mensalidade.replace('.', '')[:-3])
        valor_mensalidade_acima = valor_mensalidade + valor_limite
        valor_mensalidade_abaixo = valor_mensalidade - 8

        if saldo_titulo >= valor_mensalidade_abaixo and saldo_titulo <= valor_mensalidade_acima:
            return True, saldo_titulo, valor_mensalidade
        else:
            return False, saldo_titulo,  valor_mensalidade
    except:
        print(False, traceback.format_exc())
        return False, traceback.format_exc()

def get_grade_aluno(registro):
    try:
        banco = MongoConnect()
        banco.open_connections()
        # colocar analise_bolsas_descontos
        collection = banco.get_collection(variables.BOLSAS_CONCEDIDAS_COLLECTION_MONGO)
        registro = list(collection.find({"_id": registro['_id']}))
        if len(registro) == 0:
            raise
        if len(registro) > 0:
            registro = registro[0]
            return (True, registro['Grade Curricular'])
        print(False, traceback.format_exc())
        return (False, traceback.format_exc())
    finally:
        banco.close_connections()

def obter_proximo_semestre():
    data_atual = datetime.datetime.now()
    if data_atual.month >= 7:
        return f"01/01/{data_atual.year + 1}"
    else:
        return f"01/07/{ano}"