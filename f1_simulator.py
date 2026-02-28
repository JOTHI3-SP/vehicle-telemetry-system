"""
Real F1 Data Simulator using OpenF1 API
Fetches live Formula 1 telemetry and streams it to our system
"""
import requests
import time
from datetime import datetime
import sys

BASE_URL = "http://localhost:8000"
OPENF1_API = "https://api.openf1.org/v1"

def get_latest_session():
    """Get the most recent F1 session"""
    try:
        response = requests.get(f"{OPENF1_API}/sessions?session_name=Race&year=2024", timeout=5)
        sessions = response.json()
        if sessions:
            # Get the most recent session
            return sorted(sessions, key=lambda x: x['date_start'], reverse=True)[0]
        return None
    except Exception as e:
        print(f"Error fetching session: {e}")
        return None

def get_car_data(session_key):
    """Get car telemetry data from F1 session"""
    try:
        response = requests.get(
            f"{OPENF1_API}/car_data",
            params={
                "session_key": session_key,
            },
            timeout=10
        )
        return response.json()
    except Exception as e:
        print(f"Error fetching car data: {e}")
        return []

def get_location_data(session_key):
    """Get location data from F1 session"""
    try:
        response = requests.get(
            f"{OPENF1_API}/location",
            params={
                "session_key": session_key,
            },
            timeout=10
        )
        return response.json()
    except Exception as e:
        print(f"Error fetching location: {e}")
        return []

def convert_f1_to_telemetry(car_data, location_data):
    """Convert F1 data to our telemetry format"""
    # Merge car data with location
    telemetry_data = []
    
    # Create a map of location data by driver and timestamp
    location_map = {}
    for loc in location_data:
        key = f"{loc.get('driver_number', 0)}"
        if key not in location_map:
            location_map[key] = loc
    
    for car in car_data:
        driver_num = car.get('driver_number', 0)
        location = location_map.get(str(driver_num), {})
        
        # Convert F1 data to our format
        telemetry = {
            "vehicleId": f"F1-CAR-{driver_num}",
            "speed": float(car.get('speed', 0) or 0),
            "engineTemperature": 85.0 + (float(car.get('rpm', 0) or 0) / 200),  # Simulate temp from RPM
            "batteryLevel": 100.0 - (float(car.get('drs', 0) or 0) * 10),  # Simulate battery
            "energyConsumption": float(car.get('throttle', 0) or 0) / 5,  # From throttle %
            "latitude": float(location.get('y', 0) or 0) / 1000,  # Scale down
            "longitude": float(location.get('x', 0) or 0) / 1000,  # Scale down
        }
        
        # Only add if we have valid speed data
        if telemetry["speed"] > 0:
            telemetry_data.append(telemetry)
    
    return telemetry_data

def send_telemetry(data):
    """Send telemetry data to our API"""
    try:
        response = requests.post(f"{BASE_URL}/api/telemetry", json=data, timeout=2)
        return response.status_code == 201
    except Exception as e:
        return False

def run_f1_simulation():
    """Stream real F1 data"""
    print("=" * 70)
    print("🏎️  Formula 1 Real-Time Data Simulator")
    print("=" * 70)
    print("Fetching live F1 telemetry from OpenF1 API...")
    print("=" * 70)
    
    # Get latest session
    print("\n🔍 Finding latest F1 session...")
    session = get_latest_session()
    
    if not session:
        print("❌ No recent F1 session found")
        print("\n💡 Falling back to simulated F1-style data...")
        run_simulated_f1_data()
        return
    
    session_key = session['session_key']
    session_name = session.get('session_name', 'Unknown')
    location = session.get('location', 'Unknown')
    
    print(f"✓ Found session: {session_name} at {location}")
    print(f"  Session Key: {session_key}")
    print(f"\n📡 Streaming F1 telemetry data...\n")
    
    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iteration {iteration}")
            print("-" * 70)
            
            # Fetch F1 data
            car_data = get_car_data(session_key)
            location_data = get_location_data(session_key)
            
            if not car_data:
                print("⚠️  No car data available, retrying...")
                time.sleep(5)
                continue
            
            # Convert and send
            telemetry_list = convert_f1_to_telemetry(car_data[:10], location_data[:10])
            
            sent_count = 0
            for telemetry in telemetry_list:
                if send_telemetry(telemetry):
                    sent_count += 1
                    print(f"✓ {telemetry['vehicleId']}: "
                          f"Speed={telemetry['speed']:.1f} km/h, "
                          f"Temp={telemetry['engineTemperature']:.1f}°C")
            
            print(f"\n📊 Sent {sent_count}/{len(telemetry_list)} telemetry records")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Simulation stopped by user")
        print("=" * 70)

def run_simulated_f1_data():
    """Fallback: Generate F1-style simulated data"""
    import random
    
    print("\n🏎️  Generating simulated F1-style telemetry...")
    print("Press Ctrl+C to stop\n")
    
    drivers = [
        ("F1-VER-1", "Max Verstappen"),
        ("F1-PER-11", "Sergio Perez"),
        ("F1-HAM-44", "Lewis Hamilton"),
        ("F1-RUS-63", "George Russell"),
        ("F1-LEC-16", "Charles Leclerc"),
        ("F1-SAI-55", "Carlos Sainz"),
        ("F1-NOR-4", "Lando Norris"),
        ("F1-PIA-81", "Oscar Piastri"),
    ]
    
    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Lap {iteration}")
            print("-" * 70)
            
            for vehicle_id, driver_name in drivers:
                telemetry = {
                    "vehicleId": vehicle_id,
                    "speed": random.uniform(200, 340),  # F1 speeds
                    "engineTemperature": random.uniform(90, 125),
                    "batteryLevel": random.uniform(60, 100),
                    "energyConsumption": random.uniform(15, 35),
                    "latitude": random.uniform(25.0, 26.0),
                    "longitude": random.uniform(55.0, 56.0),
                }
                
                success = send_telemetry(telemetry)
                status = "✓" if success else "✗"
                print(f"{status} {driver_name} ({vehicle_id}): "
                      f"Speed={telemetry['speed']:.1f} km/h, "
                      f"Temp={telemetry['engineTemperature']:.1f}°C")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Simulation stopped")
        print("=" * 70)

if __name__ == "__main__":
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
    
    run_f1_simulation()
