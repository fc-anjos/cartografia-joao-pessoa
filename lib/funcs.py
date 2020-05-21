import subprocess


def row_slice_to_int(row, column, index):
    divisao = row[column][0:index]
    return int(divisao)


def cnae_secao(row):
    return get_secao(row["CNAE 2.0 Divisao"])


def get_secao(divisao):
    if divisao < 5:
        return "AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA"
    elif 5 <= divisao < 10:
        return "INDÚSTRIAS EXTRATIVAS"
    elif 10 <= divisao < 35:
        return "INDÚSTRIAS DE TRANSFORMAÇÃO"
    elif 35 <= divisao < 36:
        return "ELETRICIDADE E GÁS"
    elif 36 <= divisao < 41:
        return "ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO"
    elif 41 <= divisao < 45:
        return "CONSTRUÇÃO"
    elif 45 <= divisao < 49:
        return "COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS"
    elif 49 <= divisao < 55:
        return "TRANSPORTE, ARMAZENAGEM E CORREIO"
    elif 55 <= divisao < 58:
        return "ALOJAMENTO E ALIMENTAÇÃO"
    elif 58 <= divisao < 64:
        return "INFORMAÇÃO E COMUNICAÇÃO"
    elif 64 <= divisao < 68:
        return "ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS"
    elif 68 <= divisao < 69:
        return "ATIVIDADES IMOBILIÁRIAS"
    elif 69 <= divisao < 75:
        return "ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS"
    elif 75 <= divisao < 84:
        return "ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES"
    elif 84 <= divisao < 85:
        return "ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL"
    elif 85 <= divisao < 86:
        return "EDUCAÇÃO"
    elif 86 <= divisao < 90:
        return "SAÚDE HUMANA E SERVIÇOS SOCIAIS"
    elif 90 <= divisao < 94:
        return "ARTES, CULTURA, ESPORTE E RECREAÇÃO"
    elif 94 <= divisao < 97:
        return "OUTRAS ATIVIDADES DE SERVIÇOS"
    elif 97 <= divisao < 99:
        return "SERVIÇOS DOMÉSTICOS"
    elif divisao >= 99:
        return "ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS"
    else:
        raise ValueError("Uma divisão não pôde ser classificada em seção")


def get_bins(df, column, k=5):
    min_v = df[column].min()
    max_v = df[column].max()

    array = []

    for i in range(k + 1):
        step = max_v / (k + 1)
        array.append(round(step * (i + 1), 0))
    return array


def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        k = txt.get_text()
        try:
            txt.set_text(mapping[int(float(k))])
        except ValueError:
            pass


def to_kml(df, output):
    command = "ogr2ogr -f KML {0}.kml {0}.json ".format(output)
    with open("{0}.json".format(output), "w") as f:
        f.write(df.to_crs(epsg=4326).to_json())

    subprocess.call(command, shell=True)


def export(df, output, epsg):
    kml_output = "./OUTPUT/KML/" + output
    csv_output = "./OUTPUT/CSV/" + output + ".csv"
    shp_output = "./OUTPUT/SHP/" + output

    without_geometry = df.loc[:, df.columns != "geometry"]
    without_geometry.to_csv(csv_output)

    df_projected = df.to_crs(epsg=3857)
    to_kml(df_projected, kml_output)
    df_projected.to_file(shp_output)


def get_renda_per_capita(row):
    try:
        renda = row["rendimento_nominal"] / row["num_pessoas"]
    except (ValueError, ZeroDivisionError):
        print(row["rendimento_nominal"])
        print(row["num_pessoas"])
        return np.nan
    return renda


def get_renda_por_trabalhador(row):
    try:
        renda = row["rendimento_nominal"] / row["num_pessoas_rendimento"]
    except (ValueError, ZeroDivisionError):
        return np.nan
    return renda


def get_area(row):
    return row["geometry"].area / 10000


def get_density(row):
    density = row["MORADORES"] / row["area"]
    return density
