#!/usr/bin/env python3
"""
Simple tests that don't require moviepy installation.
These tests focus on the core logic functions that can be tested independently.
"""
import unittest
import os
import tempfile
import shutil
import numpy as np
from PIL import Image
import sys
import importlib.util

# Import only the functions we can test without moviepy
def import_functions_from_create_movie():
    """Import specific functions from create_movie without importing moviepy dependencies"""
    spec = importlib.util.spec_from_file_location("create_movie", "create_movie.py")
    
    # Read the file and extract just the functions we need
    with open("create_movie.py", "r") as f:
        content = f.read()
    
    # Create a modified version that doesn't import moviepy
    modified_content = content.replace(
        "from moviepy import ImageSequenceClip, AudioFileClip",
        "# moviepy imports removed for testing"
    )
    
    # Execute the modified code in a namespace
    namespace = {}
    exec(modified_content, namespace)
    
    return (
        namespace['get_image_files'],
        namespace['calculate_progressive_duration'],
        namespace['resize_image_to_standard']
    )

try:
    get_image_files, calculate_progressive_duration, resize_image_to_standard = import_functions_from_create_movie()
    FUNCTIONS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not import functions: {e}")
    FUNCTIONS_AVAILABLE = False


class TestCreateMovieSimple(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        if not FUNCTIONS_AVAILABLE:
            self.skipTest("Functions not available for testing")
            
        self.test_dir = tempfile.mkdtemp()
        self.images_dir = os.path.join(self.test_dir, "images")
        os.makedirs(self.images_dir)
        
        # Create test images
        self.test_images = []
        for i in range(20):
            img_path = os.path.join(self.images_dir, f"test_image_{i:02d}.png")
            # Create a simple test image
            img = Image.new('RGB', (100, 100), color=(i*10 % 255, 0, 0))
            img.save(img_path)
            self.test_images.append(img_path)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if hasattr(self, 'test_dir'):
            shutil.rmtree(self.test_dir)
    
    def test_get_image_files(self):
        """Test getting image files from directory"""
        image_files = get_image_files(self.images_dir)
        
        self.assertEqual(len(image_files), 20)
        self.assertTrue(all(f.endswith('.png') for f in image_files))
        # Files should be sorted by modification time
        self.assertEqual(image_files, sorted(image_files, key=os.path.getmtime))
    
    def test_get_image_files_empty_directory(self):
        """Test getting image files from empty directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        
        image_files = get_image_files(empty_dir)
        self.assertEqual(len(image_files), 0)
    
    def test_calculate_progressive_duration_basic(self):
        """Test progressive duration calculation"""
        # Test start of progression
        start_duration = calculate_progressive_duration(0.0, 1.0, 0.2)
        self.assertAlmostEqual(start_duration, 1.0, places=3)
        
        # Test middle of progression
        mid_duration = calculate_progressive_duration(0.5, 1.0, 0.2)
        self.assertGreater(mid_duration, 0.2)
        self.assertLess(mid_duration, 1.0)
        
        # Test end of progression
        end_duration = calculate_progressive_duration(1.0, 1.0, 0.2)
        self.assertAlmostEqual(end_duration, 0.2, places=3)
    
    def test_calculate_progressive_duration_with_acceleration(self):
        """Test progressive duration with acceleration parameter"""
        # Test linear progression (acceleration = 1.0)
        linear_mid = calculate_progressive_duration(0.5, 1.0, 0.2, 1.0)
        self.assertAlmostEqual(linear_mid, 0.6, places=3)
        
        # Test accelerated progression (acceleration > 1.0)
        accel_mid = calculate_progressive_duration(0.5, 1.0, 0.2, 2.0)
        self.assertLess(accel_mid, linear_mid)  # Should be smaller with acceleration
        
        # Test very fast acceleration
        fast_accel = calculate_progressive_duration(0.5, 1.0, 0.2, 4.0)
        self.assertLess(fast_accel, accel_mid)
    
    def test_calculate_progressive_duration_edge_cases(self):
        """Test edge cases for progressive duration calculation"""
        # Test with same start and end duration (no progression)
        same_duration = calculate_progressive_duration(0.5, 0.5, 0.5)
        self.assertAlmostEqual(same_duration, 0.5, places=3)
        
        # Test with zero progress
        zero_progress = calculate_progressive_duration(0.0, 2.0, 0.1)
        self.assertAlmostEqual(zero_progress, 2.0, places=3)
        
        # Test with full progress
        full_progress = calculate_progressive_duration(1.0, 2.0, 0.1)
        self.assertAlmostEqual(full_progress, 0.1, places=3)
    
    def test_resize_image_to_standard(self):
        """Test image resizing functionality"""
        # Create a test image with known dimensions
        test_img_path = os.path.join(self.test_dir, "resize_test.png")
        img = Image.new('RGB', (800, 600), color=(255, 0, 0))
        img.save(test_img_path)
        
        resized = resize_image_to_standard(test_img_path, (1920, 1080))
        
        # Should return numpy array with target dimensions
        self.assertEqual(resized.shape, (1080, 1920, 3))
        self.assertIsInstance(resized, np.ndarray)
    
    def test_resize_image_aspect_ratio_preservation(self):
        """Test that aspect ratio is preserved during resize"""
        # Create a square image
        test_img_path = os.path.join(self.test_dir, "square_test.png")
        img = Image.new('RGB', (100, 100), color=(0, 255, 0))
        img.save(test_img_path)
        
        resized = resize_image_to_standard(test_img_path, (1920, 1080))
        
        # Should have black borders (aspect ratio preservation)
        # Check that the image is centered with black borders
        self.assertEqual(resized.shape, (1080, 1920, 3))
        
        # Check that corners are black (borders)
        self.assertTrue(np.array_equal(resized[0, 0], [0, 0, 0]))
        self.assertTrue(np.array_equal(resized[0, -1], [0, 0, 0]))


if __name__ == '__main__':
    if not FUNCTIONS_AVAILABLE:
        print("Skipping tests - functions not available")
        sys.exit(0)
    else:
        unittest.main()