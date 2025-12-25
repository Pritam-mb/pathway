"""
Bio-Watcher Agent - Agentic Clinical Intelligence
Uses LangGraph for multi-step reasoning and tool orchestration.
"""
from typing import Annotated, TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
import json
from datetime import datetime


# Agent State
class AgentState(TypedDict):
    """State maintained across agent execution"""
    messages: List[HumanMessage | AIMessage | SystemMessage]
    current_task: str
    retrieved_docs: List[Dict]
    safety_score: int
    alerts: List[Dict]
    reasoning_trace: List[str]


# Tools for the Agent
@tool
def pathway_retriever(query: str) -> str:
    """
    Retrieve relevant medical documents from the live Pathway index.
    Includes both internal hospital docs and external alerts.
    """
    from backend.pathway_engine.retriever import PathwayRetriever
    
    retriever = PathwayRetriever()
    results = retriever.retrieve(query, top_k=5)
    
    if not results:
        return "No relevant documents found."
    
    # Format results
    formatted = []
    for i, doc in enumerate(results):
        text = doc.get('text', '')[:300]
        source = doc.get('metadata', {}).get('source_type', 'unknown')
        formatted.append(f"[{i+1}] Source: {source}\n{text}...")
    
    return "\n\n".join(formatted)


@tool
def safety_auditor(drug_name: str) -> str:
    """
    Cross-reference a drug name with internal patient records.
    Identifies patients currently prescribed the specified medication.
    """
    from backend.pathway_engine.retriever import PathwayRetriever
    
    retriever = PathwayRetriever()
    
    # Search internal documents only
    query = f"patient prescribed {drug_name} medication prescription"
    results = retriever.retrieve_by_source(query, source_type="internal", top_k=10)
    
    if not results:
        return f"No patients currently prescribed {drug_name}."
    
    # Extract patient references
    patients = []
    for doc in results:
        text = doc.get('text', '')
        # Simple pattern matching - in production use NER
        if drug_name.lower() in text.lower():
            patients.append(text[:200])
    
    if not patients:
        return f"No active prescriptions for {drug_name} found."
    
    return f"Found {len(patients)} patient(s) prescribed {drug_name}:\n\n" + "\n---\n".join(patients)


@tool
def calculate_safety_score(findings: str) -> int:
    """
    Calculate overall safety score based on current findings.
    Returns score from 0-100.
    """
    # Simple heuristic - in production use more sophisticated logic
    critical_keywords = ['warning', 'urgent', 'critical', 'danger', 'risk', 'adverse']
    
    score = 95  # Start with high score
    
    findings_lower = findings.lower()
    for keyword in critical_keywords:
        if keyword in findings_lower:
            score -= 10
    
    return max(0, min(100, score))


@tool
def generate_alert(severity: str, title: str, description: str) -> Dict:
    """
    Generate a structured alert for the dashboard.
    """
    alert = {
        "id": datetime.now().timestamp(),
        "timestamp": datetime.now().isoformat(),
        "severity": severity,  # 'info', 'warning', 'critical'
        "title": title,
        "description": description,
        "acknowledged": False
    }
    
    # In production, this would publish to a message queue or WebSocket
    print(f"🚨 Alert Generated: [{severity.upper()}] {title}")
    
    return alert


# Agent Node Functions
def should_continue(state: AgentState) -> str:
    """Decide if agent should continue reasoning"""
    if len(state["reasoning_trace"]) > 10:
        return "end"
    
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and not last_message.tool_calls:
        return "end"
    
    return "continue"


def call_model(state: AgentState) -> AgentState:
    """Call LLM with current state"""
    from config.settings import settings
    
    llm = ChatGoogleGenerativeAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        google_api_key=settings.gemini_api_key
    )
    
    # Bind tools to LLM
    tools = [pathway_retriever, safety_auditor, calculate_safety_score, generate_alert]
    llm_with_tools = llm.bind_tools(tools)
    
    # Add system prompt
    system_prompt = SystemMessage(content="""You are a Clinical Sentinel AI, monitoring medical safety in real-time.

Your responsibilities:
1. Monitor for new external alerts (FDA, WHO) and internal hospital documents
2. Cross-reference drug safety warnings with patient records
3. Calculate risk scores and generate alerts when patterns are detected
4. Provide clear reasoning traces for medical audit compliance

When you detect a safety concern:
- Use pathway_retriever to get relevant context
- Use safety_auditor to check patient impact
- Use calculate_safety_score to quantify risk
- Use generate_alert to notify clinical staff

Always explain your reasoning step-by-step.""")
    
    messages = [system_prompt] + state["messages"]
    
    # Call LLM
    response = llm_with_tools.invoke(messages)
    
    # Add reasoning trace
    reasoning = f"[{datetime.now().strftime('%H:%M:%S')}] Agent reasoning: {response.content[:100]}..."
    state["reasoning_trace"].append(reasoning)
    
    return {
        **state,
        "messages": state["messages"] + [response]
    }


# Build the Agent Graph
def create_agent():
    """Create the LangGraph agent"""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode([pathway_retriever, safety_auditor, calculate_safety_score, generate_alert]))
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


# Main Agent Runner
class BioWatcherAgent:
    """High-level agent interface"""
    
    def __init__(self):
        self.graph = create_agent()
        self.state = {
            "messages": [],
            "current_task": "",
            "retrieved_docs": [],
            "safety_score": 95,
            "alerts": [],
            "reasoning_trace": []
        }
    
    def process_event(self, event_type: str, event_data: Dict):
        """
        Process a data change event from Pathway.
        
        Args:
            event_type: 'new_doc', 'doc_updated', 'web_delta'
            event_data: Details of the change
        """
        print(f"\n{'='*60}")
        print(f"⚡ Event Detected: {event_type}")
        print(f"{'='*60}")
        
        # Create initial message
        message = HumanMessage(content=f"""
A new data change has been detected:

Event Type: {event_type}
Event Data: {json.dumps(event_data, indent=2)}

Please analyze this change and determine if any action is needed:
1. Retrieve relevant context from the knowledge base
2. Check for patient safety implications
3. Calculate updated safety score
4. Generate alerts if necessary
""")
        
        # Run the agent
        self.state["messages"] = [message]
        self.state["current_task"] = f"Processing {event_type} event"
        
        result = self.graph.invoke(self.state)
        
        # Display results
        print("\n📊 Agent Analysis Complete:")
        print(f"Safety Score: {result.get('safety_score', 'N/A')}")
        print(f"\nReasoning Trace:")
        for trace in result.get('reasoning_trace', []):
            print(f"  {trace}")
        
        return result
    
    def query(self, question: str) -> str:
        """Ask the agent a question"""
        message = HumanMessage(content=question)
        self.state["messages"] = [message]
        
        result = self.graph.invoke(self.state)
        
        # Get final response
        final_message = result["messages"][-1]
        return final_message.content


def main():
    """Test the agent"""
    agent = BioWatcherAgent()
    
    # Simulate an event
    event = {
        "source": "external_web",
        "url": "http://localhost:5000/alerts",
        "change_type": "new_alert",
        "content_preview": "WARNING: Drug-X (Cardioxin) shows increased risk..."
    }
    
    agent.process_event("web_delta", event)


if __name__ == "__main__":
    main()
