from random import * 

base_name = 'svn_'
indice = 0
max_indice = 100

base = 100
factor = 100


if __name__ == "__main__":
    while (indice < max_indice):
        gflops = base + randint(-500, 500) / float(factor)
        print(base_name + str(indice) + ',' +  str(gflops))
        
        indice += 1
        base += 1
