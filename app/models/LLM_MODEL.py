import logging

from langchain_openai import ChatOpenAI

from app.config.env_utils import LLM_API_KEY, LLM_BASE_URL



class ModelInstances:
    try:
        query_llm = ChatOpenAI(
            model="qwen-turbo",
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            temperature=0.1
        )

        analyst_llm = ChatOpenAI(
            model="qwen-max",
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )

        html_llm = ChatOpenAI(
            model="qwen-max",
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )

        leader_llm = ChatOpenAI(
            model="qwen-max",
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )
    except Exception as e:
        logging.error(f"模型初始化失败: {str(e)}")
        raise


