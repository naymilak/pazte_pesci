import unittest
from pedestrian_detection_v1 import resize_coordinates

class TestResizeCoordinates(unittest.TestCase):
    
    def test_resize_coordinates(self):

        det = [[100, 100, 300, 300], [500, 500, 700, 700]]
        original_width = 1920
        original_height = 1080
        target_width = 1280
        target_height = 720
        
        resized_det = resize_coordinates(det, original_width, original_height, target_width, target_height)
        
        expected_resized_det = [[66.67, 66.67, 200, 200], [333.33, 333.33, 466.67, 466.67]]
        
        self.assertEqual(resized_det, expected_resized_det)

if __name__ == '__main__':
    unittest.main()

