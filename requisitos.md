# Documento de requisitos

### Tela de login
- Campos
	- Email
	- Senha
- Após o login, redirecione o usuário para a tela de controle apropriada conforme a resposta do servidor
- O usuário manterá a sua sessão por meio de Cookies. Veja como podemos fazer

### Cadastro de Visitante
- Campos
	- Nome
	- CPF (Validar)
	- Data de Nascimento (Validar)
	- Cidade
- Quando você fizer o request para o servidor, você vai receber um Código de status HTTP, olhe na documentação e veja como você vai lidar com os erros e tal
- Caso o cadastro for concluido com sucesso, mostre na tela o número da comanda gerada

### Cadastro do Expositor
- Campos
	- Empresa/Expositor
	- CPF (Validar)
	- Cidade
	- Email (Validar)
	- Senha
		- A senha DEVE passar por um hash SHA256 e ser codificada para HEXADECIMAL. NÂO envie para o servidor senhas, SOMENTE AS HASHES.

### Tela de controle do expositor
- Deve ter um botão para abrir a câmera e começar a ler o Código QR
	- Após ler com sucesso, o servidor vai conferir se há vales disponíveis para serem gastos, caso existirem, apenas mostre uma caixa dizendo "Vale deduzido!"
		- Caso não existirem mais vales, após a leitura, mostre uma caixa perguntando quantos vales o visitante quer a mais e um botão para confirmar.
		- Olhe na documentação para as possíveis respostas do servidor
- Abaixo desse botão haverá um campo para inserir o número da comanda manualmente, caso haja erro na leitura do código e do lado um botão para confirmar, trate as respostas do servidor da mesma forma do que com o código
- Abaixo desse botão coloque um contador de visitantes no estande
	- Só é atualizado quando atualiza a página para poupar I/O do servidor

### Tela de Controle da Administração
- Botão para redirecionar para a tela de Cadastro do visitante
- Botão para redirecionar para a tela de Cadastro do expositor
- Botão para consultar a situação da comanda ou do visitante através do CPF
- Dentro dessa tela haverá um botão para fechar a comanda
	- Apertando nesse botão será mostrado o preço da comanda e o visitante responsável
- Botão para adicionar vales em certa comanda
	- Veja como o expositor faz para adicionar vales, é a mesma coisa

