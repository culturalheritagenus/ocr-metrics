"""
Quick test script - run this to verify the package works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from jawi_metrics import cer, wer, normalize_text

print("Testing basic functionality...")

# Test 1: Perfect match
assert cer("hello", "hello") == 0.0
print("✓ CER perfect match")

# Test 2: One char different
assert cer("hello", "hallo") == 0.2
print("✓ CER with error")

# Test 3: WER
assert wer("hello world", "hello earth") == 0.5
print("✓ WER calculation")

# Test 4: Jawi text
assert cer("سلام", "سلام") == 0.0
print("✓ Jawi text support")

# Test 5: Normalization
assert normalize_text("Hello, World! 123") == "Hello World"
print("✓ Text normalization")

# Test 6: Parameters
assert cer("Test 123", "Test 456", remove_numbers=False) > 0
print("✓ Parameter handling")

print("\n✅ All tests passed! Package is ready to use.")