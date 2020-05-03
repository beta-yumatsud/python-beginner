import os
import pytest

import tests.calculation as calculation

# pytestというツールでテストも可能
# pytestは下記のようにtest_というprefixを付ければ良いだけ
# $ pip install pytest
# printなどを標準出力に出すには、-sのオプションが必要
# $ pytest test_calculation_pytest.py -s

# メソッド単体で書くこと可能
# def test_add_num_and_double():
#     cal = calculation.Cal()
#     assert cal.add_num_and_double(1, 1) == 4

# test実行時に、optionを渡すことができる
# 同フォルダにconftest.pyを作る（中身はそちらを参照）
# そうすることで下記コマンドを打つと、optionsで受け取れるようになっていることがわかる
# $ pytest test_calculation_pytest.py --help

# fixtureでつかるもの
# $ pytest -q --fixtures

# カバレッジ
# $ pip install pytest-cov pytest-xdist
# $ pytest test_calculation_pytest.py --cov --cov-report term-missing

# 他にもnoseというものが紹介されていた
# https://nose.readthedocs.io/en/latest/

# setuptoolsでテストする方法
# setup.pyの 「test_suits='tests'」と指定し、「$ python setup.py test」とかでOK
# pytestでやる場合はsetup.pyのtests_requireにpytestを指定し、
# setup.cfgを作成してあげればそちらで実行も可能

# Toxで仮想環境(Virtual env)でテスト
# tox.iniを作って、toxというコマンドを打てば良いみたい

# seleniumでUIの自動テストも紹介してた
# Note: https://qiita.com/memakura/items/20a02161fa7e18d8a693
# $ pip install selenium
# $ pip install chromedriver-binary==81.0.4044.20.0
# → chromeのバージョンを揃えないとエラーになる
# 詳細はtests/ui/test_ui.pyを参照

env = 'production'


class TestCal(object):
    @classmethod
    def setup_class(cls):
        print('start!!')
        cls.cal = calculation.Cal()
        cls.test_dir = '/tmp/test_dir'
        cls.test_file_name = 'test_fixture.txt'

    @classmethod
    def teardown_class(cls):
        print('end!!')
        del cls.cal
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    # 実行前の処理
    def setup_method(self, method):
        print('setup. method={}'.format(method.__name__))

    # 実行後のお片付け処理
    def teardown_method(self, method):
        print('teardown. method={}'.format(method.__name__))

    def test_save_no_dir(self):
        self.cal.save(self.test_dir, self.test_file_name)
        test_file_path = os.path.join(self.test_dir, self.test_file_name)
        assert os.path.exists(test_file_path) is True

    def test_add_num_and_double(self):
        assert self.cal.add_num_and_double(1, 1) == 4

    # optionは request というfixtureをパラメータに指定することで取得する
    def test_add_num_and_double_option(self, request):
        os_name = request.config.getoption('--os-name')
        print(os_name)

    # fixtureのtmpdirの例
    def test_save(self, tmpdir):
        self.cal.save(tmpdir, self.test_file_name)
        test_file_path = os.path.join(tmpdir, self.test_file_name)
        assert os.path.exists(test_file_path) is True

    # 独自のfixtureを作る例
    # conftestを参照
    def test_original_fixture(self, csv_file):
        print(csv_file)

    # 例外はpytest.raisesをwith構文で書く
    def test_add_num_and_double_raise(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')

    @pytest.mark.skipif(env == 'production', reason='skip!!')
    def test_add_num_and_double_skip(self):
        assert self.cal.add_num_and_double(1, 1) == 4
