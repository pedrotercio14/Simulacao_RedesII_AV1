import matplotlib.pyplot as plt

# Dicionário com caminhos dos arquivos
dados = {
    "Router 1": "./router/logs/tempo_atualizacao_router1.txt",
    "Router 2": "./router/logs/tempo_atualizacao_router2.txt",
    "Router 3": "./router/logs/tempo_atualizacao_router3.txt",
    "Router 4": "./router/logs/tempo_atualizacao_router4.txt",
    "Router 5": "./router/logs/tempo_atualizacao_router5.txt",
}

nomes = []
medias = []

for nome, caminho in dados.items():
    try:
        with open(caminho) as f:
            tempos = [float(l.strip()) for l in f if l.strip()]
            media = sum(tempos) / len(tempos) if tempos else 0
            nomes.append(nome)
            medias.append(media)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")

# Gerar gráfico de barras
plt.figure(figsize=(9, 6))
plt.bar(nomes, medias, color="mediumslateblue")
plt.title("Tempo Médio de Atualização da Tabela de Roteamento")
plt.ylabel("Tempo (ms)")
plt.xlabel("Roteadores")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("grafico_tempo_medio_roteadores.png")
plt.show()
