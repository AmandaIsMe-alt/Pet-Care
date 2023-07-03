# Pet Care

Uma API que permitisse um PetShop ter um maior controle e organização dos dados dos animais de sua gama de clientes.

Tecnologias utilizadas:

 - Python
 - Django

  ## **Devs**

 > - [Amanda R. Costa](https://www.linkedin.com/in/amanda-fullstack/)

 ---

 ## **Start the project:**
 ### Type the command in the terminal:

```json
  Criar Ambiente Venv : python -m venv venv
  
  Ativar Ambiente Venv : source venv/Scripts/activate -> para Windows // source venv/bin/activate -> para Linux
  
  Instalar Pacotes : pip install -r requirements.txt

  Preencher informações sensíveis no arquivo ENV
  
  Gerar Migrações : python manage.py migrate
  
  Iniciar Servidor : python manage.py runserver
 ```


## Modo de usar pelo insomnia:
---

## **Usuário**

## 1. Cadastro

- POST api/pets/
- Cadastrar pet

Request:
```json
{
	"name": "teste",
	"age": "2",
	"weight": "2.3",
	"sex": "Male",
	"group": "Dog",
	"traits": "whatever"
}
```
---
 ## 2. Listar

- GET api/pets/
- Listar seleções
---
 ## 3. Filtrar

- GET api/pets/:id/
- Filtragem de pet
---
 ## 4. Atualizar

- PATCH api/pets/:id/
- Atualização de pet
---
 ## 5. Deletar

- DELETE api/pets/:id/
- Deleção de pet
---
