class UnitPointCalculator:
    def __init__(self, hp_weight, mp_weight, bap_weight, ep_weight, pa_weight, sa_weight, pd_weight, sd_weight, dex_weight, roa_weight):
        self.hp_weight = hp_weight
        self.mp_weight = mp_weight
        self.bap_weight = bap_weight
        self.ep_weight = ep_weight
        self.pa_weight = pa_weight
        self.sa_weight = sa_weight
        self.pd_weight = pd_weight
        self.sd_weight = sd_weight
        self.dex_weight = dex_weight
        self.roa_weight = roa_weight

    def calculate_points(self, unit_stats):
        hp = unit_stats.get("HP", 0)
        mp = unit_stats.get("MP", 0)
        bap = unit_stats.get("BAP", 0)
        ep = unit_stats.get("EP", 0)
        pa = unit_stats.get("PA", 0)
        sa = unit_stats.get("SA", 0)
        pd = unit_stats.get("PD", 0)
        sd = unit_stats.get("SD", 0)
        dex = unit_stats.get("DEX", 0)
        roa = unit_stats.get("RoA", 0)

        points = (
            self.hp_weight * hp
            + self.mp_weight * mp * 500
            + self.bap_weight * bap
            + self.ep_weight * ep * 250
            + self.pa_weight * pa 
            + self.sa_weight * sa
            + self.pd_weight * pd
            + self.sd_weight * sd
            + self.dex_weight * dex * 12.5
            + self.roa_weight * roa * 125
        ) / 12.5 * 0.1
        return points


# Example usage
if __name__ == "__main__":
    unit_stats = {
        "HP": 1500,
        "MP": 5,
        "RoA": 3,
        "BAP": 560,
        "EP": 200,
        "PA": 200,
        "SA": 250,
        "PD": 100,
        "SD": 150,
        "DEX": 85,
    }

    calculator = UnitPointCalculator(
        hp_weight=0.75,
        mp_weight=2,
        bap_weight=1.25,
        ep_weight=1.8,
        pa_weight=1.1,
        sa_weight=1.1,
        pd_weight=0.9,
        sd_weight=0.9,
        dex_weight=1.33,
        roa_weight=1.5,
    )
    points = calculator.calculate_points(unit_stats)
    print(f"Points: {points}")