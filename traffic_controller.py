"""
Smart Traffic Light Controller - AI Rule Engine
Author: Internship Project
Description: AI-based traffic management system using rule engine + reinforcement logic
"""

import random
import time
import json
from datetime import datetime


# ─────────────────────────────────────────────
#  Traffic Lane Class
# ─────────────────────────────────────────────
class Lane:
    def __init__(self, lane_id, direction):
        self.lane_id = lane_id
        self.direction = direction       # NORTH, SOUTH, EAST, WEST
        self.vehicle_count = 0
        self.signal = "RED"
        self.wait_time = 0              # seconds lane has been waiting
        self.green_time = 0             # seconds of green assigned
        self.priority_score = 0.0

    def update_vehicle_count(self, count):
        self.vehicle_count = count

    def compute_priority(self, base_green=10, max_green=60):
        """
        AI Rule Engine: Priority Score Calculation
        Formula: (vehicle_count * density_weight) + (wait_time * wait_weight)
        Green time is dynamically allocated based on priority.
        """
        density_weight = 1.5
        wait_weight = 0.8

        self.priority_score = (self.vehicle_count * density_weight) + (self.wait_time * wait_weight)
        # Clamp green time between base and max
        self.green_time = min(max_green, max(base_green, int(self.priority_score)))
        return self.priority_score

    def to_dict(self):
        return {
            "lane_id": self.lane_id,
            "direction": self.direction,
            "vehicle_count": self.vehicle_count,
            "signal": self.signal,
            "wait_time": round(self.wait_time, 1),
            "priority_score": round(self.priority_score, 2),
            "green_time": self.green_time
        }


# ─────────────────────────────────────────────
#  Vehicle Density Sensor (Dummy / OpenCV-ready)
# ─────────────────────────────────────────────
class VehicleSensor:
    """
    Simulates camera-based vehicle counting.
    In production: replace get_count() with OpenCV YOLO detection output.
    """

    def __init__(self, mode="simulation"):
        self.mode = mode

    def get_count(self, lane_direction, cycle=0):
        if self.mode == "simulation":
            return self._simulate(lane_direction, cycle)
        elif self.mode == "manual":
            return self._manual_input(lane_direction)

    def _simulate(self, direction, cycle):
        """Simulate rush hour patterns"""
        base = {"NORTH": 20, "SOUTH": 15, "EAST": 30, "WEST": 10}
        noise = random.randint(-5, 10)
        rush_hour_bonus = 15 if cycle % 3 == 0 else 0
        return max(0, base.get(direction, 10) + noise + rush_hour_bonus)

    def _manual_input(self, direction):
        try:
            count = int(input(f"  Enter vehicle count for {direction} lane: "))
            return max(0, count)
        except ValueError:
            return random.randint(5, 30)


