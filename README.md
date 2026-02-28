# 🚗 Vehicle Telemetry Collection System

Enterprise-grade Fleet Monitoring Control Center with real-time telemetry streaming, interactive dashboards, and comprehensive analytics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

## ✨ Features

### Backend
- 🚀 **FastAPI** - High-performance REST API
- 📡 **WebSocket Streaming** - Real-time data broadcasting
- 🗄️ **PostgreSQL** - Production database with optimized indexing
- 🔄 **Auto Status Computation** - NORMAL/WARNING/CRITICAL classification
- ✅ **Input Validation** - Pydantic schemas with comprehensive validation
- 🐳 **Docker Ready** - Complete containerization

### Dashboards
- 🎨 **3 Professional Dashboards** - From simple to enterprise-level
- 📊 **Live Charts** - Chart.js integration with real-time updates
- 🗺️ **Interactive Maps** - Leaflet.js with color-coded vehicle markers
- 🚨 **Alert System** - Toast notifications for critical events
- 🌙 **Dark Mode** - Modern glassmorphism design
- 📱 **Responsive** - Works on all screen sizes

### Data Simulators
- 🎲 **Realistic Simulator** - Generates authentic vehicle behavior
- 🏎️ **F1 Simulator** - Formula 1 telemetry data integration
- 🌐 **Real-time API** - Mockly WebSocket streaming

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Python 3.11+
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd vehicle-telemetry

# Start services
docker-compose up --build
```

### Run Simulator

```bash
# Install dependencies
pip install requests

# Start simulator (10 vehicles, 2-second interval)
python simulator.py 10 2
```

### Open Dashboard

Open any of these dashboards in your browser:
- `dashboard.html` - Simple, clean interface
- `dashboard_elite.html` - Beautiful gradient design  
- `fleet_control_center.html` - **Enterprise control center** (Recommended)

## 📊 Dashboards

### Fleet Control Center (Enterprise)
Professional Tesla-style monitoring dashboard with:
- Left sidebar with vehicle list
- WebSocket controls (Stream All/Single Vehicle)
- Fleet overview with 5 stat cards
- Status distribution pie chart
- Interactive Leaflet.js map
- Vehicle detail panel with 3 live charts
- Real-time toast notifications
- Trend arrows for metrics

### Dashboard Elite
Modern gradient design with:
- Animated background
- Glass-morphism cards
- Real-time charts
- Search functionality

### Dashboard (Basic)
Clean, simple interface for quick monitoring

## 🔌 API Endpoints

### REST API

#### POST /api/telemetry
```json
{
  "vehicleId": "VEHICLE-001",
  "speed": 80.5,
  "engineTemperature": 95.0,
  "batteryLevel": 75.0,
  "energyConsumption": 15.2,
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

**Status Rules:**
- 🔴 CRITICAL: `engineTemperature > 120` OR `batteryLevel < 10`
- 🟡 WARNING: `speed > 150`
- 🟢 NORMAL: Otherwise

#### GET /api/telemetry/{vehicle_id}/latest
Get most recent telemetry for a vehicle

#### GET /api/telemetry/{vehicle_id}?limit=10
Get recent telemetry history

### WebSocket API

#### ws://localhost:8000/api/telemetry/stream
Stream all vehicles' telemetry in real-time

#### ws://localhost:8000/api/telemetry/stream/{vehicle_id}
Stream specific vehicle's telemetry

## 📁 Project Structure

```
vehicle-telemetry/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── routes.py            # API endpoints
│   └── websocket.py         # WebSocket manager
├── dashboard.html           # Simple dashboard
├── dashboard_elite.html     # Premium dashboard
├── fleet_control_center.html # Enterprise dashboard
├── simulator.py             # Vehicle data simulator
├── f1_simulator.py          # F1 data simulator
├── realtime_stream.py       # Real-time API integration
├── test_api.py              # API test suite
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🗄️ Database Schema

**Table: telemetry**
- `id` - Primary Key
- `vehicleId` - String (indexed)
- `speed` - Float (>= 0)
- `engineTemperature` - Float
- `batteryLevel` - Float (0-100)
- `energyConsumption` - Float
- `latitude` - Float
- `longitude` - Float
- `timestamp` - DateTime (UTC)
- `status` - String (NORMAL/WARNING/CRITICAL)

**Index:** Composite index on `(vehicleId, timestamp DESC)`

## 🧪 Testing

```bash
# Run API tests
python test_api.py

# Test WebSocket
# Open test_websocket.html in browser
```

## 🛠️ Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
  - Default: `postgresql://postgres:postgres@db:5432/telemetry`

### Simulator Options
```bash
python simulator.py <num_vehicles> <interval_seconds>
# Example: python simulator.py 10 2
```

## 🐛 Troubleshooting

### Docker not running
```bash
# Start Docker Desktop first
docker-compose up
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

### Database connection failed
```bash
# Wait for health check to complete
# Check logs: docker-compose logs db
```

## 📝 License

MIT License - feel free to use this project for learning and development

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ using FastAPI, PostgreSQL, Chart.js, and Leaflet.js
