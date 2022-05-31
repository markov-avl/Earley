from llparser import Parser


if __name__ == '__main__':
    parser = Parser(
        [
            'E -> E+T',
            'E -> T',
            'T -> T*F',
            'T -> F',
            'F -> a'
        ],
        'a*a')
    trace = parser.run()
    print(*trace, sep='\n')
