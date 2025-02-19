import logging
from services.account import AccountService
from services.audit import AuditService
from services.compliance import ComplianceService

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_sqlalchemy_obj(obj):
    """Remove metadados do SQLAlchemy para exibir apenas os atributos da tabela."""
    return {
        key: value
        for key, value in getattr(obj, "__dict__", {}).items()
        if not key.startswith("_")
    }


def safe_insert(service, function_name, count):
    """Executa operações de inserção de forma segura, capturando e logando erros."""
    try:
        return _extracted_from_safe_insert_4(service, function_name, count)
    except TypeError as e:
        logging.error(
            f"Erro de tipo ao executar {function_name}: {e}. Verifique se os argumentos são válidos."
        )
        return []
    except Exception as e:
        logging.error(f"Erro ao executar {function_name}: {str(e)}")
        return []


# TODO Rename this here and in `safe_insert`
def _extracted_from_safe_insert_4(service, function_name, count):
    function = getattr(service, function_name, None)
    if function is None or not callable(function):
        logging.error(
            f"Erro: {function_name} não encontrado ou não é uma função no serviço {service.__name__}"
        )
        return []

    result = function(count)

    if isinstance(result, list) and not result:
        logging.warning(f"{function_name} não inseriu nenhum dado.")

    elif result is None:
        logging.warning(
            f"{function_name} retornou None. Verifique a lógica de inserção."
        )

    logging.info(f"{function_name} concluído: {result}")
    return result or []


def main():
    operations = [
        (AccountService, "insert_users", 5),
        (AccountService, "insert_accounts", 5),
        (AccountService, "insert_subaccounts", 5),
        (AuditService, "insert_audits", 5),
        (ComplianceService, "insert_regulations", 5),
        (ComplianceService, "insert_user_verification", 5),
    ]

    for service, function_name, count in operations:
        logging.info(f"Iniciando {function_name}...")
        safe_insert(service, function_name, count)

    logging.info("Dados inseridos com sucesso!")


if __name__ == "__main__":
    main()
