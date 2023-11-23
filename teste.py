from cclang_tokenizer import CCLangTokenizer
import regexp


expr = r"[a-Z]+ \+ [a-Z]+"
test = "Hello + World = Hello World"

# for a, b in regexp.regex_grammar.terminal:
#     print(a, "\t", b)


machine = regexp.compile(expr)
print(machine.match(test))

# for i in regexp.regex_tokenizer.run(expr):
#     print(i)

# tokenizer = CCLangTokenizer()

# input_string = "abc 123 hello world"
# bla = tokenizer.run(input_string)

# for i in bla:
#     print(i)