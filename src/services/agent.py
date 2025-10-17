"""
AI Agent Module using LangChain and Google Gemini
Handles intelligent conversation and tool calling for the travel assistant
"""
from typing import Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.config import settings
from src.services.tools import tools
import logging

logger = logging.getLogger(__name__)


# System prompt for the travel assistant
SYSTEM_PROMPT = """You are an expert AI travel assistant for GoTravel, a travel booking platform. 
Your role is to help users discover and book travel packages, hotels, and tourist destinations.

## Your Capabilities:
1. **Search Hotels**: Find accommodations based on location, rating, and preferences
2. **Search Packages**: Discover travel packages by destination, category, price, and duration
3. **Search Places**: Help users find tourist attractions and places to visit
4. **Weather Information**: Provide current weather information for any city
5. **Create Bookings**: Assist users in booking packages and hotels

## Guidelines:
- Be friendly, helpful, and conversational
- When users ask about availability, always use the appropriate search tools
- Present information in a clear, organized manner
- When multiple options are available, highlight the best matches first
- For booking requests, ensure you collect all necessary information (name, email, phone, number of participants)
- If a tool returns no results, suggest alternatives or ask clarifying questions
- Provide specific details like prices, ratings, and locations when available
- Use natural language and avoid technical jargon
- When mentioning prices, always include the currency
- If asked about weather, provide a comprehensive summary including temperature, conditions, and recommendations

## Important:
- Always use tools to fetch real-time data instead of making assumptions
- When booking, confirm all details with the user before proceeding
- Be transparent about pricing and what's included in packages
- Suggest popular destinations when users are unsure
- Format numbers and dates clearly (e.g., "BDT 15,000" not "15000.0")

## Response Style:
- Use bullet points for listing multiple items
- Include emojis occasionally to make responses more engaging (🏨 🌴 ✈️ ⭐ 🌤️)
- Keep responses concise but informative
- Always end with a helpful follow-up question or suggestion

Remember: Your goal is to make travel planning easy, enjoyable, and efficient for users!"""


class TravelAgent:
    """Main AI Agent for travel assistance"""
    
    def __init__(self):
        """Initialize the travel agent with LLM and tools"""
        
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            google_api_key=settings.google_api_key
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        # Store for chat histories (in production, use Redis or database)
        self.chat_histories: Dict[str, InMemoryChatMessageHistory] = {}
    
    def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = InMemoryChatMessageHistory()
        return self.chat_histories[session_id]
    
    async def process_message(
        self,
        message: str,
        session_id: str = "default",
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response
        
        Args:
            message: User's input message
            session_id: Session identifier for maintaining conversation history
            user_context: Optional context about the user (id, preferences, etc.)
        
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            logger.info(f"Processing message for session {session_id}: {message}")
            
            # Get chat history
            chat_history = self.get_chat_history(session_id)
            
            # Prepare the agent with history
            agent_with_history = RunnableWithMessageHistory(
                self.agent_executor,
                lambda session_id: self.get_chat_history(session_id),
                input_messages_key="input",
                history_messages_key="chat_history",
            )
            
            # Invoke the agent
            result = await agent_with_history.ainvoke(
                {"input": message},
                config={"configurable": {"session_id": session_id}}
            )
            
            # Extract response
            response_text = result.get("output", "I'm sorry, I couldn't generate a response.")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Log tool calls
            tools_used = []
            for step in intermediate_steps:
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    tools_used.append({
                        "tool": action.tool,
                        "input": action.tool_input,
                    })
            
            logger.info(f"Tools used: {[t['tool'] for t in tools_used]}")
            
            return {
                "success": True,
                "response": response_text,
                "session_id": session_id,
                "tools_used": tools_used,
                "message_count": len(chat_history.messages)
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return {
                "success": False,
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "error": str(e),
                "session_id": session_id
            }
    
    def clear_history(self, session_id: str) -> bool:
        """Clear chat history for a session"""
        if session_id in self.chat_histories:
            self.chat_histories[session_id].clear()
            return True
        return False
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about a chat session"""
        if session_id not in self.chat_histories:
            return {
                "exists": False,
                "message_count": 0
            }
        
        history = self.chat_histories[session_id]
        return {
            "exists": True,
            "message_count": len(history.messages),
            "session_id": session_id
        }


# Create a global agent instance
travel_agent = TravelAgent()


# Convenience function for quick testing
async def chat(message: str, session_id: str = "test") -> str:
    """Quick function to chat with the agent"""
    result = await travel_agent.process_message(message, session_id)
    return result.get("response", "Error occurred")


if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        """Test the agent with sample queries"""
        print("🤖 GoTravel AI Assistant - Test Mode\n")
        
        # Test queries
        queries = [
            "Show me hotels in Dhaka",
            "What are the cheapest travel packages?",
            "What's the weather in Cox's Bazar?",
            "Find popular tourist places in Bangladesh"
        ]
        
        for query in queries:
            print(f"\n👤 User: {query}")
            response = await chat(query, session_id="test")
            print(f"🤖 Assistant: {response}\n")
            print("-" * 80)
    
    # Run test
    asyncio.run(test_agent())
