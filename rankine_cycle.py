import tabelas

#Entrada de Dados
print("\n***************** Dados de Entrada *****************\n")
print("-> Pressões entre 11 e 20000 KPa")
baixa_pressao = int(input("1) Valor de Baixa Pressão (KPa): "))
alta_pressao = int(input("2) Valor de Alta Pressão (KPa): "))
temp_super_aquec = int(input("3) Valor da T de super aquecimento (ºC): "))
eficiencia_turbina = int(input("4) Eficiência da Turbina (%): "))
eficiencia_turbina = eficiencia_turbina/100
eficiencia_bomba = int(input("5) Eficiência das Bombas (%): "))
eficiencia_bomba = eficiencia_bomba/100
trabalho_desejado = float(input("6) Trabalho desejado (KW): "))
fluido = str(input("7) Escolha o fluido (Só tem água): "))

#Chamando a Classe Tabelas
tabela = tabelas.Tabelas

#Criando lista de possíveis pressões intermediárias
pressao_intermediaria = []
#Número de posições possíveis para o Regenerador
numero_divisoes = 1000
#Distância entre as possíveis posições do Regenerador
passo = (alta_pressao - baixa_pressao) / numero_divisoes
#Montando a lista de posições
add_intermediario = baixa_pressao + passo
while add_intermediario < alta_pressao:
    pressao_intermediaria.append(add_intermediario)
    add_intermediario += passo

#Criando listas para armazenar os valores de todos elementos em cada iteração
h1_lista = []
h2_lista = []
h3_lista = []
h4_lista = []
h5_lista = []
h6_lista = []
h7_lista = []
m1_lista = []
wb1_lista = []
wb2_lista = []
qh_lista = []
rendimento_lista = []
wt_lista = []
vazao_sistema_lista = []
x7_lista = []

'''
DESCOMENTAR ESSA LINHA PARA CICLO RANKINE SIMPLES
pressao_intermediaria = [baixa_pressao]
'''

