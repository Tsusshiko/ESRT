import os,re

def rotasmanuais():
    resposta2 = input("Indique os detalhes da rota no seguinte formato:(em loops coloque true ou false)\n"
                      "nºrota,loops,nloops\n")
    loop = resposta2.split(",")
    filepath = "../Cupcarbon_G2/gps/route" + loop[0] + ".gps"
    stringfinal = ""
    stringfinal += "Route name\nCity one\nCity two\n" + loop[1] + "\n" + loop[2] + "\n"
    ponto = input("Insira um ponto do seguinte formato (doubles):\n"
                  "Longitude,Latitude\n")
    pontos = ponto.split(",")
    primeiroponto = pontos
    stringfinal += "0 " + pontos[0] + " " + pontos[1] + " 0.0 0.4\n"
    while (ponto != "0"):
        ponto = input("Insira outro ponto\n (Coloque apenas um 0 se não quiser colocar mais pontos)\n")
        if "," in ponto:
            pontos = ponto.split(",")
            stringfinal += "1 " + pontos[0] + " " + pontos[1] + " 0.0 0.4\n"

    if (loop[1] == "true"):
        tempo = input("Quanto tempo para o loop começar?\n")
        stringfinal += tempo + " " + primeiroponto[0] + " " + primeiroponto[1] + " 0.0 0.4\n"
    with open(filepath, "w") as file:
        file.write(stringfinal)

def alterareservas(valor):
    with open("../Cupcarbon_G2/scripts/Gateway.csc", "r") as file:
        script=file.read()

    #\1 representa o primeiro grupo que neste caso é a palavra reserva
    novoscript = re.sub(r'(reserva) (\d+)', r'\1 '+ valor , script)

    with open("../Cupcarbon_G2/scripts/Gateway.csc", "w") as file:
        file.write(novoscript)

def collisions(valor):
    if (valor =="1"):
        with open("../Cupcarbon_G2/scripts/Multihop.csc", "r") as file:
            script=file.read()
        novoscript = re.sub(r'(send x iddestino\n)(send col iddestino)', r'//\1//\2 ', script)
        finalscript= re.sub(r'//(send respum id\n)//(send respdois idsegundo)', r'\1\2 ', novoscript)
        with open("../Cupcarbon_G2/scripts/Multihop.csc", "w") as file:
            file.write(finalscript)
    else:
        with open("../Cupcarbon_G2/scripts/Multihop.csc", "r") as file:
            script=file.read()
        novoscript = re.sub(r'//(send x iddestino\n)//(send col iddestino)', r'\1\2 ', script)
        finalscript =re.sub(r'(send respum id\n)(send respdois idsegundo)', r'//\1//\2 ', novoscript)
        with open("../Cupcarbon_G2/scripts/Multihop.csc", "w") as file:
            file.write(finalscript)

def escolharotas():
    for i in range(1, 11):
        resposta2 = input(
            "Coloque a informação do veículo " + str(i) + " no seguinte formato:(em loops coloque true ou false)\n"
                                                          "nlugar,loops,nloops\n"
                                                          "PS:Se não quiser que esse veículo vá para um lugar, coloque 0 no nlugar.\n")
        resp = resposta2.split(",")
        filepath = "../Cupcarbon_G2/gps/route" + str(i) + ".gps"
        if (resp[0] != "0") and (resp[1] == "true"):
            string = Lugares[int(resp[0])].replace("false", "true")
            string = string.replace("10\n", resp[2] + "\n")
            lastelement = Lugares[int(resp[0])].split("\n")[-2]
            lastelement = lastelement.replace("1 -", "60 -")
            print(lastelement)
            stringfinal = string + lastelement
        else:
            stringfinal = Lugares[int(resp[0])]
        with open(filepath, "w") as file:
            file.write(stringfinal)

Lugares = {1:"Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n1 -8.331257700920105 41.44828352483543 0.0 4.0\n1 -8.331177234649658 41.44819104364697 0.0 4.0\n1 -8.33138644695282 41.44811062511507 0.0 4.0\n"}

