from lrparser import Grammar, Parser

if __name__ == '__main__':
    grammar = Grammar(
        'E',
        'E -> T+E',
        'E -> T',
        'T -> F*T',
        'T -> F',
        'F -> a'
    )
    parser = Parser(grammar)
    trace = parser.run('a+a')
    print(*trace, sep='\n')
