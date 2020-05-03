import pytest

# fixtureの継承も可能
@pytest.fixture
def csv_file(tmpdir):
    # return 'csv file!!'
    # 下記のようにyieldを書くと、テストの時にopenとかcloseとかを気にしなくてOKになる
    with open('../test.csv', 'r') as c:
        print('before test')
        yield c
        print('after test')


def pytest_addoption(parser):
    parser.addoption('--os-name', default='linux', help='os name')
