import unittest
from calculator_logic import calculate_logic

class TestParkingCalculator(unittest.TestCase):
    def test_free_period(self):
        # 30분 정각 무료
        duration, fee = calculate_logic("09:00", "09:30")
        self.assertEqual(fee, 0)
        self.assertEqual(duration, "30분")

    def test_paid_start(self):
        # 31분 주차 -> 500원
        duration, fee = calculate_logic("09:00", "09:31")
        self.assertEqual(fee, 500)

    def test_paid_unit(self):
        # 40분 주차 -> 500원
        duration, fee = calculate_logic("09:00", "09:40")
        self.assertEqual(fee, 500)

    def test_paid_round_up(self):
        # 41분 주차 -> 1000원
        duration, fee = calculate_logic("09:00", "09:41")
        self.assertEqual(fee, 1000)

    def test_midnight_crossing(self):
        # 자정 경과 (23:00 -> 01:00, 2시간 = 120분)
        # 30분 무료 + 90분 유료 (9회 * 500 = 4500원)
        # 실제 계산: 120 - 30 = 90. 90/10 = 9회. 9 * 500 = 4500.
        duration, fee = calculate_logic("23:00", "01:00")
        self.assertEqual(fee, 4500)

    def test_max_fee(self):
        # 매우 긴 주차 (20,000원 제한 확인)
        duration, fee = calculate_logic("09:00", "23:00")
        self.assertEqual(fee, 20000)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            calculate_logic("25:00", "26:00")
        with self.assertRaises(ValueError):
            calculate_logic("abc", "10:00")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingCalculator)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    print(f"\n결과 -> 통과: {result.testsRun - len(result.failures) - len(result.errors)}, 실패: {len(result.failures) + len(result.errors)}")
    
    if not result.wasSuccessful():
        exit(1)
