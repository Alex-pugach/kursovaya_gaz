from src.fluid import Fluid
from src.reservoir import Reservoir, ResProps
from src.pipe import Pipe
from src.well import Well
from src.compressor import DCS
from src.simulator import FieldSimulator

print("=== Создаём модель ===")

# Флюид
fluid = Fluid()

# Пласт
resprops = ResProps(P=100.0, V=3.1416*500**2*25, T=310.0)
reservoir = Reservoir(resprops, fluid)

# Трубы скважин
pipe1 = Pipe(L=2000, D=0.062, roughness=0.000046, fluid=fluid, vertical_depth=1800)
pipe2 = Pipe(L=2500, D=0.062, roughness=0.000046, fluid=fluid, vertical_depth=1900)
pipe3 = Pipe(L=1800, D=0.073, roughness=0.000046, fluid=fluid, vertical_depth=1600)

# Скважины
well1 = Well(fluid, k=50, h=25, re=500, rw=0.1, pipe=pipe1)
well2 = Well(fluid, k=50, h=25, re=500, rw=0.1, pipe=pipe2)
well3 = Well(fluid, k=50, h=25, re=500, rw=0.1, pipe=pipe3)

# Шлейф
shlyf = Pipe(L=5000, D=0.200, roughness=0.000046, fluid=fluid, vertical_depth=0.0)

# ДКС
dcs = DCS(CR=1.5, P_line=5.0, q_ext=500.0)

# Симулятор
sim = FieldSimulator(reservoir, [well1, well2, well3], shlyf, dcs)

print("=== Рабочая точка ===")
states = sim.solve(100.0)
for name, st in states.items():
    print(f"{name}: q={st.q_std:.0f}, dP={st.dP:.2f}")

print("\n=== Динамика на 5 дней ===")
df = sim.run(5, dt=1.0)
print(df)