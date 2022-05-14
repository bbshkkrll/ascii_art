import unittest
from arg_parser import ArgParser


class MyTestCase(unittest.TestCase):
    def test_args_parser(self):
        parser = ArgParser(
            ['-i', 'in\\unnamed.jpg', '-s', '0.3'])

        self.assertEqual('out\\unnamed_result.txt', parser.out)


if __name__ == '__main__':
    unittest.main()
