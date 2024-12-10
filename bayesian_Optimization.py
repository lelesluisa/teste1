# %%
from bayes_opt import BayesianOptimization
import os
import numpy as np
import subprocess
from tkinter.filedialog import askopenfilename, askdirectory     # Escolher e salvar o diretório de alguma pasta de escolha do usuário 
import functools
from time import time
from plot_strees_curve import Plot_Stress_Time_Curve

# %%
# Função de chamada da simulação ABAQUS
# 
def run_Abaqus(script_simulacao, nome_da_simulacao, garra_S_T_Y, garra_I_T_Y, garra_S_R_Y, garra_I_R_Y, 
               rosca_S_R_X, rosca_S_R_Z, rosca_I_R_X, rosca_I_R_Z, parafuso_T_X, 
               parafuso_T_Z, parafuso_R_X, parafuso_R_Z, diretorio_conter_simulacoes, amplitude_file):


    while True:

        # Monta o comando para rodar o Abaqus sem GUI
        line_command = f"abaqus cae noGui={script_simulacao} -- "
        print(type(nome_da_simulacao))
        # Parâmetros que serão passados como argumentos para dentro da simulação
        extend_parameters = f"--nome_da_simulacao {nome_da_simulacao} --garra_S_T_Y {garra_S_T_Y} --garra_I_T_Y {garra_I_T_Y} --garra_S_R_Y {garra_S_R_Y} --garra_I_R_Y {garra_I_R_Y} --rosca_I_R_X {rosca_I_R_X} --rosca_I_R_Z {rosca_I_R_Z} --rosca_S_R_X {rosca_S_R_X} --rosca_S_R_Z {rosca_S_R_Z} --parafuso_T_X {parafuso_T_X} --parafuso_T_Z {parafuso_T_Z} --parafuso_R_X {parafuso_R_X} --parafuso_R_Z {parafuso_R_Z} --amplitude {amplitude_file}"

        # Concatena o comando e os parâmetros adicionais
        general_command = line_command + extend_parameters     

        print(general_command)     
        
        try:
            # Executa o comando do sistema
            process = subprocess.Popen(general_command, shell=True, cwd=diretorio_conter_simulacoes)
            process.wait()  # Espera o processo terminar

            if process.returncode == 0:
                print("\nSimulação executada com sucesso!\n")
                break  # Sai do loop se o processo foi bem-sucedido
            else:
                # Retorna uma excessão caso, por ventura, o subprocesso não finalize corretamente
                raise Exception("Falha na execução da simulação!")             
                
        except Exception:
            print("Erro na simulação!")
            process.terminate()                                         # Termina o subprocesso
            process.wait()                                              # Espera ele encerrar o finalizamento
            break                                                       # Sai do loop

# %%
# Função de chamada para leitura dos resultados da simulação ABAQUS
# 
def read_Output_Abaqus(script_odb, nome_da_simulacao, diretorio_conter_simulacoes):

    # Monta o comando para rodar o Abaqus sem GUI
    line_command = f"abaqus cae noGui={script_odb} -- "
        
    # Parâmetros que serão passados como argumentos para dentro da simulação
    extend_parameters = f"--nome_da_simulacao {nome_da_simulacao} --diretorioSimulacoes {diretorio_conter_simulacoes}"

    # Concatena o comando e os parâmetros adicionais
    general_command = line_command + extend_parameters 

    try:
            # Executa o comando do sistema
            process = subprocess.Popen(general_command, shell=True)
            process.wait()  # Espera o processo terminar

            if process.returncode == 0:
                print("\nLeitura do arquivo .ODB realizada com sucesso!\n")
    
            else:
                # Retorna uma excessão caso, por ventura, o subprocesso não finalize corretamente
                raise Exception("Falha na execução da leitura do arquivo .ODB!")             
                
    except Exception:
        print("Erro na leitura do arquivo .ODB!")
        process.terminate()                                         # Termina o subprocesso
        process.wait()                                              # Espera ele encerrar o finalizamento
        
    


# %%
# Criando a função objetivo: Garantir que a Energia Cinética / Energia Interna < 10 %.
# 

# black_box_function(...) => temp_f(...)

