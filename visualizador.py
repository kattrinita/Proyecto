import seaborn as sns
import matplotlib.pyplot as plt

def visualizador(df, maximos_df):
   
    sns.set_theme(style="whitegrid")    #ajusto el diagrama
    plt.figure(figsize=(14, 7))
    
    sns.lineplot(x='2Theta', y='Iobs', data=df, 
                 label='Señal Original (Iobs)', color='blue', alpha=0.5)    #grafica la señal orignal
    
    sns.lineplot(x='2Theta', y='Linea_Base', data=df, 
                 label='Fondo / Línea Base', color='green', linestyle='--')     #grafica la linea de base amorfa
    
    sns.lineplot(x='2Theta', y='Iobs_Limpia', data=df, 
                 label='Señal Limpia', color='red', linewidth=1.5)      #grafica la señal aplanada

    sns.scatterplot(x='2Theta', y='Iobs_maxima', data=maximos_df,       #marca los picos maximos
                        color='black', marker='x', s=50,
                        label='Máximos Detectados', zorder=5)

    plt.title('Procesamiento de Señal DRX y Detección de Picos', fontsize=16)
    plt.xlabel('Ángulo 2θ ', fontsize=12)
    plt.ylabel('Intensidad', fontsize=12)
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    plt.show()       # Mostrar el gráfico