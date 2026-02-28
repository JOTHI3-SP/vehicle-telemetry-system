"""
Real-time Vehicle Telemetry Data Simulator
Continuously generates and streams realistic vehicle data to the API
"""
import requests
import time
import random
from datetime import datetime
import json

BASE_URL = "http://localhost:8000"

class VehicleSimulator:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.speed = random.uniform(40, 100)
        self.engine_temp = random.uniform(80, 100)
        self.battery_level = random.uniform(50, 100)
        self.energy_consumption = random.uniform(10, 20)
        self.latitude = random.uniform(37.0, 38.0)
        self.longitude = random.uniform(-123.0, -122.0)
        
    def update(self):
        """Simulate realistic vehicle behavior"""
        # Speed variations
        self.speed += random.uniform(-5, 5)
        self.speed = max(0, min(180, self.speed))
        
        # Engine temperature (increases with speed)
        target_temp = 85 + (self.speed / 10)
        self.engine_temp += (target_temp - self.engine_temp) * 0.1 + random.uniform(-2, 2)
        self.engine_temp = max(70, min(140, self.engine_temp))
        
        # Battery drain
        self.battery_level -= random.uniform(0.1, 0.5)
        if self.battery_level < 5:
            self.battery_level = random.uniform(80, 100)  # Simulate recharge
        
        # Energy consumption (related to speed)
        self.energy_consumption = 10 + (self.speed / 10) + random.uniform(-2, 2)
        self.energy_consumption = max(5, min(40, self.energy_consumption))
        
        # Location drift
        self.latitude += random.uniform(-0.001, 0.001)
        self.longitude += random.uniform(-0.001, 0.001)
        
    def get_telemetry(self):
        """Get current telemetry data"""
        return {
            "vehicleId": self.vehicle_id,
            "speed": round(self.speed, 2),
            "engineTemperature": round(self.engine_temp, 2),
            "batteryLevel": round(self.battery_level, 2),
            "energyConsumption": round(self.energy_consumption, 2),
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6)
        }
    
    def simulate_scenario(self):
        """Randomly trigger different scenarios"""
        scenario = random.random()
        
        if scenario < 0.05:  # 5% chance - Critical temperature
            self.engine_temp = random.uniform(121, 135)
            print(f"  ⚠️  {self.vehicle_id}: CRITICAL TEMPERATURE!")
            
        elif scenario < 0.10:  # 5% chance - Low battery
            self.battery_level = random.uniform(2, 9)
            print(f"  ⚠️  {self.vehicle_id}: LOW BATTERY!")
            
        elif scenario < 0.20:  # 10% chance - High speed
            self.speed = random.uniform(151, 170)
            print(f"  ⚠️  {self.vehicle_id}: HIGH SPEED WARNING!")

def send_telemetry(data):
    """Send telemetry data to API"""
    try:
        response = requests.post(f"{BASE_URL}/api/telemetry", json=data, timeout=2)
        return response.status_code == 201
    except Exception as e:
        print(f"Error sending data: {e}")
        return False

def run_simulation(num_vehicles=5, interval=2):
    """Run continuous simulation"""
    print("=" * 70)
    print("🚗 Vehicle Telemetry Real-Time Simulator")
    print("=" * 70)
    print(f"Simulating {num_vehicles} vehicles")
    print(f"Update interval: {interval} seconds")
    print(f"API endpoint: {BASE_URL}")
    print("=" * 70)
    print("\nPress Ctrl+C to stop\n")
    
    # Create vehicle simulators
    vehicles = [VehicleSimulator(f"VEHICLE-{str(i+1).zfill(3)}") for i in range(num_vehicles)]
    
    iteration = 0
    try:
        while True:
            iteration += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iteration {iteration}")
            print("-" * 70)
            
            for vehicle in vehicles:
                # Update vehicle state
                vehicle.update()
                
                # Randomly trigger scenarios
                if random.random() < 0.15:  # 15% chance per vehicle
                    vehicle.simulate_scenario()
                
                # Get and send telemetry
                telemetry = vehicle.get_telemetry()
                success = send_telemetry(telemetry)
                
                status_icon = "✓" if success else "✗"
                print(f"{status_icon} {telemetry['vehicleId']}: "
                      f"Speed={telemetry['speed']:.1f} km/h, "
                      f"Temp={telemetry['engineTemperature']:.1f}°C, "
                      f"Battery={telemetry['batteryLevel']:.1f}%")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Simulation stopped by user")
        print("=" * 70)
    except Exception as e:
        print(f"\n\nError: {e}")

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    num_vehicles = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("❌ API is not responding correctly")
            sys.exit(1)
    except:
        print("❌ Cannot connect to API. Make sure it's running:")
        print("   docker-compose up")
        sys.exit(1)
    
    run_simulation(num_vehicles, interval)