def black_box_function(script_file, script_odb, nome_simulacao, amp_Curve, diretorio_simulacoes):
    #@actual_decorator
    def temp_f(garra_S_T_Y, garra_I_T_Y, garra_S_R_Y, garra_I_R_Y, rosca_S_R_X, rosca_S_R_Z, rosca_I_R_X, rosca_I_R_Z, parafuso_T_X, parafuso_T_Z, parafuso_R_X, parafuso_R_Z):

        garra_S_T_Y = 1 if garra_S_T_Y > 0.6 else 0
        garra_I_T_Y = 1 if garra_I_T_Y > 0.6 else 0
        garra_S_R_Y = 1 if garra_S_R_Y > 0.6 else 0
        garra_I_R_Y = 1 if garra_I_R_Y > 0.6 else 0

        rosca_S_R_X = 1 if rosca_S_R_X > 0.6 else 0
        rosca_S_R_Z = 1 if rosca_S_R_Z > 0.6 else 0
        rosca_I_R_X = 1 if rosca_I_R_X > 0.6 else 0
        rosca_I_R_Z = 1 if rosca_I_R_Z > 0.6 else 0

        parafuso_T_X = 1 if parafuso_T_X > 0.6 else 0
        parafuso_T_Z = 1 if parafuso_T_Z > 0.6 else 0
        parafuso_R_X = 1 if parafuso_R_X > 0.6 else 0
        parafuso_R_Z = 1 if parafuso_R_Z > 0.6 else 0
                
        # Atualizando o nome da simulação
        nome = (nome_simulacao + "_" +
        f"{round(garra_S_T_Y, 0)}".replace('.', '_') + "_" +
        f"{round(garra_I_T_Y, 0)}".replace('.', '_') + "_" +
        f"{round(garra_S_R_Y, 0)}".replace('.', '_') + "_" +
        f"{round(garra_I_R_Y, 0)}".replace('.', '_') + "_" +
        f"{round(rosca_S_R_X, 0)}".replace('.', '_') + "_" +
        f"{round(rosca_S_R_Z, 0)}".replace('.', '_') + "_" +
        f"{round(rosca_I_R_X, 0)}".replace('.', '_') + "_" +
        f"{round(rosca_I_R_Z, 0)}".replace('.', '_') + "_" +
        f"{round(parafuso_T_X, 0)}".replace('.', '_') + "_" +
        f"{round(parafuso_T_Z, 0)}".replace('.', '_') + "_" +
        f"{round(parafuso_R_X, 0)}".replace('.', '_') + "_" +
        f"{round(parafuso_R_Z, 0)}".replace('.', '_'))
 
        
    
        # Rodando a simulação Abaqus
        run_Abaqus(script_simulacao=script_file, nome_da_simulacao=nome, garra_S_T_Y=garra_S_T_Y, garra_I_T_Y=garra_I_T_Y, garra_S_R_Y=garra_S_R_Y,garra_I_R_Y=garra_I_R_Y, rosca_S_R_X=rosca_S_R_X, rosca_S_R_Z=rosca_S_R_Z,rosca_I_R_X=rosca_I_R_X, rosca_I_R_Z=rosca_I_R_Z, parafuso_T_X=parafuso_T_X,parafuso_T_Z=parafuso_T_Z, parafuso_R_X=parafuso_R_X, parafuso_R_Z=parafuso_R_Z, diretorio_conter_simulacoes=diretorio_simulacoes, amplitude_file=amp_Curve)


        # Chamar o executável .ODB para realizar a leitura da simulação finalizada
        read_Output_Abaqus(script_odb=script_odb, nome_da_simulacao=nome, diretorio_conter_simulacoes=diretorio_simulacoes)

        # Plotar os resultados em .pdf
        tensao = Plot_Stress_Time_Curve(diretorio=diretorio_conter_simulacoes, nome_simulacao=nome)

        return np.random.randint(0, 10)
    
    return temp_f

    

# %% [markdown]
# ## Início do código:
# 
# 1. Consiste em entrar com todos os diretórios e além disso o nome que se deseja dar a simualação        
#         1.1 Escolher o script em python da simulação Abaqus       
#         1.2 Dar um nome a sua simulação         
#         1.3 Escolher o arquivo python responsável pela leitura do arquivo .ODB gerado durante a simulação       
#         1.4 Escolher um diretório para salvar todos os outros arquivos criados durante a simulação pelo próprio Abaqus
#         1.5 Escolher um diretório para salvar os arquivos das curvas de resposta ALLIE e ALLKE

# %%
# Buscar todos os diretórios em que o usuário deseja salvar as simulações e os arquivos de resposta das curvas ALLIE e ALLKE da simulação Abaqus
#

