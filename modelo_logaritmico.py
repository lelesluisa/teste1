import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

print("Escolha o arquivo csv com uma coluna com os ciclos e outra coluna com a tensão")
arquivo = askopenfilename(filetypes=[("All files", ".txt")], title='Arquivo com os pontos de tensão')

dados = np.genfromtxt(arquivo, delimiter=',', names=True)
ciclos = dados['Ciclo']
tensao = dados['Tensao']

def modelo_logaritmico(x, a, b):
    return a * np.log(x) + b

ciclos_filtrados = ciclos[ciclos > 0]
tensao_filtrada = tensao[ciclos > 0]


parametros_iniciais = [1, max(tensao)]

parametros, _ = curve_fit(modelo_logaritmico, ciclos_filtrados, tensao_filtrada, p0=parametros_iniciais)
a, b = parametros
print(f"Parâmetros ajustados: a={a:.4f}, b={b:.4f}")

tensao_ajustada = modelo_logaritmico(ciclos_filtrados, a, b)

r_quadrado = r2_score(tensao_filtrada, tensao_ajustada)
print(f"R²: {r_quadrado:.4f}")

plt.figure(figsize=(8, 6))

ciclos_expandidos = np.linspace(min(ciclos_filtrados), max(ciclos_filtrados), 50)
tensao_expandidas = np.interp(ciclos_expandidos, ciclos_filtrados, tensao_filtrada)

plt.scatter(ciclos_expandidos, tensao_expandidas, color='blue', label='Dados simulados em MEF', alpha=0.6, s=10)

#plt.plot(ciclos_filtrados, tensao_ajustada, color='red', label='Ajuste Logarítmico')
plt.rcParams.update({'font.family': 'arial', 'font.size': 12})
plt.xlabel('Ciclos')
plt.ylabel('Tensão (MPa)')
plt.legend()
plt.grid()
plt.savefig("plot_dados_experimentais", dpi=300)
plt.show()