class Regra(str):
    def __repr__(self):
        return "Regra"

tabela = {
    ('S', '0M'): ['B'],
    ('S', '1M'): ['B'],
    ('S', '0'): ['B'],
    ('S', '1'): ['B'],

    ('B', '0M'): ['0M', 'Bl'],
    ('B', '1M'): ['1M', 'Bl'],
    ('B', '0'): ['0'],
    ('B', '1'): ['1'],

    ('Bl', '0m'): ['Om','B'],
    ('Bl', '1m'): ['1m', 'B'],
    ('Bl', '0'): ['0'],
    ('Bl', '1'): ['1'],
}

tabela_regras = {
    ('S', '0M'): Regra('S.val = B.val'),
    ('S', '1M'): Regra('S.val = B.val'),
    ('S', '0'): Regra('S.val = B.val'),
    ('S', '1'): Regra('S.val = B.val'),

    ('B', '0M'): Regra('B.lvl = Bl.lvl + 1; B.val = Bl.val'),
    ('B', '1M'): Regra('B.lvl = Bl.lvl + 1; B.val = 2**B.lvl + Bl.val'),
    ('B', '0'): Regra('B.val = 0; Bl.lvl = 0'),
    ('B', '1'): Regra('B.val = 1; Bl.lvl = 0'),

    ('Bl', '0m'): Regra('Bl.lvl = B.lvl + 1; Bl.val = B.val'),
    ('Bl', '1m'): Regra('Bl.lvl = B.lvl + 1; Bl.val = 2**Bl.lvl + B.val'),
    ('Bl', '0'): Regra('Bl.val = 0; Bl.lvl = 0'),
    ('Bl', '1'): Regra('Bl.val = 1; Bl.lvl = 0'),
}

memoria_regras = {
    'Bl.val': 0,
    'B.val': 0,
    'Bl.lvl': 0,
    'B.lvl': 0,
    'S.val': 0,
}

def executa_regra(rule):
    for key in memoria_regras:
        rule = rule.replace(key, f'memoria_regras["{key}"]')
    exec(rule)

terminal = {'0M','1m','0m','1M','0','1'}
naoterminal = {'S', 'B', 'Bl'}
w = ['0M','1m','1M','0']
ip = 0
stack = []
stack.append('$')
stack.append('S')
x = stack[-1]

print(stack)
while x != '$':
    if isinstance(x, Regra):
        executa_regra(x)
        stack.pop()
        x = stack[-1]
        continue

    if x == w[ip]:
        stack.pop()
        x = stack[-1]
        ip = ip + 1
        continue

    if x in terminal:
        print()
        print('Ocorreu um erro')
        break

    if (x, w[ip]) not in tabela:
        print()
        print(f'Ocorreu um erro: Caractere inesperado "{w[ip]}"')
        break
    

    stack.pop()
    regra = tabela_regras.get((x, w[ip]), None)
    if regra is not None:
        pass
        # stack.append(regra)
    
    derivados = tabela[x,w[ip]]
    stack.extend(reversed(derivados))
    x = stack[-1]

    print(stack)

else:
    # Só entra aqui o loop não for interrompido por um erro
    print()
    print("S.val =", memoria_regras["S.val"])