# ─────────────────────────────────────────────
#  AI Traffic Controller (Core Engine)
# ─────────────────────────────────────────────
class SmartTrafficController:
    def __init__(self, mode="simulation"):
        self.lanes = [
            Lane("L1", "NORTH"),
            Lane("L2", "SOUTH"),
            Lane("L3", "EAST"),
            Lane("L4", "WEST"),
        ]
        self.sensor = VehicleSensor(mode=mode)
        self.cycle_count = 0
        self.log = []
        self.total_vehicles_cleared = 0

    def scan_all_lanes(self):
        """Step 1: Read vehicle density from all lanes"""
        print("\n📷  Scanning lanes...")
        for lane in self.lanes:
            count = self.sensor.get_count(lane.direction, self.cycle_count)
            lane.update_vehicle_count(count)
            print(f"   {lane.direction:6s} → {count:3d} vehicles detected")

    def compute_priorities(self):
        """Step 2: AI Rule Engine computes priority for each lane"""
        for lane in self.lanes:
            lane.compute_priority()

    def prioritize_lanes(self):
        """Step 3: Sort lanes by priority score (Reinforcement Logic)"""
        return sorted(self.lanes, key=lambda l: l.priority_score, reverse=True)

    def run_signal_cycle(self, sorted_lanes):
        """Step 4: Simulate signal switching — highest priority gets green first"""
        print("\n🚦  Signal Cycle Starting...\n")

        for lane in self.lanes:
            lane.signal = "RED"

        for lane in sorted_lanes:
            lane.signal = "GREEN"
            vehicles_cleared = min(lane.vehicle_count, lane.green_time // 2)
            self.total_vehicles_cleared += vehicles_cleared

            print(f"   🟢 GREEN → {lane.direction:5s} | Score: {lane.priority_score:6.1f} | "
                  f"Green Time: {lane.green_time}s | Vehicles: {lane.vehicle_count} | "
                  f"Cleared: {vehicles_cleared}")

            time.sleep(0.3)  # Simulate real-time switching delay

            lane.signal = "RED"
            lane.wait_time = 0  # Reset wait after green

            # Increase wait time for other lanes
            for other in self.lanes:
                if other.lane_id != lane.lane_id:
                    other.wait_time += lane.green_time

        print(f"\n   ✅  Cycle {self.cycle_count + 1} complete. Total vehicles cleared: {self.total_vehicles_cleared}")

    def log_cycle(self, sorted_lanes):
        """Log this cycle's data for analytics"""
        entry = {
            "cycle": self.cycle_count + 1,
            "timestamp": datetime.now().isoformat(),
            "lanes": [l.to_dict() for l in sorted_lanes],
            "total_cleared": self.total_vehicles_cleared
        }
        self.log.append(entry)

    def save_log(self, filepath="traffic_log.json"):
        with open(filepath, "w") as f:
            json.dump(self.log, f, indent=2)
        print(f"\n💾  Log saved to {filepath}")

    def display_dashboard(self):
        """Terminal dashboard showing current state"""
        print("\n" + "═" * 60)
        print(f"  🏙️  SMART TRAFFIC CONTROLLER  |  Cycle #{self.cycle_count + 1}")
        print("═" * 60)
        print(f"  {'Lane':<6} {'Direction':<8} {'Vehicles':>8} {'Score':>8} {'Green(s)':>9} {'Signal':>7}")
        print("  " + "─" * 54)
        for lane in sorted(self.lanes, key=lambda l: l.priority_score, reverse=True):
            signal_icon = "🟢" if lane.signal == "GREEN" else "🔴"
            print(f"  {lane.lane_id:<6} {lane.direction:<8} {lane.vehicle_count:>8} "
                  f"{lane.priority_score:>8.1f} {lane.green_time:>9} {signal_icon:>5} {lane.signal}")
        print("═" * 60)

    def run(self, total_cycles=5):
        """Main simulation loop"""
        print("\n" + "=" * 60)
        print("  🚗  AI-BASED SMART TRAFFIC LIGHT CONTROLLER")
        print("  Mode: Simulation | Lanes: 4 | Cycles:", total_cycles)
        print("=" * 60)

        for cycle in range(total_cycles):
            self.cycle_count = cycle
            print(f"\n\n{'─'*60}")
            print(f"  🔄  CYCLE {cycle + 1} of {total_cycles}")
            print(f"{'─'*60}")

            self.scan_all_lanes()
            self.compute_priorities()
            sorted_lanes = self.prioritize_lanes()
            self.display_dashboard()
            self.run_signal_cycle(sorted_lanes)
            self.log_cycle(sorted_lanes)

            if cycle < total_cycles - 1:
                print(f"\n⏳  Next cycle in 2 seconds...")
                time.sleep(2)

        self.save_log()
        print("\n\n🎉  Simulation Complete!")
        print(f"   Total Cycles     : {total_cycles}")
        print(f"   Total Vehicles Cleared: {self.total_vehicles_cleared}")
        print(f"   Log saved        : traffic_log.json")


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\nSelect Mode:")
    print("  1. Simulation (auto dummy data)")
    print("  2. Manual Input")
    choice = input("Enter choice (1/2) [default: 1]: ").strip()

    mode = "manual" if choice == "2" else "simulation"
    cycles = input("Enter number of cycles [default: 5]: ").strip()
    cycles = int(cycles) if cycles.isdigit() else 5

    controller = SmartTrafficController(mode=mode)
    controller.run(total_cycles=cycles)
