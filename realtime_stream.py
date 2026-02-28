"""
Real-time Vehicle Telemetry Streaming using Mockly WebSocket API
Connects to free WebSocket API and streams real vehicle data
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"
MOCKLY_WS = "wss://mockly.me/ws/map"

async def stream_realtime_data():
    """Connect to Mockly WebSocket and stream real-time vehicle data"""
    print("=" * 70)
    print("🚗 Real-Time Vehicle Telemetry Streaming")
    print("=" * 70)
    print(f"Connecting to Mockly WebSocket API...")
    print(f"Target API: {BASE_URL}")
    print("=" * 70)
    print("\nPress Ctrl+C to stop\n")
    
    try:
        async with websockets.connect(MOCKLY_WS) as websocket:
            print("✓ Connected to Mockly WebSocket!")
            print("📡 Streaming real-time vehicle data...\n")
            
            iteration = 0
            vehicle_map = {}
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type')
                    
                    if msg_type == 'fleet_info':
                        # Initial fleet information
                        vehicles = data.get('vehicles', [])
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Fleet Info Received")
                        print(f"Total vehicles: {len(vehicles)}")
                        print("-" * 70)
                        
                        for vehicle in vehicles:
                            vehicle_map[vehicle['id']] = vehicle
                            telemetry = convert_to_telemetry(vehicle)
                            send_telemetry(telemetry)
                            print(f"✓ {telemetry['vehicleId']}: "
                                  f"Speed={telemetry['speed']:.1f} km/h, "
                                  f"Battery={telemetry['batteryLevel']:.1f}%")
                    
                    elif msg_type == 'batch_update':
                        # Batch updates
                        iteration += 1
                        updates = data.get('updates', [])
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Batch Update #{iteration}")
                        print(f"Updates received: {len(updates)}")
                        print("-" * 70)
                        
                        for update in updates:
                            if update.get('type') == 'location_update':
                                vehicle_id = update.get('vehicle_id')
                                
                                # Update vehicle info
                                if vehicle_id in vehicle_map:
                                    vehicle_map[vehicle_id]['current_location'] = update.get('location', {})
                                    vehicle_map[vehicle_id]['current_status'] = update.get('status', 'unknown')
                                    vehicle_map[vehicle_id]['battery_level'] = update.get('battery', 100)
                                    
                                    telemetry = convert_to_telemetry(vehicle_map[vehicle_id])
                                    send_telemetry(telemetry)
                                    print(f"✓ {telemetry['vehicleId']}: "
                                          f"Speed={telemetry['speed']:.1f} km/h, "
                                          f"Status={update.get('status', 'unknown')}")
                    
                    elif msg_type == 'delivery_completed':
                        vehicle_id = data.get('vehicle_id')
                        print(f"\n🎉 Delivery completed by {vehicle_id}")
                    
                    elif msg_type == 'traffic_event':
                        vehicle_id = data.get('vehicle_id')
                        event = data.get('event', {})
                        print(f"\n⚠️  Traffic event for {vehicle_id}: {event.get('message', 'Unknown')}")
                    
                except json.JSONDecodeError:
                    print(f"⚠️  Invalid JSON received")
                except Exception as e:
                    print(f"⚠️  Error processing message: {e}")
                
    except websockets.exceptions.WebSocketException as e:
        print(f"\n❌ WebSocket error: {e}")
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Streaming stopped by user")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Error: {e}")

def convert_to_telemetry(vehicle):
    """Convert Mockly vehicle data to our telemetry format"""
    location = vehicle.get('current_location', {})
    status = vehicle.get('current_status', 'unknown')
    
    # Map status to speed (simulate realistic speeds)
    speed_map = {
        'loading': 0.0,
        'en-route': 60.0,
        'idle': 0.0,
        'delivering': 30.0,
        'returning': 50.0,
        'unknown': 40.0
    }
    
    base_speed = speed_map.get(status, 40.0)
    max_speed = vehicle.get('max_speed', 90)
    
    # Add some variation
    import random
    speed = min(base_speed + random.uniform(-10, 10), max_speed)
    speed = max(0, speed)
    
    # Simulate engine temperature based on speed
    engine_temp = 75 + (speed / 3) + random.uniform(-5, 5)
    
    # Get battery level
    battery = vehicle.get('battery_level', 100)
    
    # Simulate energy consumption
    energy = (speed / 10) + random.uniform(5, 15)
    
    return {
        "vehicleId": vehicle.get('id', 'unknown'),
        "speed": round(speed, 2),
        "engineTemperature": round(engine_temp, 2),
        "batteryLevel": round(battery, 2),
        "energyConsumption": round(energy, 2),
        "latitude": location.get('lat', 0.0),
        "longitude": location.get('lng', 0.0)
    }

def send_telemetry(data):
    """Send telemetry data to our API"""
    try:
        response = requests.post(f"{BASE_URL}/api/telemetry", json=data, timeout=2)
        return response.status_code == 201
    except Exception as e:
        return False

def check_api():
    """Check if our API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    # Check if API is running
    if not check_api():
        print("❌ Cannot connect to API. Make sure it's running:")
        print("   docker-compose up")
        exit(1)
    
    # Run the streaming
    asyncio.run(stream_realtime_data())
