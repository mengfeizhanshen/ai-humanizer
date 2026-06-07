#!/usr/bin/env python3
"""
Test script for AI Humanizer API
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_intensity_levels():
    """Test intensity levels endpoint"""
    print("\n=== Testing Intensity Levels ===")
    response = requests.get(f"{BASE_URL}/intensity-levels")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_single_humanize():
    """Test single text humanization"""
    print("\n=== Testing Single Text Humanization ===")
    
    test_cases = [
        {
            "text": "The integration of artificial intelligence technology has fundamentally transformed the landscape of modern society, thereby necessitating comprehensive adaptation strategies.",
            "intensity": "light"
        },
        {
            "text": "Furthermore, the implementation of machine learning algorithms has demonstrated significant efficacy in optimizing operational efficiency.",
            "intensity": "medium"
        },
        {
            "text": "Consequently, stakeholders must leverage innovative methodologies to ameliorate the ubiquitous challenges perpetuated by technological disruption.",
            "intensity": "strong"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i} - Intensity: {test_case['intensity']}")
        response = requests.post(
            f"{BASE_URL}/humanize",
            json=test_case
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Original: {result['original']}")
        print(f"Humanized: {result['humanized']}")
        print(f"Score: {result['score']}")
        
        if response.status_code != 200:
            return False
    
    return True

def test_batch_humanize():
    """Test batch text humanization"""
    print("\n=== Testing Batch Humanization ===")
    
    payload = {
        "texts": [
            "The paradigm shift necessitates a comprehensive reevaluation of existing methodologies.",
            "Leveraging cutting-edge technology facilitates unprecedented optimization opportunities.",
            "Contemporary analysis demonstrates significant efficacy in implementing innovative frameworks."
        ],
        "intensity": "medium"
    }
    
    response = requests.post(
        f"{BASE_URL}/humanize-batch",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total texts: {result['total']}")
    print(f"Successful: {result['success_count']}")
    
    for i, item in enumerate(result['results'], 1):
        print(f"\nResult {i}:")
        print(f"  Original: {item['original']}")
        print(f"  Humanized: {item['humanized']}")
        print(f"  Score: {item['score']}")
    
    return response.status_code == 200

def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===")
    
    # Invalid intensity
    print("\n1. Testing invalid intensity...")
    response = requests.post(
        f"{BASE_URL}/humanize",
        json={
            "text": "Test text",
            "intensity": "invalid"
        }
    )
    print(f"Status: {response.status_code} (Expected: 400)")
    if response.status_code == 400:
        print(f"Error: {response.json()['detail']}")
    
    # Empty text
    print("\n2. Testing empty text...")
    response = requests.post(
        f"{BASE_URL}/humanize",
        json={
            "text": "",
            "intensity": "medium"
        }
    )
    print(f"Status: {response.status_code} (Expected: 422 or 400)")
    
    return True

def main():
    """Run all tests"""
    print("="*50)
    print("AI Humanizer API Test Suite")
    print("="*50)
    
    try:
        # Run tests
        results = {
            "Health Check": test_health(),
            "Intensity Levels": test_intensity_levels(),
            "Single Humanize": test_single_humanize(),
            "Batch Humanize": test_batch_humanize(),
            "Error Handling": test_error_handling(),
        }
        
        # Print summary
        print("\n" + "="*50)
        print("Test Summary")
        print("="*50)
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        total_passed = sum(results.values())
        print(f"\nTotal: {total_passed}/{len(results)} tests passed")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