# Verificar se o usuário deseja entrar com novos valores ou se deseja reaproveitar os dados do último ensaio
#
print("\nDeseja entrar com novos valores ou reaproveitar dados já existentes ? [E/R]\n E: Entrar com novos dados\n R: Reaproveitar")
resposta_usuario = input().upper()
if 'E' in resposta_usuario:

    # Usuário dará início a escolha dos novos arquivos e diretórios dessa simulação
    #
    print("Digite o nome do arquivo em que deseja salvar seus dados")
    salvar_Dados = input()

    print("\nEscolha o script '.py' da simulação\n")
    # filetypes: Permite aparecer na janela apenas os tipos de arquivos especificados, de modo a filtrar a quantidade de arquivos que aparecem para seleção
    # intialdir: Qual o diretorio incial será apresentado na tela pop-up que abrir. Isso serve para caso seu arquivo já esteja próximo de onde está rodando o código você perca menos tempo abrindo outras pastas até chegar ao arquivo destino     
    # title: Escreve uma mensagem no topo do pop-up
    script_simulacao = askopenfilename(filetypes=[("All files", ".py")], initialdir=os.getcwd(), title='Please enter the script .py file of the simulation')    

    print("\nDê um nome a sua simulacao\n")
    nome_da_simulacao = input()

    print("\nEscolha o arquivo python de leitura dos resultados .odb da simulacao\n")
    script_odb = askopenfilename(filetypes=[("All files", ".py")], initialdir=os.getcwd(), title='Please enter the ODB script .py file')

    print("\nEscolha o arquivo de amplitudes a ser utilizado na simulação\n")
    amplitude_file = askopenfilename(filetypes=[("All files", ".txt")], initialdir=os.getcwd(), title='Please enter with the amplitude curve filename')

    print("\nEscolha um diretorio para salvar todos os arquivos das simulações Abaqus\n")
    diretorio_conter_simulacoes = askdirectory(title='Please enter the directory to save all abaqus simulation files')

    #print("\nEscolha um diretorio para salvar os dados das curvas de energia ALLIE e ALLKE\n")
    #diretorio_curvas_de_energia = askdirectory(title='Please enter the directory to save all the energy output files')

elif 'R' in resposta_usuario:
    dados_Salvos = askopenfilename(filetypes=[("All files", ".txt")], initialdir=os.getcwd(), title="Entre com os dados já pré existentes")
    with open(dados_Salvos, 'r') as file:
        conteudo = file.readlines()
        
        script_simulacao = conteudo[0].strip()
        nome_da_simulacao = conteudo[1].strip()
        script_odb = conteudo[2].strip()
        amplitude_file = conteudo[3].strip()
        diretorio_conter_simulacoes = conteudo[4].strip()
        #diretorio_curvas_de_energia = conteudo[5].strip()

else:
    print("\nComando não encontrado.\nDigite E ou R para prosseguir com o ensaio.\n")

# %%
# Criando um Dictionary() que irá conter todos os inputs do usuário e caso este queira recuperar essas informações não precisa entrar com todos os diretórios novamente
#
if resposta_usuario == 'E':
    conter_Dados = {'script': script_simulacao,
                    'ID': nome_da_simulacao,
                    'Odb': script_odb,
                    'Amp curve': amplitude_file,
                    'simulacoes_dir': diretorio_conter_simulacoes}
                   

    salvar_conter_Dados = os.path.join(diretorio_conter_simulacoes, salvar_Dados + ".txt")
    with open(salvar_conter_Dados, 'w') as file:
        for conteudo in conter_Dados.values():
            file.write(f"{conteudo}\n")

# %%
# Defina o espaço de busca para o mass scaling
pbounds = {'garra_S_T_Y':(0, 1), 'garra_I_T_Y':(0,1), 'garra_S_R_Y':(0,1), 'garra_I_R_Y':(0,1),
               'rosca_S_R_X':(0, 1), 'rosca_S_R_Z':(0, 1), 'rosca_I_R_X':(0, 1), 'rosca_I_R_Z':(0,1), 'parafuso_T_X':(0,1), 
               'parafuso_T_Z':(0,1), 'parafuso_R_X':(0,1), 'parafuso_R_Z':(0, 1)}  # Ajuste o intervalo conforme necessário

# Inicialize o otimizador bayesiano
optimizer = BayesianOptimization(
    f=black_box_function(script_file=script_simulacao, script_odb=script_odb, nome_simulacao=nome_da_simulacao, amp_Curve=amplitude_file, diretorio_simulacoes=diretorio_conter_simulacoes),  # A função objetivo
    pbounds=pbounds,       # O espaço de busca para mass scaling
    random_state=1,
)

# %% [markdown]
# The BayesianOptimization object will work out of the box without much tuning needed. The main method you should be aware of is maximize, which does exactly what you think it does.
# 
# There are many parameters you can pass to maximize, nonetheless, the most important ones are:
# 
# n_iter: How many steps of bayesian optimization you want to perform. The more steps the more likely to find a good maximum you are.
# init_points: How many steps of random exploration you want to perform. Random exploration can help by diversifying the exploration space.

# %%
optimizer.maximize(
    init_points=30,
    n_iter=1,
)