#Percorrendo todos os valores da lista de Pressões Intermediárias
for i in range(0,len(pressao_intermediaria)):
    #Definindo a pressão em cada ponto
    p1 = baixa_pressao
    p2 = pressao_intermediaria[i]
    p3 = pressao_intermediaria[i]
    p4 = alta_pressao
    p5 = alta_pressao
    p6 = pressao_intermediaria[i]
    p7 = baixa_pressao
    # Temos p1, p2
    # h1 da tabela (Posição 6, Entalpia líquido saturado)
    h1 = tabela.interpolar_agua_saturada(p1, 6)

    # 1) Trabalho na bomba 1 -> wb1 = v(p2-p1)
    v = tabela.interpolar_agua_saturada(baixa_pressao, 1) #Usar v de qual pressão?????
    wb1 = v*(p2 - p1)
    
    wb1 = wb1/eficiencia_bomba #Considerando a eficiência da bomba

    # 2) Entalpia depois da bomba 1 -> h2 – h1 = wb1
    h2 = wb1 + h1

    # Temos p3, p4
    # h3 da tabela (Posição 6, Entalpia líquido saturado
    h3 = tabela.interpolar_agua_saturada(p3, 6)

    # 3) Trabalho na bomba 2 -> wb2 = v(p4-p3)

    wb2 = v*(p4 - p3)
    
    wb2 = wb2/eficiencia_bomba #Considerando a eficiência da bomba

    # 4)	Entalpia depois da bomba 2 -> h4-h3 = wb2
    h4 = wb2 + h3


    # Temos p5( = alta_pressao ), T5, p6( = pressao_intermediaria ), p7( = baixa_pressao )
    # s5 da tabela (Posição 11, Entropia vapor saturado) -> Adicionar vapor superaquecido!!!!
    ''' @@@ Para saturado -> s5 = tabela.interpolar_agua_saturada(p5, 11) @@@ '''
    T5 = temp_super_aquec
    s5 = tabela.interpolar_mestre(p5, T5, [11, 4], 0)

    #h5 da tabela (Posição 8, Entalpia vapor saturado) -> Adicionar vapor superaquecido!!!!
    ''' @@@ h5 = tabela.interpolar_agua_saturada(p5, 8) @@@ '''
    h5 = tabela.interpolar_mestre(p5, T5, [8, 3], 0)
    
    #PASSO ADICIONAL
    #I)Verificar a região ideal com entropia ideal
    #II)Encontrar (interpolando) entalpia ideal com entropia ideal
    #III) Encontrar entalpia real com eficiência da turbina
    #IV) Verificar região real com entalpia real
    #V) Se for superaquecido -> encontra s6 atraves de h6
    #VI) Se não, acha o título através do passo 8)
    
    s6s = s5

    h6s = tabela.interpolar_mestre(p6, s6s, [8, 3])
    
    h6 = h5 - eficiencia_turbina*(h5 - h6s)
    
    regiao = tabela.interpolar_mestre(p6, h6, [8, 3], 3, retornar_sat_ou_super = True) #Regiao True => Saturado; Regiao False=>Superaquecido

    if regiao == False:
        s6 = tabela.interpolar_mestre(p6, h6, [11, 4], 3)
    else:       
    
        # 5)	Encontrar x6s (através de s5 = s6s)
        # s6s = s_pressao_inter_liq + x6s*s_pressao_inter_evap
        # s_liq (Posição 9) // s_evap(Posição 10)

        #Verificar se é saturado ou superaquecido
        '''sat_ou_super = tabela.interpolar_mestre(p6, s5 ) @@@@@@@@@ Travamos!!!!!!!!'''

        '''s_pressao_inter_liq = tabela.interpolar_agua_saturada(p6, 9)
        s_pressao_inter_evap = tabela.interpolar_agua_saturada(p6, 10)
        s6s = s5
        x6s = (s6s - s_pressao_inter_liq)/s_pressao_inter_evap'''


        '''# 6)	Encontrar h6s
        # h6s = h_pressao_inter_liq + x6s*h_pressao_inter_evap
        h_pressao_inter_liq = tabela.interpolar_agua_saturada(p6, 6)
        h_pressao_inter_evap = tabela.interpolar_agua_saturada(p6, 7)
        h6s = h_pressao_inter_liq + x6s*h_pressao_inter_evap'''

        '''# 7)	Encontrar h6 (real) pela eficiência da turbina -> eficiencia_turbina = h5 – h6/ h5 – h6s
        h6 = h5 - eficiencia_turbina*(h5 - h6s)'''

        h_pressao_inter_liq = tabela.interpolar_agua_saturada(p6, 6)
        h_pressao_inter_evap = tabela.interpolar_agua_saturada(p6, 7)

        # 8)	Encontrar o título (real) x6
        x6 = (h6 - h_pressao_inter_liq) / h_pressao_inter_evap
        # s6 = s_pressao_inter_liq + x6s*s_pressao_inter_evap
        s6 = s_pressao_inter_liq + x6*s_pressao_inter_evap


    # 9)	Encontrar a fração mássica (m1) -> m1*h6 + (1-m1)*h2 = h3
    m1 = (h3 - h2)/(h6-h2)

    
    s7s = s6

    h7s = tabela.interpolar_mestre(p7, s7s, [8, 3], 4)
    
    h7 = h6 - eficiencia_turbina*(h6 - h7s)
    
    regiao = tabela.interpolar_mestre(p7, h7, [8, 3], 3, retornar_sat_ou_super = True) #Regiao True => Saturado; Regiao False=>Superaquecido

    if regiao == False:
        s7 = tabela.interpolar_mestre(p7, h7, [11, 4], 3)
    else:         


        h_pressao_inter_liq = tabela.interpolar_agua_saturada(p7, 6)
        h_pressao_inter_evap = tabela.interpolar_agua_saturada(p7, 7)

        # 8)	Encontrar o título (real) x6
        x7 = (h7 - h_pressao_inter_liq) / h_pressao_inter_evap
        # s6 = s_pressao_inter_liq + x6s*s_pressao_inter_evap
        s7 = s_pressao_inter_liq + x7*s_pressao_inter_evap
    
    '''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''

    '''    # 10) Encontrar x7s (através de s6 = s7s)
    # s7s = s_pressao_baixa_liq + x7s*s_pressao_baixa_evap
    # s_liq (Posição 9) // s_evap(Posição 10)
    s_pressao_baixa_liq = tabela.interpolar_agua_saturada(p7, 9)
    s_pressao_baixa_evap = tabela.interpolar_agua_saturada(p7, 10)

    s7s = s6
    x7s = (s7s - s_pressao_baixa_liq)/s_pressao_baixa_evap

    # 10) Encontrar h7s
    # h7s = h_pressao_baixa_liq + x6s*h_pressao_baixa_evap
    h_pressao_baixa_liq = tabela.interpolar_agua_saturada(p7, 6)
    h_pressao_baixa_evap = tabela.interpolar_agua_saturada(p7, 7)
    h7s = h_pressao_baixa_liq + x7s*h_pressao_baixa_evap

    # 11) Encontrar h7 (real) pela eficiência da turbina -> eficiencia_turbina = h6 – h7/ h6 – h7s
    h7 = h6 - eficiencia_turbina*(h6 - h7s) 

    # 12) Encontrar o título (real) x7 -> Saída do programa
    x7 = (h7 - h_pressao_baixa_liq) / h_pressao_baixa_evap '''


    # 13)	Trabalho da turbina(kJ/kg) -> wt = (h5-h6) + (1-m1)*(h6 – h7)
    wt = (h5-h6) + (1-m1)*(h6 - h7)

    # 14)	Encontrar vazão do sistema (trabalho_desejado/wt) -> Saída do programa
    vazao_sistema = trabalho_desejado/wt


    # 15)	Encontrar qh = h5 – h4
    qh = h5 - h4


    # 16)	Encontrar ql = h7 – h1
    ql = h7 - h1


    # 17)	Encontrar rendimento: wliq/qh -> Onde wliq = wt – (1 – m1)*wb1 – wb2
    wliq = wt - (1 - m1)*wb1 - wb2
    rendimento = wliq/qh


    # 18)	Encontrar Qh, Ql
    Qh = qh * vazao_sistema
    Ql = ql * vazao_sistema

    #Adicionando o valor da iteração nas listas
    h1_lista.append(h1)
    h2_lista.append(h2)
    h3_lista.append(h3)
    h4_lista.append(h4)
    h5_lista.append(h5)
    h6_lista.append(h6)
    h7_lista.append(h7)
    m1_lista.append(m1)
    wb1_lista.append(wb1)
    wb2_lista.append(wb2)
    qh_lista.append(qh)
    rendimento_lista.append(rendimento)
    wt_lista.append(wt)
    vazao_sistema_lista.append(vazao_sistema)

print ("\n******************* Imprimindo Saídas *******************\n")
print ("\n------------ Referentes ao rendimento máximo ------------\n")
#Encontrando maior rendimento e a posição dele na lista
rendimento_maximo = max(rendimento_lista)
indice = rendimento_lista.index(rendimento_maximo)

#Pressão intermediária que fornece rendimento máximo
pressao_int_max = pressao_intermediaria[indice]
print ("Pressão Inter. de Rendimento Máximo = ",pressao_int_max)
print ("h1 = ",h1_lista[indice])
print ("h2 = ",h2_lista[indice])
print ("h3 = ",h3_lista[indice])
print ("h4 = ",h4_lista[indice])
print ("h5 = ",h5_lista[indice])
print ("h6 = ",h6_lista[indice])
print ("h7 = ",h7_lista[indice])
print ("Fração mássica = ",m1_lista[indice])
print ("wb1 = ",wb1_lista[indice])
print ("wb2 = ",wb2_lista[indice])
print ("qh = ",qh_lista[indice])
print ("n = ",rendimento_lista[indice])
print ("wt = ",wt_lista[indice])
print ("Vazão = ",vazao_sistema_lista[indice])

'''
Cuidado ao descomentar essa parte se colocar o número de divisões muito grande!
print("Pressões testadas", pressao_intermediaria)
print ("h1 = ",h1_lista)
print ("h2 = ",h2_lista)
print ("h3 = ",h3_lista)
print ("h4 = ",h4_lista)
print ("h5 = ",h5_lista)
print ("h6 = ",h6_lista)
print ("h7 = ",h7_lista)
print ("Fração mássica = ",m1_lista)
print ("wb1 = ",wb1_lista)
print ("wb2 = ",wb2_lista)
print ("qh = ",qh_lista)
print ("n = ",rendimento_lista)
print ("wt = ",wt_lista)
print ("Vazão = ",vazao_sistema_lista)
'''
print ("\n*********************** FIM ***********************\n")
