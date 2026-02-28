"""
Test script for Vehicle Telemetry API
Run this after starting docker-compose up
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_create_telemetry_normal():
    print("\n=== Testing POST /api/telemetry (NORMAL status) ===")
    data = {
        "vehicleId": "VEHICLE-001",
        "speed": 80.5,
        "engineTemperature": 95.0,
        "batteryLevel": 75.0,
        "energyConsumption": 15.2,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 201
    assert result["status"] == "NORMAL"
    assert result["vehicleId"] == "VEHICLE-001"
    assert "timestamp" in result
    print("✓ Normal telemetry created")
    return result

def test_create_telemetry_warning():
    print("\n=== Testing POST /api/telemetry (WARNING status) ===")
    data = {
        "vehicleId": "VEHICLE-002",
        "speed": 160.0,  # > 150
        "engineTemperature": 100.0,
        "batteryLevel": 50.0,
        "energyConsumption": 25.5,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 201
    assert result["status"] == "WARNING"
    print("✓ Warning telemetry created")

def test_create_telemetry_critical_temp():
    print("\n=== Testing POST /api/telemetry (CRITICAL - High Temp) ===")
    data = {
        "vehicleId": "VEHICLE-003",
        "speed": 70.0,
        "engineTemperature": 125.0,  # > 120
        "batteryLevel": 60.0,
        "energyConsumption": 18.0,
        "latitude": 34.0522,
        "longitude": -118.2437
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 201
    assert result["status"] == "CRITICAL"
    print("✓ Critical (temp) telemetry created")

def test_create_telemetry_critical_battery():
    print("\n=== Testing POST /api/telemetry (CRITICAL - Low Battery) ===")
    data = {
        "vehicleId": "VEHICLE-004",
        "speed": 50.0,
        "engineTemperature": 90.0,
        "batteryLevel": 5.0,  # < 10
        "energyConsumption": 20.0,
        "latitude": 41.8781,
        "longitude": -87.6298
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 201
    assert result["status"] == "CRITICAL"
    print("✓ Critical (battery) telemetry created")

def test_validation_negative_speed():
    print("\n=== Testing Validation (Negative Speed) ===")
    data = {
        "vehicleId": "VEHICLE-005",
        "speed": -10.0,  # Invalid
        "engineTemperature": 90.0,
        "batteryLevel": 50.0,
        "energyConsumption": 15.0,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 422
    print("✓ Validation rejected negative speed")

def test_validation_battery_out_of_range():
    print("\n=== Testing Validation (Battery > 100) ===")
    data = {
        "vehicleId": "VEHICLE-006",
        "speed": 60.0,
        "engineTemperature": 90.0,
        "batteryLevel": 150.0,  # Invalid
        "energyConsumption": 15.0,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    response = requests.post(f"{BASE_URL}/api/telemetry", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 422
    print("✓ Validation rejected battery > 100")

def test_get_latest():
    print("\n=== Testing GET /api/telemetry/{vehicle_id}/latest ===")
    # Create multiple records for same vehicle
    for i in range(3):
        data = {
            "vehicleId": "VEHICLE-LATEST",
            "speed": 60.0 + i * 10,
            "engineTemperature": 90.0,
            "batteryLevel": 70.0,
            "energyConsumption": 15.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        requests.post(f"{BASE_URL}/api/telemetry", json=data)
    
    response = requests.get(f"{BASE_URL}/api/telemetry/VEHICLE-LATEST/latest")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    assert result["speed"] == 80.0  # Last one
    print("✓ Latest telemetry retrieved")

def test_get_history():
    print("\n=== Testing GET /api/telemetry/{vehicle_id}?limit=5 ===")
    response = requests.get(f"{BASE_URL}/api/telemetry/VEHICLE-LATEST?limit=5")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: Found {len(result)} records")
    for record in result:
        print(f"  - Speed: {record['speed']}, Timestamp: {record['timestamp']}")
    assert response.status_code == 200
    assert len(result) <= 5
    print("✓ History retrieved with limit")

def test_get_latest_not_found():
    print("\n=== Testing GET /api/telemetry/{vehicle_id}/latest (Not Found) ===")
    response = requests.get(f"{BASE_URL}/api/telemetry/NONEXISTENT/latest")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 404
    print("✓ 404 returned for non-existent vehicle")

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("Vehicle Telemetry API Test Suite")
        print("=" * 60)
        
        test_health()
        test_create_telemetry_normal()
        test_create_telemetry_warning()
        test_create_telemetry_critical_temp()
        test_create_telemetry_critical_battery()
        test_validation_negative_speed()
        test_validation_battery_out_of_range()
        test_get_latest()
        test_get_history()
        test_get_latest_not_found()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the API is running: docker-compose up")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