Lugares[2]="\n".join(Lugares[1].split("\n")[:-2])+"\n1 -8.331080675125122 41.44808247860536 0.0 4.0\n1 -8.331295251846313 41.44796587150645 0.0 4.0\n"
Lugares[3]="\n".join(Lugares[2].split("\n")[:-2])+"\n1 -8.330994844436646 41.44794978775222 0.0 4.0\n1 -8.331182599067688 41.447861327032705 0.0 4.0\n"
Lugares[4]="\n".join(Lugares[3].split("\n")[:-2])+"\n1 -8.330914378166199 41.447833180414825 0.0 4.0\n1 -8.331107497215271 41.44772461477437 0.0 4.0\n"
Lugares[5]="\n".join(Lugares[4].split("\n")[:-2])+"\n1 -8.330785632133484 41.44771657286786 0.0 4.0\n1 -8.331005573272705 41.44762409087126 0.0 4.0\n"
Lugares[6]="\n".join(Lugares[5].split("\n")[:-2])+"\n1 -8.330608606338501 41.44746727327138 0.0 4.0\n1 -8.33087146282196 41.44735870701889 0.0 4.0\n"
Lugares[7]="\n".join(Lugares[6].split("\n")[:-2])+"\n1 -8.330517411231995 41.44735870701866 0.0 4.0\n1 -8.330801725387573 41.44724611960473 0.0 4.0\n"
Lugares[8]="\n".join(Lugares[7].split("\n")[:-2])+"\n1 -8.330447673797607 41.447226014683544 0.0 4.0\n1 -8.330689072608948 41.44712549000963 0.0 4.0\n"
Lugares[9]="\n".join(Lugares[8].split("\n")[:-2])+"\n1 -8.33036720752716 41.44708930108828 0.0 4.0\n1 -8.33062469959259 41.447008881190754 0.0 4.0\n"
Lugares[10]="\n".join(Lugares[9].split("\n")[:-2])+"\n1 -8.330297470092773 41.446964650204634 0.0 4.0\n1 -8.330533504486084 41.44687216713623 0.0 4.0\n"
Lugares[0]="Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n"


