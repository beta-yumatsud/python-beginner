import unittest
from unittest.mock import MagicMock
from unittest import mock

import tests.salary as salary


class TestSalary(unittest.TestCase):
    # mockをMagicMockを使ってかける
    def test_calculation_salary(self):
        s = salary.Salary(year=2017)
        s.bonus_api.bonus_price = MagicMock(return_value=1)
        self.assertEqual(s.calculation_salary(), 101)
        # メソッドが呼ばれているかどうかなどは下記のようにかける
        s.bonus_api.bonus_price.assert_called()
        s.bonus_api.bonus_price.assert_called_once()
        s.bonus_api.bonus_price.assert_called_with(year=2017)
        s.bonus_api.bonus_price.assert_called_once_with(year=2017)
        self.assertEqual(s.bonus_api.bonus_price.call_count, 1)

    def test_calculation_salary_no_salary(self):
        s = salary.Salary(year=2050)
        s.bonus_api.bonus_price = MagicMock(return_value=0)
        self.assertEqual(s.calculation_salary(), 100)
        s.bonus_api.bonus_price.assert_not_called()

    @mock.patch('tests.salary.ThirdPartyBonusRestApi.bonus_price')
    def test_calculation_salary_patch(self, mock_bonus):
        mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()

    # patchをwith構文でかける
    def test_calculation_salary_patch_with(self):
        with mock.patch('tests.salary.ThirdPartyBonusRestApi.bonus_price') as mock_bonus:
            mock_bonus.return_value = 1

            s = salary.Salary(year=2017)
            salary_price = s.calculation_salary()

            self.assertEqual(salary_price, 101)
            mock_bonus.assert_called()

    # patcherをsetupとかteardownとかで設定して、それを使うでもあり
    def test_calculation_salary_patch_patcher(self):
        patcher = mock.patch('tests.salary.ThirdPartyBonusRestApi.bonus_price')
        mock_bonus = patcher.start()
        mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()
        patcher.stop()

    # side effectは独自の関数を定義する
    # 関数以外にもリストや例外処理もかける
    def test_calculation_salary_patch_side_effect(self):
        def f(year):
            return 1
        patcher = mock.patch('tests.salary.ThirdPartyBonusRestApi.bonus_price')
        mock_bonus = patcher.start()
        mock_bonus.side_effect = f
        mock_bonus.side_effect = lambda year: 1
        # mock_bonus.side_effect = ConnectionRefusedError
        # mock_bonus.side_effect = [
        #     1,
        #     2,
        #     3,
        #     ValueError('Bankrupt!!')
        # ]

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()
        patcher.stop()

    # クラスごとmock化するイメージ
    # デコレータは複数可能、その際は引数はdefに近い方の順で指定される
    @mock.patch('tests.salary.ThirdPartyBonusRestApi', spec=True)
    def test_calculation_salary_class(self, MockRest):
        mock_rest = MockRest.return_value
        mock_rest.bonus_price.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_rest.bonus_price.assert_called()

