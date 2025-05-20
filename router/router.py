import threading
import socket
import time
import os

from link_state_packet import LinkStatePacket
from dijkstra import Dijkstra

class Router:
    def __init__(self, router_id, port, neighbors):
        self.router_id = router_id
        self.port = port
        self.neighbors = neighbors  # {vizinho: (ip, porta, custo)}
        self.lsdb = {self.router_id: {n: {"ip": ip,"custo":custo} for n, (ip, _, custo) in neighbors.items()}}
        self.routing_table = {}

    def send_link_state_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            packet = LinkStatePacket(self.router_id, {n: {"ip": ip, "custo": custo} for n, (ip, _, custo) in self.neighbors.items()}, sequence_number=int(time.time()))
            data = packet.serialize()
            for neighbor, (ip, port, _) in self.neighbors.items():
                sock.sendto(data, (ip, port))
                print(f"[{self.router_id}] Enviado estado de enlace para {neighbor} ({ip}:{port})")
            time.sleep(1)

    def receive_link_state_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))
        print(f"[{self.router_id}] Aguardando pacotes na porta {self.port}...")
        while True:
            data, _ = sock.recvfrom(4096)
            packet = LinkStatePacket.deserialize(data)
            print(f"[{self.router_id}] Recebido pacote de {packet.router_id}: {packet.neighbors}")

            # Atualiza a LSDB com o pacote recebido
            if packet.router_id not in self.lsdb or packet.sequence_number > self.lsdb[packet.router_id].get("sequence_number", 0):
                self.lsdb[packet.router_id] = packet.neighbors
                self.lsdb[packet.router_id]["sequence_number"] = packet.sequence_number
                self.update_routing_table()

                # Reencaminha o pacote para os vizinhos
                for neighbor, (ip, port, _) in self.neighbors.items():
                    if neighbor != packet.router_id:
                        sock.sendto(data, (ip, port))
                        print(f"[{self.router_id}] Reencaminhado pacote para {neighbor} ({ip}:{port})")

    def update_routing_table(self):
        inicio = time.time()

        graph = self.build_graph()
        print(f"[{self.router_id}] Grafo atualizado: {graph}")
        self.routing_table = Dijkstra(graph, self.router_id)

        fim = time.time()
        tempo_ms = (fim - inicio) * 1000
        print(f"[{self.router_id}] Tempo de atualização da tabela: {tempo_ms:.2f} ms")

        # Salvar tempo para análise posterior
        with open(f"/logs/tempo_atualizacao_{self.router_id}.txt", "a") as f:
            f.write(f"{tempo_ms:.2f}\n")

        host_to_ip = {}
        for _, neighbors in self.lsdb.items():
            for neighbor, info in neighbors.items():
                if isinstance(info, dict) and "ip" in info:
                    host_to_ip[neighbor] = info["ip"]

        for destination, path in self.routing_table.items():
            if not path:
                continue
            if destination == self.router_id or destination in self.neighbors:
                continue

            next_hop = path[0]
            dest_ip = host_to_ip.get(destination, destination)
            dest_ip_str = str(dest_ip)
            if '.' in dest_ip_str and all(part.isdigit() and 0 <= int(part) <= 255 for part in dest_ip_str.split('.')):
                ip_parts = dest_ip_str.split('.')
                gateway = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            else:
                continue

            ip_next_hop = host_to_ip.get(next_hop, next_hop)
            if not ('.' in ip_next_hop and all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_next_hop.split('.'))):
                continue

            cmd = f"ip route replace {gateway} via {ip_next_hop}"
            print(f"[{self.router_id}] Executando: {cmd}")
            os.system(cmd)

        output = []
        output.append(f"\n[{self.router_id}] Tabela de Roteamento Atualizada:")
        output.append(f"{'Destino':<10} | {'Caminho'}")
        output.append(f"{'-'*10}-+-{'-'*30}")

        for destination, path in self.routing_table.items():
            full_path = ' -> '.join([str(self.router_id)] + [str(node) for node in path]) if path else str(self.router_id)
            output.append(f"{destination:<10} | {full_path}")

        print("\n".join(output))
        with open(f"routing_table_{self.router_id}.txt", "w") as f:
            f.write("\n".join(output))

    def build_graph(self):
        graph = {}
        for node, neighbors in self.lsdb.items():
            graph[node] = {}
            for neighbor, info in neighbors.items():
                cost = info["custo"] if isinstance(info, dict) and "custo" in info else info
                graph[node][neighbor] = cost

        all_nodes = set(graph.keys())
        for neighbors in graph.values():
            all_nodes.update(neighbors.keys())
        for node in all_nodes:
            if node not in graph:
                graph[node] = {}
            else:
                graph[node] = {k: v for k, v in graph[node].items() if v is not None}
        return graph

def parse_neighbors(neighbor_string):
    neighbors = {}
    if neighbor_string:
        for entry in neighbor_string.split(','):
            parts = entry.strip().split(':')
            if len(parts) == 4:
                name, ip, port, cost = parts
                neighbors[name] = (ip, int(port), int(cost))
    return neighbors

if __name__ == "__main__":
    router_id = os.getenv("ROUTER_ID")
    port = int(os.getenv("ROUTER_PORT", 5000))
    neighbors = parse_neighbors(os.getenv("NEIGHBORS", ""))

    print(f"[{router_id}] Inicializando o roteador na porta {port} com vizinhos: {neighbors}")

    router = Router(router_id, port, neighbors)

    threading.Thread(target=router.send_link_state_packet, daemon=True).start()
    threading.Thread(target=router.receive_link_state_packet, daemon=True).start()
    threading.Thread(target=router.update_routing_table, daemon=True).start()

    while True:
        time.sleep(1)
