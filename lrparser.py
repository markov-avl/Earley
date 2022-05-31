from lrparser import Parser


if __name__ == '__main__':
    parser = Parser(
        [
            'E -> T+E',
            'E -> T',
            'T -> F*T',
            'T -> F',
            'F -> a'
        ],
        'a+a')
    trace = parser.run()
    print(*trace, sep='\n')
