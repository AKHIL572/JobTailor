import pytest

from app.core.llm_client import LLMClient


class ModelNotFoundError(Exception):
    status_code = 404


class MissingModelCompletions:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        raise ModelNotFoundError("model not found")


class MissingModelAPI:
    def __init__(self):
        self.chat = self
        self.completions = MissingModelCompletions()


def make_client():
    client = LLMClient.__new__(LLMClient)
    client.provider = "ollama"
    client.model = "llama3.1:8b"
    client.temperature = 0.3
    client.max_retries = 3
    client.log_records = []
    client._client = MissingModelAPI()
    return client


def test_missing_ollama_model_fails_without_retries():
    client = make_client()

    with pytest.raises(RuntimeError, match="ollama pull llama3.1:8b"):
        client.chat("job_analysis", [{"role": "user", "content": "Analyze this job"}])

    assert client._client.completions.calls == 1
    assert client.log_records[0].attempts == 1


def test_connection_test_explains_missing_ollama_model():
    client = make_client()

    ok, message = client.test_connection()

    assert not ok
    assert "ollama pull llama3.1:8b" in message
