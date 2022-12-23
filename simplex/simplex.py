from numpy import matrix
from numFracionario import NumFracionario

class Tabela(object):
    def __init__(self, funcao_objetivo, restricoes=None):
        self.linha_restricao = []
        quatidade_variaveis_extra = len(restricoes) + len([(c,t,tr) for (c,t,tr) in restricoes if t!='<='])
        self.linha_funcao_objetivo = [1] + [c*(-1) for c in funcao_objetivo] + [0]*quatidade_variaveis_extra + [0] 
        
        for i,(coeficientes, tipo, termo) in enumerate(restricoes):
            coluna_extra = [0]*quatidade_variaveis_extra
            
            if tipo == '<=':
                coluna_extra[i] = 1       
                
            elif tipo == '=':
                coluna_extra[i] = 1         
                self.linha_funcao_objetivo[1 + len(coeficientes) + i] = NumFracionario(0, NumFracionario(1))
                      
            elif tipo == '>=':
                coluna_extra[i] = -1
                coluna_extra[i + 1] = 1              
                self.linha_funcao_objetivo[1 + len(coeficientes) + i + 1] = NumFracionario(0, NumFracionario(1))
            
            self.linha_restricao.append(self.converteFracionario([0] + coeficientes + coluna_extra + [termo]))
        
    def converteFracionario(self,lista):
        return [NumFracionario(e) for e in lista]
       
    def imprimirTabela(self):      
        tabela = [self.linha_funcao_objetivo] + self.linha_restricao    
        print('\n', matrix([[str(f) for f in l] for l in tabela]))
           
    def _encontraEntra(self):
        menor_coeficiente = min(self.linha_funcao_objetivo[1:-1])
        
        if menor_coeficiente >= 0: 
            return None
        else:        
            return self.linha_funcao_objetivo[0:-1].index(menor_coeficiente)
  
    def _encontraSai(self, colunaDoPivo):   
        termos = [r[-1] for r in self.linha_restricao]
        variavel_entra = [r[colunaDoPivo] for r in self.linha_restricao]
        
        razoes = []
        for i,termo in enumerate(termos):
            if variavel_entra[i] == 0:
                razoes.append(NumFracionario(1,1))
            else:
                razoes.append(termo / variavel_entra[i])
                
        menor_positivo = min([r for r in razoes if r > 0])        
        return razoes.index(menor_positivo)
  
    def pivoteamento(self, pi, pj):
        p = self.linha_restricao[pi][pj]     
        self.linha_restricao[pi] = [x/p for x in self.linha_restricao[pi]]     
        tempLinha = [self.linha_funcao_objetivo[pj]* x for x in self.linha_restricao[pi]]  
        self.linha_funcao_objetivo = [self.linha_funcao_objetivo[i] - tempLinha[i] for i in range(len(tempLinha))]
        
        for i,restricao in enumerate(self.linha_restricao):
            if i != pi: 
                tempLinha = [restricao[pj]* x for x in self.linha_restricao[pi]]         
                self.linha_restricao[i] = [restricao[i] - tempLinha[i] for i in range(len(tempLinha))]   
  
    def solucaoOtimaEncontrada(self):
        if min(self.linha_funcao_objetivo[1:-1]) >= 0: 
            return True
        else:
            return False
     
    def executar(self):
        self.imprimirTabela()
        
        while not self.solucaoOtimaEncontrada():
            c = self._encontraEntra()
            r = self._encontraSai(c)
            
            self.pivoteamento(r,c)
            
            print('\nColuna do pivo: %s\nLinha do pivo: %s'%(c+1,r))
            
            self.imprimirTabela()
    
    @property
    def variaveisDentroBase(self):      
        dentro_base = [] 
        for c in range(1,len(self.linha_funcao_objetivo)-1):
            valor_coluna = [l[c] for l in self.linha_restricao]
            
            numDeZeros = len([z for z in valor_coluna if z==NumFracionario(0)])
            numDeUms = len([u for u in valor_coluna if u==NumFracionario(1)])
            
            if numDeUms == 1 and numDeZeros == len(self.linha_restricao) - 1 :
                dentro_base.append(c)

        return dentro_base
    
    @property
    def variaveisForaBase(self):
        return [i for i in range(1,len(self.linha_funcao_objetivo)-1) if i not in self.variaveisDentroBase]
        
    @property  
    def solucaoOtima(self):
        if not self.solucaoOtimaEncontrada():
            self.executar() 
        
        dentro = self.variaveisDentroBase
        fora = self.variaveisForaBase
        
        solucao = []

        for val in dentro:
            for l in self.linha_restricao:
                if l[val] == NumFracionario(1):
                    solucao.append((val,l[-1]))
                    break
        
        solucao += [(val,NumFracionario(0)) for val in fora]

        return [(t[0],float(t[1])) for t in solucao]
        
    @property
    def valorOtimo(self):
        if not self.solucaoOtimaEncontrada():
            self.executar()
        
        return self.linha_funcao_objetivo[-1]
             
             
def getNomeDeVariavel(index):
    return 'x' + str(index)

def toStringComNomes(lista):
    if type(lista[0]) is type(0):
        return [getNomeDeVariavel(i) for i in lista]
    
    elif type(lista[0]) is type(()):
        return [(getNomeDeVariavel(l[0]),l[1]) for l in lista]

if __name__ == '__main__':
    t = Tabela([20, 24],restricoes=[([3, 6],"<=", 60),([4, 2],",<=", 32)])
    
    print("\nValor otimo: %s (%s)" % (float(t.valorOtimo),t.valorOtimo))
    print("\nBasicas: %s" % (toStringComNomes(t.variaveisDentroBase)))
    print("\nNão Basicas: %s" % (toStringComNomes(t.variaveisForaBase)))
    print("\nSolução otima: %s" % (toStringComNomes(t.solucaoOtima)))