# 📊 Projeto: Vertex Cover em Grafos Snark

Este projeto utiliza Python e a biblioteca Google OR-Tools para modelar e resolver o problema da **Cobertura Mínima por Vértices** (Minimum Vertex Cover) em grafos do tipo Snark.

O script inclui geradores para dois tipos específicos de Snarks:
* **Flower Snark (J_n)**
* **Goldberg Snark**

O solver utiliza Programação Inteira Mista (MIP) para encontrar o menor conjunto de vértices que "cobre" todas as arestas do grafo.

---

## ⚙️ Requisitos

* Python 3.x
* Biblioteca Google OR-Tools

Para instalar a dependência necessária, execute:

```bash
pip install ortools
