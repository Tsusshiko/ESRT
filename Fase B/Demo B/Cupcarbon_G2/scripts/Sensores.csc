//Flag que serve para assegurar que só é enviada mensagem quando o sensor muda
set mudanca 0

//Potência
atpl 50

atget id id
set type "S"
set reserva 0
set iddestino 45

//Identificação do nodo intermédio que o sensor tem de enviar
//(Colocamos para evitar a criação de scripts novos com apenas esta diferença)
if (id<=5)
set nextnode 54
else
set nextnode 55
end

loop

//Leitura do sensor
dreadsensor s

// Quando não há uma reserva a luminosidade deste depende do que é lido no sensor
if (reserva == 0)
//Marca o que leu
mark s

// Se entrar um carro no lugar
if (s==1) && (mudanca==0)
    //Timestamp do pacote gerado
    time x
    set t x/0.0001
    int tg t
    set t tg/10
    data p type id iddestino s t
    
    randb atraso 5 20
    delay atraso

    //Timestamp do envio da mensagem
    time x
    set te x/0.0001
    int ten te
    set te ten/10
    data pacote p te

    // Envio da mensagem para o nodo intermédio
    send pacote nextnode
    set mudanca 1

end

//Se sair um carro do lugar
if (s==0) && (mudanca==1)
    //Timestamp do pacote gerado
    time x
    set t x/0.0001
    int tg t
    set t tg/10
    data p type id iddestino s t

    randb atraso 5 20
    delay atraso

    delay 10
    //Timestamp do envio da mensagem
    time x
    set te x/0.0001
    int ten te
    set te ten/10
    data pacote p te

    // Envio da mensagem para o nodo intermédio
    send pacote nextnode
    set mudanca 0

end

// end do if caso não haja reserva
end

// Receção de mensagens de Colisão ou de Reserva
receive x 10

// Se receber alguma coisa
if(x!="")
rdata x type id idgateway valor t

// Se a mensagem for sobre uma Reserva
if (type == "R")
mark valor
set reserva 1
end

// Se a mensagem for sobre uma Colisão
if (type == "C")
cprint x
randb backoff 11 50
delay backoff

//Reenvio da mensagem para o nodo intermédio.
send pacote nextnode

end
end
delay 100
