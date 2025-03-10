import logging
import time
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
        logging.error(f"❌ {function_name} não encontrado em {service.__name__}")
        return []

    try:
        result = function(count)
    except TypeError as e:
        logging.error(
            f"❌ Erro de tipo em {function_name}: {e}. Verifique os argumentos."
        )
        return []
    except Exception as e:
        logging.error(f"❌ Erro ao executar {function_name}: {e}")
        return []

    if isinstance(result, list) and not result:
        logging.warning(f"⚠️ {function_name} não inseriu nenhum dado.")
    elif result is None:
        logging.warning(
            f"⚠️ {function_name} retornou None. Verifique a lógica de inserção."
        )
    else:
        logging.info(f"✅ {function_name} inseriu {len(result)} registros.")

    return result or []


def main():
    """Executa a inserção de dados continuamente."""
    operations = [
        (AccountService, "insert_users", 2000),
        (AccountService, "insert_accounts", 2000),
        (AccountService, "insert_subaccounts", 2000),
        (AuditService, "insert_audits", 2000),
        (ComplianceService, "insert_regulations", 2000),
        (ComplianceService, "insert_user_verification", 2000),
        (CreditService, "insert_credit_scores", 2000),
        (CreditService, "insert_risk_assessments", 2000),
        (EntityService, "insert_entities", 2000),
        (InsuranceService, "insert_policies", 2000),
        (InsuranceService, "insert_claims", 2000),
        (InsuranceService, "insert_insured_entities", 2000),
        (PortfolioService, "insert_portfolios", 2000),
        (LoanService, "insert_loans", 2000),
        (LoanService, "insert_payments", 2000),
        (TransactionService, "insert_transactions", 2000),
        (TransactionService, "insert_payment_methods", 2000),
        (TransactionService, "insert_merchants", 2000),
    ]

    while True:
        try:
            logging.info("🔄 Iniciando novo ciclo de inserção de dados...")

            for service, function_name, count in operations:
                logging.info(f"▶️ Executando {function_name}...")
                safe_insert(service, function_name, count)

            logging.info(
                "✅ Todos os dados foram inseridos. Aguardando 5 segundos antes do próximo ciclo...\n"
            )
        except Exception as e:
            logging.error(f"❌ Erro durante o ciclo de inserção: {e}")

        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("🛑 Execução interrompida pelo usuário.")
