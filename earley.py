import earley


def walk(node, level=0):
    print(level * '-' + node['a'])
    for child in node['children']:
        walk(child, level + 1)


if __name__ == '__main__':
    grammar = earley.Grammar('S')
    grammar.add('S', '0S') \
        .add('S', '1S') \
        .add('S', '1') \
        .add('S', '0')

    parser = earley.Parser(grammar)
    parser.run('101011')

    completes = parser.get_completes()
    if completes:
        walk(parser.make_node(completes[0]))
    else:
        print('Произошла ошибка')
