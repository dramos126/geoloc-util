# geoloc-util

This command-line utility fetches geographical information (latitude, longitude, place name, etc.) using the OpenWeather Geocoding API.

## Setup

### 1. Create & Activate a Virtual Environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 3. Usage:
Run the utility from the command line by providing one or more location inputs(City/State or Zip Code).  
```bash
python geoloc_util.py "Madison, WI" "12345" "Chicago, IL" "10001"
```

### 4. Running Tests:
Execute tests with pytest while in the project directory
```bash
pytest
```