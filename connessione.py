from dataclasses import dataclass
from model.prodotto import Prodotto

@dataclass
class Connessione:
    prodotto1: Prodotto
    prodotto2: Prodotto
    peso: int