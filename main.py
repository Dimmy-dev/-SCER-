from db import criar_tabela, Adicionar_especie, mostrar_especies, grau_de_risco, buscar_por_id, delet_usuario

def menu():
    criar_tabela()
    while True:
        print("\n === Cadastro de Espécie em Risco ===")
        print("1 - Adicionar nova espécie")
        print("2 - Listar todas as espécies")
        print("3 - Listar espécies por grau de ameaça")
        print("4 - Buscar espécie por ID")
        print("5 - Deletar espécie por ID")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            Adicionar_especie()
        elif escolha == "2":
            mostrar_especies()
        elif escolha == "3":
            grau_de_risco()
        elif escolha == "4":
            buscar_por_id()
        elif escolha == "5":
            delet_usuario()
        elif escolha == "0":
            print("encerrando...")
            break
        else:
            print("Coloque uma opção válida.")

if __name__ == "__main__":
    menu()