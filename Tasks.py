# Funções para cadastro de usuários

def cadastrar_usuario():
    with open("usuario.txt", "a") as file:
        nome_usuario = input("Digite seu nome de usuário: ")
        senha = input("Digite sua senha: ")
        
        file.write(f"{nome_usuario},{senha},0\n")  # Salva com 0 pontos iniciais
        print("Usuário cadastrado com sucesso!")

def login_usuario():
    nome_usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    with open("usuario.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == nome_usuario and data[1] == senha:
                print("Login realizado com sucesso!")
                return {"nome_usuario": nome_usuario, "pontos": int(data[2])}

    print("Usuário ou senha incorretos.")
    return None

def atualizar_pontos_usuario(usuario, pontos):
    lines = []
    with open("usuario.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == usuario["nome_usuario"]:
                data[2] = str(usuario["pontos"] + pontos)
            lines.append(",".join(data) + "\n")
    
    with open("usuario.txt", "w") as file:
        file.writelines(lines)
    print(f"{pontos} pontos adicionados! Total: {usuario['pontos'] + pontos} pontos.")

# Funções CRUD para tarefas

def criar_tarefa():
    with open("tasks.txt", "a") as file:
        titulo = input("Digite o título da tarefa: ")
        descricao = input("Digite a descrição da tarefa: ")
        pontos = input("Digite os pontos atribuídos a essa tarefa: ")
        file.write(f"{titulo},{descricao},{pontos},False\n")
    print("Tarefa criada com sucesso!")

def listar_tarefas():
    try:
        with open("tasks.txt", "r") as file:
            tarefas = file.readlines()
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                for index, line in enumerate(tarefas, start=1):
                    data = line.strip().split(",")
                    status = "Concluída" if data[3] == "True" else "Pendente"
                    print(f"ID: {index} | Título: {data[0]} | Pontos: {data[2]} | Status: {status}")
    except FileNotFoundError:
        print("Nenhuma tarefa cadastrada.")

def atualizar_tarefa():
    listar_tarefas()
    tarefa_id = int(input("Digite o ID da tarefa que deseja atualizar: ")) - 1
    
    with open("tasks.txt", "r") as file:
        tarefas = file.readlines()

    if 0 <= tarefa_id < len(tarefas):
        titulo = input("Digite o novo título da tarefa: ")
        descricao = input("Digite a nova descrição da tarefa: ")
        pontos = input("Digite os novos pontos da tarefa: ")
        tarefas[tarefa_id] = f"{titulo},{descricao},{pontos},False\n"
        
        with open("tasks.txt", "w") as file:
            file.writelines(tarefas)
        print("Tarefa atualizada com sucesso!")
    else:
        print("Tarefa não encontrada.")

def deletar_tarefa():
    listar_tarefas()
    tarefa_id = int(input("Digite o ID da tarefa que deseja deletar: ")) - 1

    with open("tasks.txt", "r") as file:
        tarefas = file.readlines()

    if 0 <= tarefa_id < len(tarefas):
        del tarefas[tarefa_id]
        
        with open("tasks.txt", "w") as file:
            file.writelines(tarefas)
        print("Tarefa deletada com sucesso!")
    else:
        print("Tarefa não encontrada.")

def concluir_tarefa(usuario):
    listar_tarefas()
    tarefa_id = int(input("Digite o ID da tarefa que deseja marcar como concluída: ")) - 1

    with open("tasks.txt", "r") as file:
        tarefas = file.readlines()

    if 0 <= tarefa_id < len(tarefas):
        tarefa_data = tarefas[tarefa_id].strip().split(",")
        if tarefa_data[3] == "False":  # Se a tarefa ainda não foi concluída
            tarefa_data[3] = "True"
            tarefas[tarefa_id] = ",".join(tarefa_data) + "\n"
            pontos = int(tarefa_data[2])
            usuario["pontos"] += pontos
            atualizar_pontos_usuario(usuario, pontos)
            print(f"Parabéns! Tarefa concluída. Você ganhou {pontos} pontos.")
            
            with open("tasks.txt", "w") as file:
                file.writelines(tarefas)
        else:
            print("Tarefa já concluída.")
    else:
        print("Tarefa não encontrada.")

# Função principal e menu do sistema

def main():
    print("Bem-vindo a TASK'Z, um Gerenciador de Tarefas Gamificado!")
    while True:
        print("\nDigite 1: para Cadastrar Usuário")
        print("Digite 2: para Login")
        print("Digite 3: para Sair")
        opcao = input("Digite uma opção: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario = login_usuario()
            if usuario:
                while True:
                    print("\n--- Lista de Tarefas ---")
                    print("Digite 1: para Criar Tarefa")
                    print("Digite 2: para Listar Tarefas")
                    print("Digite 3: para Atualizar Tarefa")
                    print("Digite 4: para Deletar Tarefa")
                    print("Digite 5: para Concluir Tarefa")
                    print("Digite 6: para Sair do menu principal")
                    
                    opcao = input("Escolha uma opção: ")
                    
                    if opcao == "1":
                        criar_tarefa()
                    elif opcao == "2":
                        listar_tarefas()
                    elif opcao == "3":
                        atualizar_tarefa()
                    elif opcao == "4":
                        deletar_tarefa()
                    elif opcao == "5":
                        concluir_tarefa(usuario)
                    elif opcao == "6":
                        print("Saindo para o menu principal...")
                        break
                    else:
                        print("Opção inválida.")
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
