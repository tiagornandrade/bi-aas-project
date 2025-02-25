from flask import Flask, request, jsonify
import pyarrow.dataset as ds
import datafusion

app = Flask(__name__)

ctx = datafusion.ExecutionContext()

GCS_GOLD_LAYER = "gs://bi-aas-project-gold/"

ctx.register_parquet("gold_data", GCS_GOLD_LAYER)


@app.route("/query", methods=["POST"])
def run_query():
    """
    Endpoint para executar queries SQL sobre os dados da camada Gold.
    """
    query = request.json.get("query")

    if not query:
        return jsonify({"error": "Query não fornecida"}), 400

    try:
        result = ctx.sql(query).to_pandas()
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
