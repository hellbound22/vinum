![Vinum Expo](/img/Logo.png)
### Sistema para controle de vales em exposições 

### TODO (Requisitos)
- [x] Cadastro de expositores
- [x] Acerto de Comanda (Em parte)
	- [x] Travar comanda para não poder mais receber pedidos
	- [ ] Travar todas as comandas de um visitante
- [x] Deduzir vales e adicionar mais 
	- [x] Adicionar (Em parte)
	- [x] Deduzir
- [ ] Sistema de login (Provavelmente fica para a parte do Danrlei)
- [ ] Manter histórico das transações com Timestamp

### Problemas a serem resolvidos
- [ ] Gerenciamento de Sessão
- [ ] Repetição de requests

### Features futuras
- Emissão e análise de dados para os expositores
- Monitoramento em tempo real(Imagine uma tela dizendo quais são os expositores mais procurados no momento)
- Votação por parte dos visitantes do melhor vinho ou expositor

### Documentação da API

#### Travar Comanda(após acerto)
- Método: POST
- Destino: /controle/trancar
- Data: 
```json
{
	"comanda": 2,
	"cpf_acossiado" : 12123123 
}
```
- Possíveis retornos
	- Status 406
		- Erro: Dados Incompletos
		- Erro: CPF não corresponde ao dono da comanda
	- Status 404
		- Erro: Impossível achar comanda 
	- Status 200
		- Ok, Sucesso
	- Status 500
		- Erro Interno do Servidor 

#### Requisitar acerto de contas
- Método: GET 
- Destino: /controle/acerto/'''comanda'''
	- Onde '''comanda''' é o número da comanda a ser consultada
- Possíveis retornos
	- Status 406
		- Erro: Impossível achar comanda com esse número 
	- Status 200
		- Ok
		- Retorna dados em json com a seguinte estrutura
		```json
		{
			"dono": 12123123,
			"nmr_tickets": 8,
			"preco_final": 25
		}
		```
	- Status 500 
		- Erro Interno do servidor 

#### Cobrar vale(degustação)
- Método: POST
- Destino: /expositor/cobrar
- Data: 
```json
{
	"comanda": 2,
	"qnt": 1,
	"cpf_expositor" : 12123123, 
	"sessao": "d87as5da7d5sasd8a8sd6a8sd56a85sd"
}
```
- Possíveis retornos
	- Status 406
		- Erro: Informações Incompletas
	- Status 200
		- Ok, Sucesso
	- Status 500
		- Erro Interno do Servidor 

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
