#!/usr/bin/env python3
"""
Test runner for HBnB API
Runs comprehensive unit tests and generates test reports
"""

import unittest
import sys
import os
import json
from datetime import datetime
import requests
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_server_status():
    """Check if the Flask server is running"""
    try:
        response = requests.get('http://127.0.0.1:5001/api/v1/users', timeout=2)
        return response.status_code == 200
    except:
        return False

def display_swagger_info():
    """Display information about accessing Swagger documentation"""
    print("📋 Swagger Documentation Access")
    print("=" * 50)
    print("Your Flask-RESTx API automatically generates Swagger documentation.")
    print()
    print("🌐 Access URLs:")
    print("  • Swagger UI: http://127.0.0.1:5001/api/v1/")
    print("  • JSON Spec: http://127.0.0.1:5001/api/v1/swagger.json")
    print()
    print("📝 What you'll find in Swagger:")
    print("  ✅ Complete API documentation")
    print("  ✅ Interactive endpoint testing")
    print("  ✅ Request/response schemas")
    print("  ✅ Model definitions")
    print("  ✅ Example requests and responses")
    print()
    
    if check_server_status():
        print("✅ Server is running - you can access Swagger now!")
        print("   Open: http://127.0.0.1:5001/api/v1/ in your browser")
    else:
        print("⚠️  Server not running. Start it with: python run.py")
        print("   Then access: http://127.0.0.1:5001/api/v1/")
    print()

def run_specific_test_class(test_class_name):
    """Run a specific test class"""
    print(f"🧪 Running {test_class_name} tests...")
    
    # Import the test module
    from tests.test_api_endpoints import (
        TestUserEndpoints, TestAmenityEndpoints, 
        TestPlaceEndpoints, TestReviewEndpoints, 
        TestEndpointIntegration
    )
    
    # Map class names to actual classes
    test_classes = {
        'users': TestUserEndpoints,
        'amenities': TestAmenityEndpoints,
        'places': TestPlaceEndpoints,
        'reviews': TestReviewEndpoints,
        'integration': TestEndpointIntegration
    }
    
    if test_class_name.lower() in test_classes:
        test_class = test_classes[test_class_name.lower()]
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result
    else:
        print(f"❌ Unknown test class: {test_class_name}")
        print("Available classes: users, amenities, places, reviews, integration")
        return None

def run_all_tests():
    """Run all test suites"""
    print("🧪 Running Complete Test Suite")
    print("=" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    start_time = datetime.now()
    result = runner.run(suite)
    end_time = datetime.now()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Duration: {end_time - start_time}")
    
    if result.failures:
        print(f"\n❌ Failures ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  • {test}")
    
    if result.errors:
        print(f"\n💥 Errors ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  • {test}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  Some tests failed. Check the output above for details.")
    
    return result

def run_validation_tests():
    """Run specific validation tests"""
    print("🔍 Running Validation Tests")
    print("=" * 30)
    
    # Your specific validation test case
    validation_tests = [
        {
            "name": "User Creation with Invalid Data",
            "url": "http://127.0.0.1:5001/api/v1/users/",
            "method": "POST",
            "data": {
                "first_name": "",
                "last_name": "",
                "email": "invalid-email"
            },
            "expected_status": 400
        },
        {
            "name": "Place Creation with Invalid Price",
            "url": "http://127.0.0.1:5001/api/v1/places/",
            "method": "POST", 
            "data": {
                "title": "Test Place",
                "price": -10.0,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "owner_id": "fake-id"
            },
            "expected_status": 400
        },
        {
            "name": "Review Creation with Invalid Rating",
            "url": "http://127.0.0.1:5001/api/v1/reviews/",
            "method": "POST",
            "data": {
                "text": "Test review",
                "rating": 6,
                "user_id": "fake-id",
                "place_id": "fake-id"
            },
            "expected_status": 400
        }
    ]
    
    if not check_server_status():
        print("❌ Server not running. Please start with: python run.py")
        return
    
    for i, test in enumerate(validation_tests, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        try:
            response = requests.post(
                test['url'],
                json=test['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == test['expected_status']:
                print(f"✅ PASS: Got expected status {response.status_code}")
            else:
                print(f"❌ FAIL: Expected {test['expected_status']}, got {response.status_code}")
                
            print(f"Response: {response.json()}")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")

def display_test_examples():
    """Display example curl commands for manual testing"""
    print("🛠️  Manual Testing Examples")
    print("=" * 30)
    
    examples = [
        {
            "name": "Create User (Valid)",
            "command": '''curl -X POST "http://127.0.0.1:5001/api/v1/users/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}''''
        },
        {
            "name": "Create User (Invalid - Your Test)",
            "command": '''curl -X POST "http://127.0.0.1:5001/api/v1/users/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}''''
        },
        {
            "name": "Get All Users",
            "command": '''curl -X GET "http://127.0.0.1:5001/api/v1/users/"'''
        },
        {
            "name": "Create Place",
            "command": '''curl -X POST "http://127.0.0.1:5001/api/v1/places/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Test Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "USER_ID_HERE"
}''''
        }
    ]
    
    for example in examples:
        print(f"\n📝 {example['name']}:")
        print(example['command'])
        print()

def main():
    """Main test runner function"""
    print("🚀 HBnB API Test Suite")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'swagger':
            display_swagger_info()
        elif command == 'validation':
            run_validation_tests()
        elif command == 'examples':
            display_test_examples()
        elif command in ['users', 'amenities', 'places', 'reviews', 'integration']:
            run_specific_test_class(command)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: swagger, validation, examples, users, amenities, places, reviews, integration")
    else:
        # Run everything
        display_swagger_info()
        print()
        run_all_tests()
        print()
        run_validation_tests()
        print()
        display_test_examples()

if __name__ == '__main__':
    main()
