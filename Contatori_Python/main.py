'''
Author: Andrea Tomatis

Date: January 3, 2020

Licence: open source
'''

tab_eccitazione_flip_flop_singoli = {'t' : {'0:0' : '0', 
                                            '0:1' : '1',
                                            '1:0' : '1',
                                            '1:1' : '0'},
                                     'd' : {'0:0' : '0',
                                            '0:1' : '1',
                                            '1:0' : '0',
                                            '1:1' : '1'}}

tab_eccitazione_flip_flop_doppi =  {'jk' : {'0:0' : ['0','X'],
                                            '0:1' : ['1','X'],
                                            '1:0' : ['X','1'],
                                            '1:1' : ['X','0']},
                                    'sr' : {'0:0' : ['0','X'],
                                            '0:1' : ['1','0'],
                                            '1:0' : ['0','1'],
                                            '1:1' : ['X','0']}}


def check_if_exit(name):
    if name.lower() == 'exit':
        exit()


def leggiDati():
    mod = input("inserisci il modulo del contatore: ")
    check_if_exit(mod)
    verso = input("inserisci il verso del contatore(up/down): ")
    check_if_exit(mod)
    if verso.lower() != 'up' and verso.lower() != 'down':
        raise Exception("invalid input")
    tipo = input("inserisci il tipo di flif-flop da utilizzare: ")
    check_if_exit(mod)
    if tipo.lower() != 'jk' and tipo.lower() != 't' and tipo.lower() != 'd' and tipo.lower() != 'sr':
        raise Exception("invalid input")

    return int(mod),verso,tipo


def generaTabEccitazione(mod,nflipflop, tipo, verso):
    try:
        tab_eccitazione = tab_eccitazione_flip_flop_singoli[tipo.lower()]
    except Exception:
        tab_eccitazione = tab_eccitazione_flip_flop_doppi[tipo.lower()]
    
    tab = []

    if verso == 'up':
        start = 0
        end = mod
        inc = 1
    else:
        start = mod-1
        end = -1
        inc = -1

    for i in range (start, end, inc):
        val = bin(i)[2:]
        tab.append(val.zfill(nflipflop))
        
    caratteri = []
    for num in tab:
        let = []
        for letter in num:
            let.append(letter)
        caratteri.append(let)

    
    
    for i in range(len(caratteri)):
        tab2 = []
        for j in range(nflipflop):
            digit = caratteri[i][j]
            future_digit = caratteri[(i+1) % len(caratteri)][j]
            chiave = ""
            chiave += digit + ':' + future_digit
            tab2.append(tab_eccitazione[chiave])
        tab[i] = {" ".join(caratteri[i]) : tab2}
    

    return tab


def main():
    
    while True:
        print("--------CONTATORI-----------")
        mod,verso,tipo = leggiDati()

        nflipflop = 0
        while 2**nflipflop < mod:
            nflipflop += 1
        
        tab_eccitazione = generaTabEccitazione(mod,nflipflop, tipo, verso)

        for i,elem in enumerate(tab_eccitazione):
            print(str(i).zfill(3),elem)


if __name__ == "__main__":
    main()
