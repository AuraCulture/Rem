
"""
Test script for remove-the-bg package functionality.
"""

import os
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw


sys.path.insert(0, str(Path(__file__).parent))

try:
    from remove_the_bg import remove_background
    from remove_the_bg.cli import process_folder, main as cli_main
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Make sure dependencies are vendored first")
    sys.exit(1)


def create_test_image(path, color=(255, 0, 0), size=(200, 200)):
    """Create a simple test image."""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    

    draw.rectangle([50, 50, 150, 150], fill=(0, 255, 0))
    draw.ellipse([75, 75, 125, 125], fill=(0, 0, 255))
    
    img.save(path)
    return path


def test_core_functionality():
    """Test the core background removal functionality."""
    print("🧪 Testing core functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        

        test_image = temp_path / "test.jpg"
        create_test_image(test_image)
        
        print(f"   Created test image: {test_image}")
        
        try:

            output_path = remove_background(str(test_image))
            
            if Path(output_path).exists():
                print("   [SUCCESS] Background removal succeeded")
                return True
            else:
                print("   [ERROR] Output file not created")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Error during background removal: {e}")
            return False


def test_cli_functionality():
    """Test CLI functionality."""
    print("🧪 Testing CLI functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        

        test_images = []
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            img_path = temp_path / f"test_{i}.png"
            create_test_image(img_path, color=color)
            test_images.append(img_path)
        
        print(f"   Created {len(test_images)} test images")
        
        try:

            success = process_folder(str(temp_path))
            
            if success:

                output_files = list(temp_path.glob("*_no_bg.png"))
                if len(output_files) >= len(test_images):
                    print("   [SUCCESS] CLI folder processing succeeded")
                    return True
                else:
                    print(f"   [ERROR] Expected {len(test_images)} output files, got {len(output_files)}")
                    return False
            else:
                print("   [ERROR] CLI folder processing failed")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Error during CLI testing: {e}")
            return False


def test_edge_cases():
    """Test edge cases and error handling."""
    print("🧪 Testing edge cases...")
    

    try:
        remove_background("/non/existent/file.jpg")
        print("   [ERROR] Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("   [SUCCESS] Correctly handled non-existent file")
    except Exception as e:
        print(f"   [ERROR] Unexpected error for non-existent file: {e}")
        return False
    

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"not an image")
        temp_file.flush()
        
        try:
            remove_background(temp_file.name)
            print("   [ERROR] Should have raised ValueError for unsupported format")
            return False
        except ValueError:
            print("   [SUCCESS] Correctly handled unsupported file format")
        except Exception as e:
            print(f"   [ERROR] Unexpected error for unsupported format: {e}")
            return False
        finally:
            os.unlink(temp_file.name)
    
    return True


def main():
    """Run all tests."""
    print("🚀 Remove-the-BG Package Tests")
    print("=" * 40)
    
    tests = [
        ("Core Functionality", test_core_functionality),
        ("CLI Functionality", test_cli_functionality),
        ("Edge Cases", test_edge_cases),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"[PASS] {test_name}: PASSED")
            else:
                print(f"[FAIL] {test_name}: FAILED")
        except Exception as e:
            print(f"[ERROR] {test_name}: ERROR - {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("[FAIL] Some tests failed")
        return False


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Test script for remove-the-bg package.

Usage: python test.py

This script tests:
1. Core background removal functionality
2. CLI interface
3. Edge cases and error handling

Note: Make sure dependencies are vendored before running tests.
        """)
        sys.exit(0)
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[CANCELLED] Tests cancelled by user")
        sys.exit(1)
