
from typing import List

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from src.prompts.prompt_library import PromptLibrary
from src.core.config.config_reader import app_config
from src.llms.llm_factory import LLMFactory
from src.rag.vector_db_connector.vector_db_connector_factory import VectorDBConnectorFactory
from src.agents.base_chat_agent import BaseChatAgent
from src.agents.chat_agent_state import AgentState

class ChatAgent(BaseChatAgent):
    def __init__(self):
        
        self.llm = self._get_llm_via_config()
        self.vector_db_connector = self._get_vector_db_via_config()
        self.graph = self._build_graph()

    def chat(self, state: AgentState) -> AgentState:
        system_prompt = PromptLibrary().get_prompt('chat')
        chat_history = self._get_chat_history_with_context(state, system_prompt)
        response = self.llm.query(chat_history)
        ai_message = response

        # Append the AI response to the state and add sources
        state['messages'].append(ai_message)
        return state

    def retrieve(self, state: AgentState) -> AgentState:
        
        human_message = HumanMessage(content=state['messages'][-1].content)
        try:
            retrieval_results = self.vector_db_connector.query(human_message.content, n_results=getattr(app_config.rag_knowledge, 'top_k', 1))
        except Exception as e:
            retrieval_results = {'documents': [], 'distances': [], 'document_ids': []}
        state['documents'] = retrieval_results.get('documents', [])
        state['distances'] = retrieval_results.get('distances', [])
        state['document_ids'] = retrieval_results.get('document_ids', [])
        return state

    def generate_followup(self, state: AgentState) -> AgentState:
        system_prompt = PromptLibrary().get_prompt('follow_up')
        chat_history = self._get_chat_history_with_context(state, system_prompt)
        response = self.llm.query(chat_history)
        state['follow_up_questions'] = response.content
        return state

    def _get_chat_history_with_context(self, state: AgentState, system_prompt: str):
        messages = state['messages']
        relevant_chunks = state['documents']
        # Combine retrieved context into a string (simple join, can be improved)
        context = '\n---\n'.join(relevant_chunks) if relevant_chunks else ''
        # Optionally, you could inject this context into the system prompt or as a separate message
        if context:
            chat_history = [
                SystemMessage(content=system_prompt + "\n\nContext:\n" + context),
            ] + messages
        else:
            chat_history = [
                SystemMessage(content=system_prompt),
            ] + messages
        return chat_history

    def _get_llm_via_config(self):
        chat_llm_cfg = app_config.chat.selected_llm
        return LLMFactory.create_llm(
            model_type=chat_llm_cfg.type,
            model_name=chat_llm_cfg.model_name,
            api_key=chat_llm_cfg.api_key
        )
    
    def _get_vector_db_via_config(self):
        rag_knowledge_cfg = app_config.rag_knowledge
        db_name = getattr(rag_knowledge_cfg.vector_db, 'type', None).name.lower()
        return VectorDBConnectorFactory.create(db_name, rag_knowledge_cfg.vector_db)

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("retrieve", self.retrieve)
        graph.add_node("chat", self.chat)
        graph.add_edge("retrieve", "chat")
        if getattr(app_config.chat, "generate_followup", False):
            graph.add_node("generate_followup", self.generate_followup)
            graph.add_edge("chat", "generate_followup")
            graph.add_edge("generate_followup", END)
        else:
            graph.add_edge("chat", END)
        graph.set_entry_point("retrieve")
        return graph.compile()
