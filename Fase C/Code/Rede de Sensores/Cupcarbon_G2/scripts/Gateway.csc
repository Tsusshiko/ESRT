//Variaveis para print
set alterado 0
set alteradore 0
set acao 0
// Mensagem inicial que permite que possamos correr logo o publisher
printfile alterado ": " acao
//Potência
atpl 70

set espaco 10

// Pacote para o placar de forma a seguir o formato das outras tramas
// Falta o tempo (O código é o mesmo raciocionio que os outros)
data plac "P" 45 52
data placar plac espaco

// Enviar ao placar quantos lugares se encontram livres (Na inicialização estão todos livres)
send placar 52

// Depois de 3 mensagens com os sensores, ocorre uma reserva (alterar este valor se quiser mais)
set reserva 3

// Vetor com os lugares, cada indice deste vetor representa o lugar
vec estacionamento 11

// Inicialização do vetor com tudo a 0 (estacionamento com todos os lugares livres)
for i 1 11
vset 0 estacionamento i
end

loop

receive rp
// Mensagem recebida no formato: Tipo da mensagem | id do sensor | id do gateway | Dados | Timestamp criação do pacote | Timestamp da envio do pacote
rdata rp type id idgateway v tpacote tenvio

//Tempo em que a mensagem foi recebida
time trecebido
set trecebido trecebido/0.0001
int tre trecebido
set trecebido tre/10

//Código para detetar colisões no gateway
//receive l 100
//if (l!="")
//cprint "Colisao!!!!"
//end

// Tempo de transmissão (Temos em falta o tamanho do pacote no cálculo)
set ttransmissao trecebido-tenvio

//Atraso da transmissão (Temos em falta o tamanho do pacote no cálculo)
set atraso trecebido-tpacote

// Se o lugar id foi ocupado
if (v==1)
//data p id "ocupado" tpacote tenvio trecebido
data p rp trecebido "ocupado"
vset 1 estacionamento id
set alterado id
set acao 1
dec espaco
end

// Se o carro saiu do lugar id
if (v==0)
//data p id "livre" tpacote tenvio trecebido
data p rp trecebido "livre"
vset 0 estacionamento id
set alterado id
set acao 0
inc espaco
end

//Depois da mensagem com o sensor decrementa a reserva
dec reserva

delay 10

//Print da mensagem da trama juntamente com o tempo de envio e uma string para identificar mais facilmente se foi ocupado ou livre
cprint p


cprint "Tempo de Transmissao: " ttransmissao
cprint "Atraso de Transmissao: " atraso

// Envio da contagem de espaços livres para o Placar
data placar plac espaco
send placar 52

// Após 3 mensagens é enviada uma reserva para um lugar vazio
if (reserva<=0)
// procurar o primeiro lugar vazio
set i 1
set x 1
while (i<11) && (x==1)
//cprint "i = " i
vget x estacionamento i
//cprint "x = " x
inc i
end

// O primeiro lugar livre é reservado
if(x==0)
time r
atget id idgateway
set lugar i-1
vset 1 estacionamento lugar
int alteradore lugar
data px "R" idgateway lugar 1 r

// Identificar qual nodo intermédio enviar
if (lugar<=5)
set nextnode 54
else
set nextnode 55
end

// Envio da mensagem de reserva
send px nextnode

cprint "O lugar: " lugar " foi reservado"
dec espaco

//Envio para o placar os espacos livres depois da reserva
data placar plac espaco
send placar 52

else

//Se após percorrermos o vetor do estacionamento, se x fica a 1 significa que o estacionamento está cheio
cprint "Estacionamento cheio"

end
//Reset da variável reserva
set reserva 3
end

if (alterado != 0)
printfile alterado ": " acao
set alterado 0
end
if (alteradore != 0)
printfile alteradore ": " 1
set alteradore 0
end
