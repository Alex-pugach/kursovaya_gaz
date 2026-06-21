import numpy as np
from scipy.optimize import fsolve
from src.state import NodeState
import pandas as pd


class FieldSimulator:
    """
    Главный класс. Собирает всю модель.
    """

    def __init__(self, reservoir, wells, shlyf, dcs):
        self.reservoir = reservoir
        self.wells = wells
        self.shlyf = shlyf
        self.dcs = dcs

    def solve(self, P_res):
        def system(x):
            q1, q2, q3, P_man = x
            q_ext = self.dcs.q_ext
            P_in_dcs = self.dcs.P_in()

            res = []
            for i, well in enumerate(self.wells):
                q = [q1, q2, q3][i]
                if well.pipe is not None:
                    state = well.pipe.dp(P_man, q)
                    P_bhp = state.P_out
                else:
                    P_bhp = P_man
                q_calc = well.q(P_res, P_bhp)
                res.append(q - q_calc)

            q_total = q1 + q2 + q3 + q_ext
            shlyf_state = self.shlyf.dp(P_in_dcs, q_total)
            res.append(P_man - shlyf_state.P_out)
            return res

        x0 = [500, 500, 500, 8.0]
        try:
            sol = fsolve(system, x0)
            q1, q2, q3, P_man = sol
        except:
            q1, q2, q3, P_man = 0, 0, 0, self.dcs.P_in()

        q1 = max(0, q1)
        q2 = max(0, q2)
        q3 = max(0, q3)

        states = {}
        for i, well in enumerate(self.wells):
            q = [q1, q2, q3][i]
            if well.pipe is not None:
                state = well.pipe.dp(P_man, q)
                P_bhp = state.P_out
            else:
                P_bhp = P_man

            states[f'well_{i+1}'] = NodeState(
                name=f'well_{i+1}',
                P_in=P_res,
                P_out=P_bhp,
                dP=P_res - P_bhp,
                q_std=q
            )

        q_total = q1 + q2 + q3 + self.dcs.q_ext
        shlyf_state = self.shlyf.dp(self.dcs.P_in(), q_total)
        states['shlyf'] = shlyf_state
        states['shlyf'].name = 'shlyf'

        states['dcs'] = NodeState(
            name='dcs',
            P_in=self.dcs.P_in(),
            P_out=self.dcs.P_line,
            dP=self.dcs.P_line - self.dcs.P_in(),
            q_std=q_total
        )

        return states

    def run(self, N_days, dt=1.0):
        P_res = self.reservoir.resprops.P
        results = []
        Gp = 0.0

        # === Запасы газа ===
        G_init = 10_000

        for day in range(N_days):
            states = self.solve(P_res)

            q1 = states['well_1'].q_std
            q2 = states['well_2'].q_std
            q3 = states['well_3'].q_std
            q_total = q1 + q2 + q3

            P_man = states['shlyf'].P_in

            dG = q_total * dt / 1_000_000
            Gp += dG
            P_res_new = P_res * (1 - Gp / G_init)
            P_res_new = max(5.0, P_res_new)

            results.append({
                't': day,
                'P_res': P_res,
                'P_man': P_man,
                'q1': q1,
                'q2': q2,
                'q3': q3,
                'q_total': q_total,
                'Gp': Gp
            })

            P_res = P_res_new

        self.reservoir.resprops.P = P_res
        return pd.DataFrame(results)