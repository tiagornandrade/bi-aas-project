from services.account import AccountService


def clean_sqlalchemy_obj(obj):
    """Remove metadados do SQLAlchemy para exibir apenas os atributos da tabela"""
    return {key: value for key, value in obj.__dict__.items() if not key.startswith("_")}

if __name__ == "__main__":

    print("Inserindo usuários...")
    users = AccountService.insert_users(5)

    print("Inserindo contas...")
    accounts = AccountService.insert_accounts(5)

    print("Inserindo subcontas...")
    subaccounts = AccountService.insert_subaccounts(5)

    print("Dados inseridos com sucesso!")
