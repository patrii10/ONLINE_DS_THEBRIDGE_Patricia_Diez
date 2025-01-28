import pandas as pd
import numpy as np
import variables as var
from pandas.api.types import is_numeric_dtype

import toolbox

from scipy import stats

def is_valid_params(dataframe, target_col, columns, target_type=[], columns_type=[]):
    mensajes = []

    df_types = toolbox.tipifica_variables(dataframe, var.UMBRAL_CATEGORIA, var.UMBRAL_CONTINUA)

    # Analisis variable target_col
    if target_col not in dataframe.columns: # Control para ver si 'target_col' existe en el dataframe
        mensajes.append(f"La columna target '{target_col}' no existe en el dataframe")
    else:
        if len(target_type) > 0: # Control para ver si 'target_col' es una variable del tipo especificado
            target_type_list = df_types[df_types[var.COLUMN_TIPO].isin(target_type)][var.COLUMN_NOMBRE].to_list() #Columnas del dataframe que son del tipo 'target_type'
            if not target_col in target_type_list:
                mensajes.append(f"La columna '{target_col}' no es una variable de tipo {target_type}")

    # Análisis de las columnas
    if len(columns_type) > 0:
        col_not_exist_list = []
        col_not_type_list = []

        column_type_list = df_types[df_types[var.COLUMN_TIPO].isin(columns_type)][var.COLUMN_NOMBRE].to_list() #Columnas del dataframe que son del tipo 'columns_type'

        for col in columns:
            if col not in dataframe.columns: # Control para ver si las columnas 'columns' existen en el dataframe
                col_not_exist_list.append(col)
            elif col not in column_type_list: # Control para ver si las columnas 'columns' son del tipo especificado 'columns_type'
                col_not_type_list.append(col)
        
        if len(col_not_exist_list) > 0:
            mensajes.append(f"Las siguientes columnas no existen en el dataframe: {col_not_exist_list}")
        if len(col_not_type_list) > 0:
            mensajes.append(f"Las siguientes columnas no son del tipo {columns_type}: {col_not_type_list}")

    for m in mensajes:
        print(m)

    return len(mensajes) == 0

# Devuelve las variables númericas especificadas en el parámetro 'columns'
def get_num_colums(dataframe, columns=[]):
    num_columns = []
    for col in columns:
        if is_numeric_dtype(dataframe[col]):
            num_columns.append(col)
    return num_columns

#Valida que los parámetros sean numéricos
def is_valid_numeric(dataframe, target_col, columms=[]):
    result = False
    if is_valid_params(dataframe, target_col, columms, var.TIPO_NUMERIC, var.TIPO_NUMERIC):
        num_columns = get_num_colums(dataframe, columms)
        not_number_columns = []
        for col in columms:
            if not col in num_columns:
                not_number_columns.append(col)
        
        if len(not_number_columns) > 0:
            print(f"Las siguientes columnas no son numéricas: {not_number_columns}")
        else:
            result = True
    
    return result

#Devuelve las columnas que correlan numéricamente
def get_corr_columns_num(dataframe, target_col, columns=[], umbral_corr=0, pvalue=None):
    result_columns = []
    for col in columns:
        corr, p_val = stats.pearsonr(dataframe[target_col].dropna(), dataframe[col].dropna())
        # Verifica que la correlación supera el umbral
        if abs(corr) > umbral_corr:
            # Si pvalue es None, añade la columna
            if pvalue is None:
                result_columns.append(col)
            # Si pvalue no es None, verificar también la significación estadística
            elif p_val <= pvalue:
                result_columns.append(col)
    return result_columns