//Potência
atpl 65

loop
receive x
rdata x type id iddestino s t te

//Colisão
//Funciona quase sempre exceto para casos especificos.
//Nomeadamente,quando ocorre colisão e esta demora tanto tempo que há uma reserva de um espaço que já se encontrava ocupado
//O que não deveria ser possível, o gateway não teve conhecimento deste estar ocupado quando estava a efetuar a reserva

receive col 10
//Se houver colisão
if (col!="")
data respum "C" id iddestino s t te
rdata col type idsegundo iddestino s t te
data respdois "C" idsegundo iddestino s t te
cprint "Colisao entre as mensagens de: " id "e" idsegundo "!"

//Com tratamento das colisões (tirar estas duas linhas de envio de mensagem de comentário caso pretenda o tratamento de colisões)
//Envio do aviso de colisão para os dispositivos onde a sua mensagem sofreu colisão
//send respum id
//send respdois idsegundo        

//Sem tratamento das colisões (colocar estas duas linhas de envio de mensagem em comentário caso pretenda o tratamento de colisões)
//Reencaminhamento para o destino, independente do facto de haver colisão
send x iddestino
send col iddestino  

else

//Caso não haja colisões , é feito um reencaminhamento para o destino , este tanto pode ser um sensor (downlink) ou o gateway, não há distinção
send x iddestino

end
delay 10