#!/usr/bin/env python3
"""
MYTHIQ.AI Plugin Loading Test Script
Tests if all plugin imports work correctly before deployment
"""

import sys
import os

def test_plugin_imports():
    """Test if all plugin imports work correctly"""
    print("🧪 MYTHIQ.AI Plugin Import Test")
    print("=" * 50)
    
    # Test 1: Check if branches directory exists
    print("\n📁 Test 1: Directory Structure")
    if os.path.exists("branches"):
        print("✅ branches/ directory exists")
    else:
        print("❌ branches/ directory missing")
        return False
    
    # Test 2: Check for __init__.py files
    print("\n📄 Test 2: Package Files")
    required_init_files = [
        "branches/__init__.py",
        "branches/visual_creator/__init__.py",
        "branches/video_generator/__init__.py",
        "branches/knowledge/__init__.py"
    ]
    
    for init_file in required_init_files:
        if os.path.exists(init_file):
            print(f"✅ {init_file} exists")
        else:
            print(f"❌ {init_file} missing")
            return False
    
    # Test 3: Check for controller files
    print("\n🎮 Test 3: Controller Files")
    required_controllers = [
        "branches/visual_creator/controller.py",
        "branches/video_generator/controller.py",
        "branches/knowledge/controller.py"
    ]
    
    for controller in required_controllers:
        if os.path.exists(controller):
            print(f"✅ {controller} exists")
        else:
            print(f"❌ {controller} missing")
            return False
    
    # Test 4: Test imports
    print("\n🔌 Test 4: Import Testing")
    
    # Test visual_creator import
    try:
        from branches.visual_creator.controller import visual_api
        print("✅ Visual Creator import successful")
    except ImportError as e:
        print(f"❌ Visual Creator import failed: {e}")
        return False
    
    # Test video_generator import
    try:
        from branches.video_generator.controller import video_api
        print("✅ Video Generator import successful")
    except ImportError as e:
        print(f"❌ Video Generator import failed: {e}")
        return False
    
    # Test knowledge import
    try:
        from branches.knowledge.controller import knowledge_api
        print("✅ Knowledge import successful")
    except ImportError as e:
        print(f"❌ Knowledge import failed: {e}")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("🚀 Plugin loading should work correctly!")
    return True

def test_blueprint_attributes():
    """Test if imported objects are Flask Blueprints"""
    print("\n🔍 Test 5: Blueprint Validation")
    
    try:
        from branches.visual_creator.controller import visual_api
        from branches.video_generator.controller import video_api
        from branches.knowledge.controller import knowledge_api
        from flask import Blueprint
        
        blueprints = [
            ("visual_api", visual_api),
            ("video_api", video_api),
            ("knowledge_api", knowledge_api)
        ]
        
        for name, obj in blueprints:
            if isinstance(obj, Blueprint):
                print(f"✅ {name} is a valid Flask Blueprint")
            else:
                print(f"❌ {name} is not a Flask Blueprint (type: {type(obj)})")
                return False
        
        print("✅ All imports are valid Flask Blueprints!")
        return True
        
    except Exception as e:
        print(f"❌ Blueprint validation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔥 Starting MYTHIQ.AI Plugin Test Suite...")
    
    # Run basic import tests
    if test_plugin_imports():
        # Run blueprint validation
        if test_blueprint_attributes():
            print("\n🏆 COMPLETE SUCCESS!")
            print("🚀 Your plugins are ready for deployment!")
            print("📈 Expected result: 3+ plugins loaded")
            sys.exit(0)
    
    print("\n💥 TESTS FAILED!")
    print("🔧 Fix the issues above before deployment")
    print("📋 Check the plugin files and directory structure")
    sys.exit(1)

