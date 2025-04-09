import numpy as np
import matplotlib.pyplot as plt
import os

def curva(x, a, b):
    return a * np.log(x) + b

# Parâmetros reais tirados da simulação_Monte_Carlo
a_real = -9.7697
b_real = 106.6356

#Parâmetros estatísticos variáveis
param_stats = {
    'a_2': {'media': a_real, 'desvio': 0.9},
    'b_2': {'media': b_real, 'desvio': 10},
}

# Lista para guardar as novas curvas
simulados = []

eixo_x = np.linspace(1, 2500, 50)

# Iteração para realizar cada simulação
for _ in range(10000):
    # Gerar coeficientes sorteados
    a_3 = np.random.normal(param_stats['a_2']['media'], param_stats['a_2']['desvio'])
    b_3 = np.random.normal(param_stats['b_2']['media'], param_stats['b_2']['desvio'])
   
    eixo_y = curva(eixo_x, a_3, b_3)
    simulados.append(eixo_y)

y_real = curva(eixo_x, a_real, b_real)

dados_salvar = np.column_stack([eixo_x] + simulados + [y_real])

# Caminho do diretório e do arquivo
diretorio = r"C:\BPL\IA\1D-CNN\PrimeiraIA"
arquivo_csv = os.path.join(diretorio, "curvas_simuladas.csv")


# Criando o cabeçalho do arquivo CSV
header = "eixo_x," + ",".join([f"simulada_{i+1}" for i in range(len(simulados))]) + ",curva_real"

# Salvar em um arquivo CSV com 4 casas decimais
np.savetxt(arquivo_csv, dados_salvar, delimiter=",", header=header, fmt="%.4f", comments='')

plt.figure(figsize=(10, 6))
for i, eixo_y in enumerate(simulados[:100]):  # Exibir apenas 100 curvas
    if i == 0:
        plt.plot(eixo_x, eixo_y, color='blue', alpha=0.1, label="Curvas sintéticas")
    else:
        plt.plot(eixo_x, eixo_y, color='blue', alpha=0.1)

# Plotar a curva real
plt.plot(eixo_x, y_real, color='red', label="Curva Real", linewidth=2)
plt.rcParams.update({'font.family': 'Arial', 'font.size': 12})
plt.xlabel('Ciclos')
plt.ylabel('Tensão (MPa)')
plt.legend()
plt.grid(True)
plt.savefig("plot_1000_curvas", dpi=300)
plt.show()

