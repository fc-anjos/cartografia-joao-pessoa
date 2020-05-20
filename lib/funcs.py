def row_slice_to_int(row, column, index):
    divisao = row[column][0:index]
    return int(divisao)

def cnae_secao(row):
    return get_secao(row['CNAE 2.0 Divisao'])

def get_secao(divisao):
    if divisao < 5:
        return 'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA'
    elif 5 <= divisao < 10:
        return 'INDÚSTRIAS EXTRATIVAS'
    elif 10 <= divisao < 35:
        return 'INDÚSTRIAS DE TRANSFORMAÇÃO'
    elif 35 <= divisao < 36:
        return 'ELETRICIDADE E GÁS'
    elif 36 <= divisao < 41:
        return 'ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO'
    elif 41 <= divisao < 45:
        return 'CONSTRUÇÃO'
    elif 45 <= divisao < 49:
        return 'COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS'
    elif 49 <= divisao < 55:
        return 'TRANSPORTE, ARMAZENAGEM E CORREIO'
    elif 55 <= divisao < 58:
        return 'ALOJAMENTO E ALIMENTAÇÃO'
    elif 58 <= divisao < 64:
        return 'INFORMAÇÃO E COMUNICAÇÃO'
    elif 64 <= divisao < 68:
        return 'ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS'
    elif 68 <= divisao < 69:
        return 'ATIVIDADES IMOBILIÁRIAS'
    elif 69 <= divisao < 75:
        return 'ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS'
    elif 75 <= divisao < 84:
        return 'ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES'
    elif 84 <= divisao < 85:
        return 'ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL'
    elif 85 <= divisao < 86:
        return 'EDUCAÇÃO'
    elif 86<= divisao < 90:
        return 'SAÚDE HUMANA E SERVIÇOS SOCIAIS'
    elif 90<= divisao < 94:
        return 'ARTES, CULTURA, ESPORTE E RECREAÇÃO'
    elif 94<= divisao < 97:
        return 'OUTRAS ATIVIDADES DE SERVIÇOS'
    elif 97<= divisao < 99:
        return 'SERVIÇOS DOMÉSTICOS'
    elif divisao >= 99:
        return 'ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS'
    else:
        raise ValueError('Uma divisão não pôde ser classificada em seção')


def get_bins(df, column, k=5):
    min_v = df[column].min()
    max_v = df[column].max()

    array = []

    for i in range(k+1):
        step = max_v/(k+1)
        array.append(round(step*(i+1), 0))
    return array

def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        k = txt.get_text()
        try:
            txt.set_text(mapping[int(float(k))])
        except ValueError:
            pass

def replace_legend(legend, mapping):
    for txt in legend.text:
        k = txt.get_text()
        txt.set_text(mapping[txt])
