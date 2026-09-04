import json
import sys

def format_dict_counts(d: dict) -> str:
    if not d:
        return "none"
    parts = [f"{k}:{v}" for k, v in sorted(d.items()) if v > 0]
    return ", ".join(parts) if parts else "none"

def main():
    metrics = json.load(open("docs/model_specs/antigravity/e17/artifacts/discovery/E17_TOP3_REPLAY_METRICS.json", encoding="utf-8"))
    quad_data = json.load(open("docs/model_specs/antigravity/e17/artifacts/discovery/quadrant_terminal_breakdown.json", encoding="utf-8"))

    # Index quad_data by episode_id
    quad_by_ep = {ep["episode_id"]: ep for ep in quad_data}

    print("="*105)
    print("E17 BENCHMARK REPLAY SUMMARY - TEMPORAL UNLOCKS & TERMINAL QUADRANT TILE BREAKDOWN")
    print("="*105)

    for ep in metrics["episodes"]:
        ep_id = ep["episode_id"]
        seed = ep["seed"]
        winner = ep["winner"]
        margin = ep["margin"]
        p0 = ep["players"]["player_0"]
        p1 = ep["players"]["player_1"]
        ep_quad = quad_by_ep.get(ep_id, {})

        print("\n" + "#"*105)
        print(f"EPISODE {ep_id} | Seed: {seed} | Winner: {winner} (Margin: +${margin:,.0f})")
        print("#"*105)

        for p_idx, (p_key, pdata) in enumerate([("player_0", p0), ("player_1", p1)]):
            ag = pdata["agent_name"]
            rew = pdata["final_reward"]
            hires = pdata["total_hires_count"]
            hands = pdata["peak_hands"]
            act = pdata["total_actions"]
            care = pdata["care_stats"]
            esc = pdata["animal_escapes_detected"]
            eg = pdata["endgame_liquidation"]

            p_quad = ep_quad.get("players", [])[p_idx] if ep_quad else {}
            q1_day = p_quad.get("q1_unlock_day")
            q1_step = p_quad.get("q1_unlock_step")
            q2_day = p_quad.get("q2_unlock_day")
            q2_step = p_quad.get("q2_unlock_step")

            print(f"\n  [P{p_idx}] {ag} - Final Money: ${rew:,.0f} | Status: {pdata['terminal_status']}")
            print(f"  |-- Temporal Unlocks: Q1 Unlock = Day {q1_day} (Step {q1_step}) | Q2 Unlock = Day {q2_day} (Step {q2_step}) | Q3 = Locked")
            print(f"  |-- Workforce & Efficiency: Hires={hires}, Peak Hands={hands}, Prod={act['productive']}, Move={act['moves']}, Move/Prod={act['move_to_productive_ratio']}, Escapes={esc}")
            print(f"  |-- Liquidation: Endgame Sells (D27-29)={pdata['endgame_liquidation']['sells_days_27_29']}, Unsold Inv Value=${eg['estimated_unsold_inventory_value']:,.2f}")
            print(f"  +-- Terminal Quadrant Breakdown (25 tiles per quadrant):")

            quadrants = p_quad.get("quadrants", {})
            for q_name in ["Q0_NW", "Q1_NE", "Q2_SW"]:
                qd = quadrants.get(q_name, {})
                uncultivated = qd.get("empty_uncultivated", 0) + qd.get("weeds", 0)
                empty_tiles = qd.get("empty_uncultivated", 0)
                weeds = qd.get("weeds", 0)
                crops_str = format_dict_counts(qd.get("crops", {}))
                animals_str = format_dict_counts(qd.get("animals", {}))
                empty_struct_str = format_dict_counts(qd.get("empty_structures", {}))

                line = (f"     [{q_name}] Non coltivate: {uncultivated:2d} (Libere: {empty_tiles:2d}, Weeds: {weeds:2d}) | "
                        f"Colture ({qd.get('total_crops', 0):2d}): [{crops_str}] | "
                        f"Animali ({qd.get('total_animals', 0):2d}): [{animals_str}]")
                if qd.get("total_empty_structures", 0) > 0:
                    line += f" | Strutture vuote: [{empty_struct_str}]"
                print(line)

if __name__ == "__main__":
    main()
