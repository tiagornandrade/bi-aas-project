import logging
from services.account import AccountService
from services.audit import AuditService
from services.compliance import ComplianceService
from services.credit import CreditService
from services.entities import EntityService
from services.insurance import InsuranceService
from services.investments import PortfolioService
from services.lending import LoanService
from services.payment import TransactionService


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
    """Executa a inserção segura em um serviço, capturando e registrando erros."""
    function = getattr(service, function_name, None)
    if function is None or not callable(function):
        logging.error(
            f"Error: {function_name} not found or not callable in {service.__name__}"
        )
        return []

    try:
        result = function(count)
    except TypeError as e:
        logging.error(f"Type error executing {function_name}: {e}. Check arguments.")
        return []
    except Exception as e:
        logging.error(f"Error executing {function_name}: {e}")
        return []

    if isinstance(result, list) and not result:
        logging.warning(f"{function_name} did not insert any data.")
    elif result is None:
        logging.warning(f"{function_name} returned None. Verify insertion logic.")

    logging.info(f"{function_name} completed with result: {result}")
    return result or []


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
        (AccountService, "insert_users", 10000),
        (AccountService, "insert_accounts", 10000),
        (AccountService, "insert_subaccounts", 10000),
        (AuditService, "insert_audits", 10000),
        (ComplianceService, "insert_regulations", 10000),
        (ComplianceService, "insert_user_verification", 10000),
        (CreditService, "insert_credit_scores", 10000),
        (CreditService, "insert_risk_assessments", 10000),
        (EntityService, "insert_entities", 10000),
        (InsuranceService, "insert_policies", 10000),
        (InsuranceService, "insert_claims", 10000),
        (InsuranceService, "insert_insured_entities", 10000),
        (PortfolioService, "insert_portfolios", 10000),
        (LoanService, "insert_loans", 10000),
        (LoanService, "insert_payments", 10000),
        (TransactionService, "insert_transactions", 10000),
        (TransactionService, "insert_payment_methods", 10000),
        (TransactionService, "insert_merchants", 10000),
    ]

    for service, function_name, count in operations:
        logging.info(f"Iniciando {function_name}...")
        safe_insert(service, function_name, count)

    logging.info("Dados inseridos com sucesso!")


if __name__ == "__main__":
    main()
