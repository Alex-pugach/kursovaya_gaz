from dataclasses import dataclass
from typing import Optional

@dataclass
class NodeState:
    """Состояние одного элемента системы (скважина, шлейф, ДКС)"""
    name: str
    P_in: float
    P_out: float
    dP: float
    q_std: float
    q_res: Optional[float] = None
    v: Optional[float] = None
    rho: Optional[float] = None
    