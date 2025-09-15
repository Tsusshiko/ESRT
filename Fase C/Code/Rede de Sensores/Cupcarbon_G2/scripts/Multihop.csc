//Pot�ncia
atpl 65

loop
receive x
rdata x type id iddestino s t te

//Colis�o
//Funciona quase sempre exceto para casos especificos.
//Nomeadamente,quando ocorre colis�o e esta demora tanto tempo que h� uma reserva de um espa�o que j� se encontrava ocupado
//O que n�o deveria ser poss�vel, o gateway n�o teve conhecimento deste estar ocupado quando estava a efetuar a reserva

receive col 10
//Se houver colis�o
if (col!="")
data respum "C" id iddestino s t te
rdata col type idsegundo iddestino s t te
data respdois "C" idsegundo iddestino s t te
cprint "Colisao entre as mensagens de: " id "e" idsegundo "!"

//Com tratamento das colis�es (tirar estas duas linhas de envio de mensagem de coment�rio caso pretenda o tratamento de colis�es)
//Envio do aviso de colis�o para os dispositivos onde a sua mensagem sofreu colis�o
//send respum id
//send respdois idsegundo        

//Sem tratamento das colis�es (colocar estas duas linhas de envio de mensagem em coment�rio caso pretenda o tratamento de colis�es)
//Reencaminhamento para o destino, independente do facto de haver colis�o
send x iddestino
send col iddestino  

else

//Caso n�o haja colis�es , � feito um reencaminhamento para o destino , este tanto pode ser um sensor (downlink) ou o gateway, n�o h� distin��o
send x iddestino

end
delay 10