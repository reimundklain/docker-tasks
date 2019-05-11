

def test_pattern_check():
    from docker_tasks.cli import parse_commands
    app = {
        '*': ['a'],
        '9.*': ['b', 'c'],
        '9.8': ['d']
    }
    commands = []
    parse_commands(app, '9.7', commands)
    assert ['a', 'b', 'c'] == sorted(commands)
