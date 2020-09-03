ALPHABET =['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#errors
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln +1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#position
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#tokens
TAML_TT_ALPHA = 'ALPHA'
TAML_TT_CRETURN = 'CRETURN'
TAML_TT_TAB = 'TAB'
TAML_TT_COMMENT = 'COMMENT'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#lexer
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        self.previous_char = self.text[self.pos.idx-1] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens =[]

        while self.current_char !=None:

            if self.current_char == '\t':
                print(f'found tab at {self.pos.idx}')
                tokens.append(Token(TAML_TT_TAB))
                self.advance()

            elif self.current_char in ALPHABET:
                tokens.append(Token(TAML_TT_ALPHA, str(self.current_char)))
                self.advance()

            elif self.current_char =='\r':
                print(f'found carriage return at {self.pos.idx}')
                tokens.append(Token(TAML_TT_CRETURN))
                self.advance()

            elif self.current_char =='-':
                if self.previous_char == '-':
                    tokens.append(Token(TAML_TT_COMMENT))
                    print(f'found comment at {self.pos.idx}')
                    self.advance()
                else:
                    self.advance()

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos,"'"+ char +"'")

        return tokens, None






#run the thing
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error