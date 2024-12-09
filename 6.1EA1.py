import numpy as np
import matplotlib.pyplot as plt

# 1. Definir a função original
def original_function(x, a, b, c):
    """Função exemplo: y = a * sin(b * x) + c"""
    return a * np.sin(b * x) + c

# 2. Parâmetros da função original
original_params = {'a': 2.0, 'b': 1.5, 'c': 0.8}  # Coeficientes iniciais
x = np.linspace(0, 10, 200)  # Domínio da função

# 3. Estatísticas dos coeficientes (média e variância)
param_stats = {
    'a': {'mean': original_params['a'], 'std_dev': 0.3},  # Média 2.0, desvio padrão 0.3
    'b': {'mean': original_params['b'], 'std_dev': 0.2},  # Média 1.5, desvio padrão 0.2
    'c': {'mean': original_params['c'], 'std_dev': 0.1}   # Média 0.8, desvio padrão 0.1
}

# 4. Simulação de Monte Carlo: Gerar curvas com parâmetros aleatórios
n_simulations = 50  # Número de simulações
simulated_curves = []

for _ in range(n_simulations):
    # Sortear parâmetros de uma distribuição normal
    a = np.random.normal(param_stats['a']['mean'], param_stats['a']['std_dev'])
    b = np.random.normal(param_stats['b']['mean'], param_stats['b']['std_dev'])
    c = np.random.normal(param_stats['c']['mean'], param_stats['c']['std_dev'])
    
    # Calcular a curva simulada e adicioná-la à lista
    simulated_curves.append(original_function(x, a, b, c))

# 5. Calcular a curva original
original_curve = original_function(x, **original_params)

# 6. Plotar as curvas
plt.figure(figsize=(12, 6))

# Curvas simuladas
for curve in simulated_curves:
    plt.plot(x, curve, alpha=0.4, color='blue')

# Curva original
plt.plot(x, original_curve, color='red', linewidth=2, label='Função Original')

# Configurações do gráfico
plt.title('Simulação Monte Carlo: Geração de Curvas Sintéticas')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
