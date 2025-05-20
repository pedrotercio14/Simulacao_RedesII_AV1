# README - Projeto de Simulação de Rede com Roteadores com Implementação do Algoritmo de Estado de Enlace com Docker e Python - AV1 REDES II

## Como executar o projeto

1. Certifique-se de ter instalado o Docker e Docker Compose no seu sistema.  
2. Clone o repositório do projeto para sua máquina local.  
3. Navegue até a pasta raiz do projeto no terminal.  
4. Execute o comando abaixo para construir as imagens e iniciar os containers:  
   docker-compose up --build

5. Para encerrar a simulação e remover os containers, utilize:
    docker-compose down
   
6. Os arquivos de log e os tempos de atualização das tabelas de roteamento ficarão disponíveis nos volumes montados, conforme definido no docker-compose.yml.

## Justificativa do(s) protocolo(s) escolhido(s)

O projeto utiliza o protocolo de roteamento por **Estado de Enlace (Link-State Routing)**, que oferece as seguintes vantagens:

* Envio periódico de pacotes com o estado dos enlaces de cada roteador, permitindo que todos conheçam a topologia completa da rede.
* Uso do algoritmo de Dijkstra para cálculo de rotas ótimas para todos os destinos, garantindo eficiência e rapidez na convergência.
* Adequado para redes de pequeno a médio porte, pois atualiza dinamicamente as rotas em caso de mudança na topologia.
* Implementação facilitada e desempenho consistente.

Como protocolo de transporte para os pacotes de estado de enlace, foi escolhido o **UDP (User Datagram Protocol)** devido a:

* Baixa latência e menor overhead, por ser um protocolo sem conexão e sem confirmação de entrega.
* Robustez suficiente para esse tipo de aplicação, pois a perda ocasional de pacotes é tolerada e corrigida em atualizações futuras.
* Simplicidade na implementação do roteamento sobre UDP, pois a confiabilidade é gerenciada no protocolo de roteamento.

## Como a topologia foi construída

* A topologia do projeto é composta por 5 roteadores interconectados, cada um operando em sub-redes distintas.
* Cada roteador comunica-se com seus vizinhos, configurados via variáveis de ambiente no docker-compose.yml.
* Cada roteador possui IPs estáticos para suas interfaces nas sub-redes simuladas, representando links ponto a ponto.
* Hosts estão conectados diretamente a seus roteadores, simulando as pontas finais da rede.
* A rede é simulada totalmente com containers Docker, o que permite isolamento, fácil replicação e testes controlados.
* O arquivo docker-compose.yml define o endereçamento IP, relações entre roteadores e hosts, e configura os volumes para logs.


