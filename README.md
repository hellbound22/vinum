![Vinum Expo](/img/Logo.png)
### Sistema para controle de vales em exposições 

### TODO (Requisitos)
- [x] Cadastro de expositores
- [ ] Acerto de Comanda
- [ ] Deduzir vales e adicionar mais conforme os Expositores ou os Operadores necessitarem
- [ ] Sistema de login (Provavelmente fica para a parte do Danrlei)
- [ ] Manter histórico das transações com Timestamp

### Documentação da API

#### Cadastro de Expositores

- Método: POST
- Destino: /cadastro_expositor
- Data: 
```json
{
	"expositor" : "Vinho Derruba", 
	"cpf" : 12123123, 
	"cidade" : "Aroio",
	"email": "vinhoderruba@nosec.com.br",
	"hash": "d87as5da7d5sasd8a8sd6a8sd56a85sd"
}
```
- Possíveis retornos
	- Status 409
		- Conflito: CPF já cadastrado
	- Status 406
		- Cadastro Incompleto
	- Status 201
		- Expositor cadastrado com sucesso
	- Status 500
		- Erro Interno do Servidor

##### Cadastro de Visitantes

- Método: POST
- Destino: /cadastro_visitante
- Data: 
```json
{
	"nome" : "Rodrigo", 
	"cpf" : 12123123, 
	"nascimento" : "16/06/1999", 
	"cidade" : "Lebon Régis"
}
```
- Possíveis retornos
	- Status 409
		- Conflito: CPF já cadastrado
	- Status 406
		- Cadastro Incompleto
	- Status 201
		- Visitante cadastrado com sucesso
		- Retorna JSON com o numero da comanda emitida: 
		```json
			{ "nmr_comanda": 4 }
		```
	- Status 500
		- Erro Interno do Servidor
