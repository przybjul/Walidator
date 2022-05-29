import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Scanner:

    def __init__(self, input):
        self.tokens = []
        self.current_token_number = 0
        for token in self.tokenize(input):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {'voltagesource', 'voltageprobe', 'currentsource', 'currentprobe',
                    'resistor', 'capacitor', 'inductor', 'diode', 'begin', 'end', 'gnd'}
        token_specification = [
            # Integer or decimal number - positive or negative, scientific numbers
            ('NUMBER',    r'-?[\d.]+(?:e-?\d+)?'),
            ('ASSIGN',    r'='),          # Assignment operator
            ('END',       r';'),           # Statement terminator
            ('ID',        r'[A-Za-z]+[0-9]+|[A-Za-z_]+'),  # Identifiers to do 5e^-1
            ('NEWLINE',   r'\n'),          # Line endings
            ('SKIP',      r'[ \t]'),       # Skip over spaces and tabs
            ('OPEN_PAR',  r'\('),          # open parenthesis
            ('CLOSE_PAR', r'\)'),          # close parenthesis
            ('OPEN_IDX',  r'\['),          # Open index
            ('CLOSE_IDX', r'\]'),          # Close index
            ('CON',       r'--'),          # Connection
            ('COMMA',     r','),           # Comma


        ]
        tok_regex = '|'.join('(?P<%s>%s)' %
                             pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1
            elif type != 'SKIP':
                value = match.group(type)
                if type == 'ID' and value in keywords:
                    type = value
                yield Token(type, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' %
                               (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position-line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number-1 < len(self.tokens):
            return self.tokens[self.current_token_number-1]
        else:
            raise RuntimeError('Error: No more tokens')
