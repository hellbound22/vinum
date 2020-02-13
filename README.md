# Vinum Server
### Sistema para controle de vales em exposições 

### Documentação da API

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
	- Status 201
		- Visitante cadastrado com sucesso
		- Retorna JSON com o numero da comanda emitida
	- Status 500
		- Erro Interno do Servidor
