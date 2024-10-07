from scrapegraphai.graphs import SmartScraperGraph
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from src.husky_scraper_v3.utils import setup_logging

logger = setup_logging('../../logs/scraper.log')


def initialize_model(config, token):
    try:
        repo_id = config["huggingface"]["repo_id"]
        max_length = config["huggingface"]["model_max_length"]
        temperature = config["huggingface"]["temperature"]

        llm_model_instance = HuggingFaceEndpoint(
            repo_id=repo_id, max_length=max_length, temperature=temperature, token=token
        )
        logger.info(f"Initialized LLM model with repo_id: {repo_id}")

        embedder_model_instance = HuggingFaceInferenceAPIEmbeddings(
            api_key=token, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )
        logger.info(f"Initialized embedding model: sentence-transformers/all-MiniLM-l6-v2")

        return llm_model_instance, embedder_model_instance
    except Exception as e:
        logger.error(f"Error initializing models: {e}")
        raise


def run_smart_scraper(source_url, prompt, model_instance):
    try:
        logger.info(f"Starting scraper for URL: {source_url}")
        graph_config = {
            "llm": {"model_instance": model_instance, "model_tokens": 100000},
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source_url,
            config=graph_config
        )

        result = smart_scraper_graph.run()
        logger.info(f"Scraper successfully ran for {source_url}")
        return result
    except Exception as e:
        logger.error(f"Error running scraper for {source_url}: {e}")
        return None