Exemplo1={}
Exemplo1[1]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.33189606666565 41.44892887902438 0.0 4.0\n1 -8.331705629825592 41.44876402280154 0.0 4.0\n1 -8.331563472747803 41.44860318705849 0.0 4.0\n1 -8.331394493579865 41.44845642409503 0.0 4.0\n1 -8.331284523010254 41.4483197130907 0.0 4.0\n1 -8.331201374530792 41.44821717964838 0.0 4.0\n1 -8.33124965429306 41.448164907635025 0.0 4.0\n1 -8.331434726715088 41.448096551861724 0.0 4.0\n"
Exemplo1[2]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.33189606666565 41.44892887902438 0.0 4.0\n1 -8.331705629825592 41.44876402280154 0.0 4.0\n1 -8.331563472747803 41.44860318705849 0.0 4.0\n1 -8.331394493579865 41.44845642409503 0.0 4.0\n1 -8.331284523010254 41.4483197130907 0.0 4.0\n1 -8.331201374530792 41.44821717964838 0.0 4.0\n1 -8.33113431930542 41.44814882393014 0.0 4.0\n1 -8.331096768379211 41.44809052046652 0.0 4.0\n1 -8.331185281276703 41.44803824835114 0.0 4.0\n1 -8.331335484981537 41.44796386103737 0.0 4.0\n"
Exemplo1[3]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.330281376838684 41.44809454139673 0.0 4.0\n1 -8.330592513084412 41.447981955256694 0.0 4.0\n1 -8.33087682723999 41.4479256621134 0.0 4.0\n1 -8.331236243247986 41.447841222306884 0.0 4.0\n"
Exemplo1[4]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.33189606666565 41.44892887902438 0.0 4.0\n1 -8.331705629825592 41.44876402280154 0.0 4.0\n1 -8.331563472747803 41.44860318705849 0.0 4.0\n1 -8.331394493579865 41.44845642409503 0.0 4.0\n1 -8.331284523010254 41.4483197130907 0.0 4.0\n1 -8.331201374530792 41.44821717964838 0.0 4.0\n1 -8.331107497215271 41.44809454139673 0.0 4.0\n1 -8.330868780612946 41.44782513852027 0.0 4.0\n1 -8.331120908260345 41.44772461476565 0.0 4.0\n"
Exemplo1[5]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.330332338809967 41.44704305965937 0.0 4.0\n1 -8.330396711826324 41.44716569989859 0.0 4.0\n1 -8.33049327135086 41.4473084448031 0.0 4.0\n1 -8.330571055412292 41.447443147453114 0.0 4.0\n1 -8.330643475055695 41.447523566812364 0.0 4.0\n1 -8.330710530281067 41.447632132789245 0.0 4.0\n1 -8.330782949924469 41.44770451000621 0.0 4.0\n1 -8.33099752664566 41.44762006991189 0.0 4.0\n1 -8.330801725387573 41.447696468097206 0.0 4.0\n1 -8.330847322940826 41.44778090809212 0.0 4.0\n1 -8.330922424793243 41.44789751552346 0.0 4.0\n1 -8.331086039543152 41.44812067743702 0.0 4.0\n1 -8.331214785575867 41.44825336794064 0.0 4.0\n1 -8.33137035369873 41.44844436137093 0.0 4.0\n1 -8.33137035369873 41.44844436137093 0.0 4.0\n"
Exemplo1[6]="Route name\nCity one\nCity two\nfalse\n3\n0 -8.330034613609314 41.44649419148628 0.0 4.0\n1 -8.330104351043701 41.44663090633725 0.0 4.0\n1 -8.33014726638794 41.44673947380781 0.0 4.0\n1 -8.330233097076416 41.446884230152634 0.0 4.0\n1 -8.330335021018982 41.447041049161726 0.0 4.0\n1 -8.330420851707458 41.4471335319894 0.0 4.0\n1 -8.330479860305786 41.447274266474274 0.0 4.0\n1 -8.330565690994263 41.44737479091941 0.0 4.0\n1 -8.330603241920471 41.44746325230229 0.0 4.0\n1 -8.330683708190918 41.44743912648256 0.0 4.0\n1 -8.330769538879395 41.44740293773614 0.0 4.0\n1 -8.33087682723999 41.447362727994204 0.0 4.0\n"
Exemplo1[7]="Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n"
Exemplo1[8]="Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n"
Exemplo1[9]="Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n"
Exemplo1[10]="Route name\nCity one\nCity two\nfalse\n10\n0 -8.33161175251007 41.44862128109947 0.0 4.0\n1 -8.331429362297058 41.448468486816886 0.0 4.0\n"


resposta1 =input("Que opção deseja?\n"
                 "Opção 1 -Exemplos\n"
                 "Opção 2 -Associar um lugar a um veiculo\n"
                 "Opção 3 -Definir uma rota manualmente\n"
                 "Opção 4 -Alterar o numero de mensagens para haver uma reserva\n"
                 "Opção 5 -Alterar a presença ou não de tratamento de colisões\n"
                 )

match resposta1:
    case "1":
        exemplo= input("Que exemplo deseja:\n"
                       "1-Reserva num lugar que se tornou livre e poderá haver uma colisão entre 1-5\n"
                       "2-Estacionamento acaba por ficar cheio e haverão reservas que serão usufruídas\n")

        if (exemplo=="1"):
            for i in range(1, 11):
                filepath = "../Cupcarbon_G2/gps/route" + str(i) + ".gps"
                stringfinal = Exemplo1[i]
                with open(filepath, "w") as file:
                    file.write(stringfinal)
        if (exemplo=="2"):
            for i in range(1, 11):
                filepath = "../Cupcarbon_G2/gps/route" + str(i) + ".gps"
                stringfinal = Lugares[i]
                with open(filepath, "w") as file:
                    file.write(stringfinal)
    case "2":
        escolharotas()
    case "3":
        rotasmanuais()
    case "4":
        reserva= input("Quantas mensagens dos sensores até haver uma reserva?\n")
        alterareservas(reserva)
    case "5":
        colisoes= input("Deseja colocar ou remover o tratamento de colisões?\n"
                        "1- Colocar\n"
                        "2- Remover\n")
        collisions(colisoes)


