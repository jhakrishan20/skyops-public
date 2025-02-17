<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkyOps Project Structure</title>
    <style>
        body { font-family: Arial, sans-serif; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>SkyOps Project Structure</h1>
    <pre>
skyops/
│
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── utils/
│   │   │   ├── 
│   │   ├── config/
│   │       ├── 
│   │
│   ├── communication/
│   │   ├── mavlink/
│   │   │   ├── handler.py
│   │
│   ├── mission/
│   │   ├── waypoints/
│   │   │   ├── __init__.py
│   │   │   ├── planner.py
│   │   ├── simulation/
│   │       ├── __init__.py
│   │       ├── sitl.py
│   │
│   ├── telemetry/
│   │   ├── __init__.py
│   │   ├── logging/
│   │   │   ├── __init__.py
│   │   │   ├── telemetry_logger.py
│   │   ├── processing/
│   │       ├── __init__.py
│   │       ├── analyzer.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── components/
│   │   │   ├── map_renderer.py
│   │   ├── controllers/
│   │       ├── dashboard.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   ├── encryption.py
│   │
│   ├── plugins/
│   │   ├── __init__.py
│   │
│   ├── tests/
│       ├── test_core.py
│       ├── test_mavlink.py
│
├── docs/
│   ├── README.md
│
├── logs/
│   ├── .gitkeep
│
├── data/
│   ├── .gitkeep
│
├── requirements.txt
├── README.md
└── LICENSE
    </pre>
</body>
</html>
