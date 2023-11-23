from cclang_tokenizer import CCLangTokenizer


tokenizer = CCLangTokenizer()

input_string = "abc 123 hello world"
bla = tokenizer.run(input_string)

for i in bla:
    print(i)