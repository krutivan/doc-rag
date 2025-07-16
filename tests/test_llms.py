import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.llms.llm_open_ai import LLMOpenAI
from src.llms.llm_anthropic import LLMAnthropic
from src.llms.llm_model_type import LLMModelType

class DummyLLM:
    def __init__(self):
        self.invoked = False
    def invoke(self, messages):
        self.invoked = True
        return "dummy response"

def test_llm_openai_monkeypatch(monkeypatch):
    # Patch ChatOpenAI in LLMOpenAI to use DummyLLM
    from src.llms import llm_open_ai
    monkeypatch.setattr(llm_open_ai, "ChatOpenAI", lambda *a, **kw: DummyLLM())
    llm = LLMOpenAI("gpt-4o", api_key="fake")
    response = llm.query(["Hello"], "Test prompt")
    assert response == "dummy response"


def test_llm_anthropic_monkeypatch(monkeypatch):
    # Patch ChatAnthropic in LLMAnthropic to use DummyLLM
    from src.llms import llm_anthropic
    monkeypatch.setattr(llm_anthropic, "ChatAnthropic", lambda *a, **kw: DummyLLM())
    llm = LLMAnthropic("claude-3-sonnet", api_key="fake")
    response = llm.query(["Hello"], "Test prompt")
    assert response == "dummy response"


def test_llm_factory(monkeypatch):
    from src.llms.llm_factory import LLMFactory
    from src.llms.llm_model_type import LLMModelType
    # Patch both LLMs
    from src.llms import llm_open_ai, llm_anthropic
    monkeypatch.setattr(llm_open_ai, "ChatOpenAI", lambda *a, **kw: DummyLLM())
    monkeypatch.setattr(llm_anthropic, "ChatAnthropic", lambda *a, **kw: DummyLLM())
    openai_llm = LLMFactory.create_llm(LLMModelType.OPENAI, "gpt-4o", api_key="fake")
    anthropic_llm = LLMFactory.create_llm(LLMModelType.ANTHROPIC, "claude-3-sonnet", api_key="fake")
    assert openai_llm.query(["hi"], "prompt") == "dummy response"
    assert anthropic_llm.query(["hi"], "prompt") == "dummy response"
