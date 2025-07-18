
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
        messages = state['messages']
        human_message = HumanMessage(content=messages[-1].content)

        system_prompt = PromptLibrary().get_prompt('chat')

        # Retrieve top-k relevant chunks from vector DB for the user prompt
        try:
            retrieval_results = self.vector_db_connector.query(human_message.content, n_results=getattr(app_config.rag_knowledge, 'top_k', 4))
        except Exception as e:
            retrieval_results = {'documents': [], 'distances': [], 'document_ids': []}
        relevant_chunks = retrieval_results.get('documents', [])
        print(retrieval_results)

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

        response = self.llm.query(chat_history)
        ai_message = response

        # Append the AI response to the state and add sources
        state['messages'].append(ai_message)
        state['documents'] = relevant_chunks
        state['distances'] = retrieval_results.get('distances', [])
        state['document_ids'] = retrieval_results.get('document_ids', [])
        return state

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
        graph.add_node("chat", self.chat)
        graph.add_edge("chat", END)
        graph.set_entry_point("chat")
        return graph.compile()
