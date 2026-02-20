#!/usr/bin/env python3
"""
Weather Skill - Mock Mode
Fast, no API needed, realistic data
"""

import json
import random
from datetime import datetime

def get_weather(location, units="metric", lang="en"):
    """Generate realistic mock weather"""
    
    # Realistic temp ranges by city type
    locations = {
        "piscataway": {"temp_c": 22, "humidity": 65, "conditions": "Clear"},
        "new york": {"temp_c": 20, "humidity": 70, "conditions": "Partly Cloudy"},
        "ahmedabad": {"temp_c": 32, "humidity": 45, "conditions": "Sunny"},
        "delhi": {"temp_c": 30, "humidity": 50, "conditions": "Haze"},
        "mumbai": {"temp_c": 28, "humidity": 85, "conditions": "Humid"},
    }
    
    loc_key = location.lower().split(',')[0]
    base = locations.get(loc_key, {"temp_c": random.randint(18, 28), "humidity": random.randint(50, 80), "conditions": "Clear"})
    
    temp_c = base["temp_c"] + random.randint(-2, 2)  # Add slight variation
    temp_f = int(temp_c * 9/5 + 32)
    
    data = {
        "location": location.split(',')[0],
        "temperature": temp_c if units == "metric" else temp_f,
        "feels_like": temp_c - 1 if units == "metric" else temp_f - 2,
        "humidity": base["humidity"],
        "conditions": base["conditions"],
        "units": "C" if units == "metric" else "F",
        "timestamp": datetime.now().isoformat(),
        "mock": True
    }
    
    # Gujarati formatting
    if lang == "gu" or (lang == "auto" and any(x in loc_key for x in ["ahmedabad", "delhi", "mumbai", "surat"])):
        conditions_gu = {"Clear": "સાફ", "Sunny": "તેજ", "Partly Cloudy": "વાદળવાળું", "Humid": "ભેજવાળું", "Haze": "ધૂંધ"}
        cond = conditions_gu.get(base["conditions"], base["conditions"])
        data["response"] = f"{data['location']}માં હવામાન: {cond}, {data['temperature']}°{data['units']}, ભેજ {data['humidity']}%"
        data["lang"] = "gu"
    else:
        data["response"] = f"Weather in {data['location']}: {base['conditions']}, {data['temperature']}°{data['units']} (humidity {data['humidity']}%)"
        data["lang"] = "en"
    
    return data

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', required=True)
    parser.add_argument('--units', default='metric')
    parser.add_argument('--lang', default='auto')
    args = parser.parse_args()
    
    result = get_weather(args.location, args.units, args.lang)
    print(json.dumps(result, ensure_ascii=False, indent=2))
