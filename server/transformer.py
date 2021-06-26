from typing import List
from enum import IntEnum
from dataclasses import dataclass
from pprint import pprint
from collections import deque


class TokenType(IntEnum):
    TEXT = 0
    LINE_COMMENT = 1
    INLINE_COMMENT = 2


@dataclass
class Token:
    type: TokenType
    content: str


# class Context(IntEnum):
#     TEXT = 0
#     LINE_COMMENT = 1
#     INLINE_COMMENT = 2


class Transformer:

    def transform(self, document: str) -> str:
        print("transforming...")
        tokens = self.tokenize(document)
        pprint(tokens)
        return "yay"

    def tokenize(self, document: str) -> List[Token]:
        print("tokenizing...")
        print(len(document))
        res: List[Token] = []
        contexts = deque[TokenType]()
        contexts.append(TokenType.TEXT)
        token_start = 0
        for pos, char in enumerate(document):
            context = contexts[-1]
            if char == '#' and context != TokenType.INLINE_COMMENT:
                if pos > token_start:
                    res.append(Token(context, document[token_start:pos]))
                    token_start = pos
                contexts.append(TokenType.LINE_COMMENT)
            elif char == '\n' and context == TokenType.LINE_COMMENT:
                res.append(Token(contexts.pop(), document[token_start:pos+1]))  # QUESTION: do I want to retain newlines at end of token? probably
                token_start = pos + 1
            elif char == '\n' and context != TokenType.INLINE_COMMENT:
                res.append(Token(context, document[token_start:pos+1]))
                token_start = pos + 1
            elif char == '/' and document[pos+1] == '*' and context != TokenType.LINE_COMMENT:
                if pos > token_start:
                    res.append(Token(context, document[token_start:pos]))
                    token_start = pos
                contexts.append(TokenType.INLINE_COMMENT)
            elif char == '/' and document[pos-1] == '*' and context == TokenType.INLINE_COMMENT:
                res.append(Token(contexts.pop(), document[token_start:pos+1]))
                token_start = pos + 1
                context = TokenType.TEXT
            # TODO: more types
        return res

 # ----------- testing ---------------


def test():
    import time
    start = time.time()
    print('testing transfomer')
    transformer = Transformer()
    with open('data/sample.ttr', 'r+', encoding='utf-8') as f:
        # headls = [l for l in f.readlines() if len(l) > 2]
        # if len(headls) > 10:
        #     headls = headls[:10]
        # head = ''.join(headls)
        data = f.read()
    # print(head)
    out = transformer.transform(data)
    # print(out)
    end = time.time()
    duration = end - start
    print(f'Time elapsed: {duration:.3f} ms')


if __name__ == "__main__":
    test()
