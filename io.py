# -*- coding: utf-8 -*-
"""io.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m83GzqugQbXn0zPrDMwSvRFIVLd3f1R6
"""

# -*- coding: utf-8 -*-
"""graficos_neon_fundo_preto_reformulado.py"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from google.colab import drive
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Constantes e configurações
DRIVE_MOUNT_PATH = "/content/drive"
GRAPHPATH = "/content/drive/MyDrive/graficos"
SUMMARYPATH = "/content/drive/MyDrive/sumarios"
CSV_URL = "https://docs.google.com/spreadsheets/d/11VcmYQ9EoMUJ3lTR-4vWfPs43A9y4D6vWzVm9g_LJ-A/export?format=csv&gid=1666118297"
NEON_PALETTE = ['#39FF14', '#FF073A', '#FFD700', '#00FFFF', '#FF69B4']  # Cores neon
FIGSIZE = (10, 6)

# Configurando o estilo neon com fundo preto
sns.set(style="whitegrid")
plt.rcParams.update({
    'figure.facecolor': 'black',  # Fundo da figura preto
    'axes.facecolor': 'black',    # Fundo dos eixos preto
    'axes.edgecolor': 'white',    # Bordas dos eixos brancas
    'xtick.color': 'white',       # Cor dos ticks do eixo X
    'ytick.color': 'white',       # Cor dos ticks do eixo Y
    'text.color': 'white',        # Cor do texto branca
    'legend.facecolor': 'black',  # Fundo da legenda preto
    'axes.labelcolor': 'white',   # Cor do rótulo dos eixos branca
    'grid.color': 'gray'          # Cor da grade cinza
})

def load_data(url):
    try:
        df = pd.read_csv(url, delimiter=',', encoding='utf-8')
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# Função para salvar gráficos
def save_fig(filename):
    plt.savefig(os.path.join(GRAPHPATH, filename), dpi=300, bbox_inches='tight')
    plt.close()

def create_figure():
    return plt.figure(figsize=FIGSIZE)

# Funções para gerar gráficos de violino
def generate_violinplot(df, x, y, hue, title, filename, split=False):
    create_figure()
    sns.violinplot(x=x, y=y, hue=hue, data=df, split=split, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

# Funções para gerar histogramas
def generate_histplot(df, x, hue, title, filename, bins=20):
    create_figure()
    sns.histplot(data=df, x=x, hue=hue, bins=bins, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

# Funções para gerar KDEs
def generate_kdeplot(df, x, hue, title, filename):
    create_figure()
    sns.kdeplot(data=df, x=x, hue=hue, palette=NEON_PALETTE, fill=True)
    plt.title(title)
    save_fig(filename)

# Função para gerar regressões polinomiais
def generate_polynomial_regression(df, x, y, degree, title, filename):
    create_figure()
    X = df[[x]]
    y = df[y]

    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    X_range_poly = poly.transform(X_range)

    plt.scatter(X, y, color='white', label='Dados Reais')
    plt.plot(X_range, model.predict(X_range_poly), color=NEON_PALETTE[0], label=f'Regressão Polinomial (Grau {degree})')
    plt.title(title)
    plt.legend()
    save_fig(filename)

# Função para gerar sumário estatístico detalhado
def generate_statistical_summary_detailed(df, col):
    try:
        summary = df[col].describe()
        print(f"Sumário estatístico detalhado para {col}:\n{summary}")
        summary.to_csv(os.path.join(SUMMARYPATH, f'summary_{col}.csv'))
    except Exception as e:
        print(f"Erro ao gerar o sumário estatístico detalhado: {e}")

# Função para gerar gráficos adicionais
def generate_boxplot(df, x, y, hue, title, filename):
    create_figure()
    sns.boxplot(x=x, y=y, hue=hue, data=df, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

def generate_barplot(df, x, y, hue, title, filename):
    create_figure()
    sns.barplot(x=x, y=y, hue=hue, data=df, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

if __name__ == "__main__":
    # Montar o Google Drive
    drive.mount(DRIVE_MOUNT_PATH, force_remount=True)
    os.makedirs(GRAPHPATH, exist_ok=True)
    os.makedirs(SUMMARYPATH, exist_ok=True)

    # Carregar os dados
    df = load_data(CSV_URL)

    if df is not None:
        # Verificar se a coluna 'Gender' existe antes de aplicarmos a transformação categórica
        if 'Gender' in df.columns:
            le_gender = LabelEncoder()
            df['Gender_Num'] = le_gender.fit_transform(df['Gender'])
        else:
            print("Coluna 'Gender' não encontrada!")

        # Verificar se a coluna 'Diagnosis' existe antes de aplicarmos a transformação categórica
        if 'Diagnosis' in df.columns:
            le_diagnosis = LabelEncoder()
            df['Diagnosis_Num'] = le_diagnosis.fit_transform(df['Diagnosis'])
        else:
            print("Coluna 'Diagnosis' não encontrada!")

        # Gráficos de violino
        if 'Gender' in df.columns and 'Diagnosis' in df.columns:
            generate_violinplot(df, 'Diagnosis', 'Age', 'Gender', 'Violin: Idade por Gênero e Diagnóstico', 'violin_idade_diagnostico_genero.png', split=True)
            generate_violinplot(df, 'Gender', 'Age', 'Diagnosis', 'Violin: Idade por Gênero e Diagnóstico', 'violin_idade_genero_diagnostico.png', split=False)
        else:
            print("Colunas necessárias para o gráfico de violino não encontradas!")

        # Histogramas
        if 'Gender' in df.columns:
            generate_histplot(df, 'Age', 'Gender', 'Histograma: Idade por Gênero', 'hist_idade_genero.png', bins=20)
        else:
            print("Coluna 'Gender' não encontrada para o histograma!")

        # KDEs
        if 'Diagnosis' in df.columns:
            generate_kdeplot(df, 'Age', 'Diagnosis', 'KDE: Idade por Diagnóstico', 'kde_idade_diagnostico.png')
        if 'Gender' in df.columns:
            generate_kdeplot(df, 'Age', 'Gender', 'KDE: Idade por Gênero', 'kde_idade_genero.png')

        # Regressões polinomiais
        if 'Diagnosis_Num' in df.columns:
            generate_polynomial_regression(df, 'Age', 'Diagnosis_Num', 3, 'Regressão Polinomial (Grau 3)', 'polynomial_diagnosis_degree_3.png')

        # Sumário estatístico detalhado
        generate_statistical_summary_detailed(df, 'Age')

        # Gráficos adicionais
        if 'Gender' in df.columns and 'Diagnosis' in df.columns:
            generate_boxplot(df, 'Diagnosis', 'Age', 'Gender', 'Boxplot: Idade por Gênero e Diagnóstico', 'boxplot_idade_diagnostico_genero.png')
            generate_barplot(df, 'Diagnosis', 'Age', 'Gender', 'Barplot: Idade por Gênero e Diagnóstico', 'barplot_idade_diagnostico_genero.png')