import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service

#================================================================
# CAP DO 1: Bo test co ban (Moi chi dat ~35% Coverage)
#================================================================
class TestEasyLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)

#================================================================
# CAP DO 2: TestMediumLevel (4 kịch bản cho Promo Code)
#================================================================
class TestMediumLevel(unittest.TestCase):
    def test_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000.0)

    def test_promo_offline_connection_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_new_os_only_success(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000.0)

    def test_promo_new_os_only_os14_value_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

#================================================================
# CAP DO 3: TestHardLevel (3 kịch bản Mocking GPS)
#================================================================
class TestHardLevel(unittest.TestCase):
    
    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_in_range(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(len(restaurants), 2)
        self.assertIn("Nha hang Pho Ly Quoc Su", restaurants)

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_out_of_range(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(restaurants, [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError("Mat tin hieu")
        app = YummyApp()
        result = app.get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")

if __name__ == '__main__':
    unittest.main()
