import matplotlib.pyplot as plt

# Dados reais do teste
carga_pps = [3.66, 8.82, 15.07, 43.01]
tempo_ms = [13.663, 11.34, 6.637, 4.65]  # tempo total dos testes (em milissegundos)

plt.figure(figsize=(8, 5))
plt.plot(carga_pps, tempo_ms, marker='o', linestyle='-', linewidth=2)

plt.title("Desempenho sob Carga - Sistema de Roteadores")
plt.xlabel("Carga de Pacotes por Segundo (pps)")
plt.ylabel("Tempo Total de Resposta (ms)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_stress_rede.png")
plt.show()

