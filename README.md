![Vinum Expo](/img/Logo.png)
### Sistema para controle de vales em degustações

### TODO (Requisitos)
- [x] Cadastro de expositores
- [x] Acerto de Comanda (Em parte)
	- [x] Travar comanda para não poder mais receber pedidos
	- [ ] Cobrar todas as comandas de um visitante
	- [ ] Travar todas as comandas de um visitante
- [x] Deduzir vales e adicionar mais 
	- [x] Adicionar (Em parte)
	- [x] Deduzir
- [x] Sistema de Tokens JWT(Autenticação)
- [x] Associar credenciais automaticamente no ato do cadastro

### Problemas a serem resolvidos
- [x] Gerenciamento de Sessão
- [ ] Repetição de requests

### Features futuras
- Emissão e análise de dados para os expositores
- Monitoramento em tempo real(Imagine uma tela dizendo quais são os expositores mais procurados no momento)
- Votação por parte dos visitantes do melhor vinho ou expositor

### Uso

#### Dependências Python
- json
- pymongo
- PyJWT
- datetime
- flask
- flask_api
- werkzeug

### Documentação da API

#### Gerar Token de Autorização(login)
- Método: POST
- Destino: /gen_auth
- Data: 
```json
{
	"user": "hahahahah@email.com",
	"hash" : "12123123" 
}
```
- Possíveis retornos
	- Status 201
		- Gera um token JWT que DEVE ser usado no HEADER de qualquer requisição ao servidor
		- Use a header "Jwt-Token"
		- Exemplo:
		```json
		{
			"token": "asdgd92d9gds2dgs298gds92gd27g"
		}
		```
	- Status 401
		- Erro: Acesso Proibido

#### Travar Comanda(após acerto)
- Autorização: adm
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
	- Status 401
		- Erro: Acesso Proibido

#### Requisitar acerto de contas
- Autorização: adm
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
	- Status 401
		- Erro: Acesso Proibido
	

#### Cobrar vale(degustação)
- Autorização: expo
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
	- Status 401
		- Erro: Acesso Proibido

#### Cadastro de Expositores
- Autorização: adm
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
	- Status 401
		- Erro: Acesso Proibido

##### Cadastro de Visitantes
- Autorização: adm
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
	- Status 401
		- Erro: Acesso Proibido
