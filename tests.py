import unittest


class TestCommandPattern(unittest.TestCase):
    def test_pattern_check(self):
        from docker_tasks.cli import parse_commands
        app = {
            '*': ['a'],
            '9.*': ['b', 'c'],
            '9.8': ['d']
        }
        commands = []
        parse_commands(app, '9.7', commands)
        self.assertEqual(['a', 'b', 'c'], sorted(commands))



if __name__ == '__main__':
    unittest.main()
