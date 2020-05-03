import unittest

import tests.calculation as calculation

release_name = 'production'


class CalTest(unittest.TestCase):
    # 実行前の処理
    def setUp(self):
        print('setup')
        self.cal = calculation.Cal()

    # 実行後のお片付け処理
    def tearDown(self):
        print('clean up')
        del self.cal

    def test_add_num_and_double(self):
        self.assertEqual(self.cal.add_num_and_double(1, 1), 4)
        # assertはIsとかInとかIsInstanceとか様々なものがあるみたい

    # 例外処理はwith構文を使う
    def test_add_num_and_double_raise(self):
        with self.assertRaises(ValueError):
            self.cal.add_num_and_double('1', '1')

    # skipは下記のようにアノテーションでいけちゃう
    # @unittest.skip('skip!')
    @unittest.skipIf(release_name == 'production', 'skip!!')
    def test_add_num_and_double_skip(self):
        self.assertEqual(self.cal.add_num_and_double(1, 1), 4)


# pythonコマンドで実行する場合は下記とかで実行できる
if __name__ == '__main__':
    unittest.main()


