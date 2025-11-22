"""
Kalpana AGI - Main Backend Entry Point
Purpose: Initialize FastAPI, Socket.IO, and Core Systems.
Dependencies: fastapi, uvicorn, python-socketio
Permissions: Network Access
"""

import os
import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import socketio
import uvicorn
from backend.modules.system_monitor import system_monitor
from backend.modules.network_scanner import network_scanner
from backend.tools.system_control import system_control
from backend.kalpana_core.brain import brain
from backend.voice.voice_engine import voice_engine
from backend.security.security_core import security_core
from backend.security.firewall_manager import firewall_manager
from backend.web.scraper import web_scraper
from backend.kalpana_core.memory import memory

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Kalpana.Main")

# Initialize FastAPI
app = FastAPI(title="Kalpana AGI", description="Backend for Kalpana Jarvis-level Assistant", version="1.0.0")

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Socket.IO (Async)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Mount Frontend (Static Files)
# We assume the frontend build or raw files are in ../frontend
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if not os.path.exists(FRONTEND_DIR):
    os.makedirs(FRONTEND_DIR)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

# API Routes
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/health")
async def health_check():
    return {"status": "online", "system": "Kalpana AGI"}

@app.post("/api/test/diagnostics")
async def run_diagnostics():
    """
    Trigger a full system diagnostic test:
    1. Open Calculator (Visual Test)
    2. Scan Network (Data Test)
    3. Update UI
    """
    logger.info("Starting Diagnostics...")
    await sio.emit('system_event', {'type': 'info', 'message': 'Running System Diagnostics...'})
    
    # 1. Test App Opening
    await sio.emit('system_event', {'type': 'action', 'message': 'Opening Calculator...'})
    system_control.open_app("Calculator")
    
    # 2. Test Network Scan
    await sio.emit('system_event', {'type': 'action', 'message': 'Scanning Network...'})
    connections = network_scanner.get_active_connections()
    local_ip = network_scanner.get_local_ip()
    
    # 3. Report Results
    report = {
        "local_ip": local_ip,
        "active_connections": len(connections),
        "top_connections": connections
    }
    await sio.emit('diagnostics_result', report)
    await sio.emit('system_event', {'type': 'success', 'message': 'Diagnostics Complete.'})
    
    return {"status": "completed", "report": report}

@app.post("/api/test/chat")
async def test_chat(request: Request):
    """
    Test the Brain's LLM integration.
    Accepts JSON: {"message": "user input"}
    """
    try:
        data = await request.json()
        user_message = data.get("message", "Hello, Kalpana. Are you online?")
        
        logger.info(f"Testing chat with: {user_message}")
        await sio.emit('system_event', {'type': 'info', 'message': f'Processing: {user_message}'})
        
        # Call the Brain
        response = await brain.process_input(user_message)
        
        await sio.emit('chat_response', {'user': user_message, 'kalpana': response})
        return {"status": "success", "user": user_message, "response": response}
    except Exception as e:
        logger.error(f"Chat test failed: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/test/voice")
async def test_voice(request: Request):
    """
    Test the Voice Engine (TTS).
    Accepts JSON: {"text": "message to speak"}
    """
    try:
        data = await request.json()
        text = data.get("text", "Kalpana voice systems online. All neural pathways functioning within normal parameters.")
        
        logger.info(f"Testing TTS with: {text}")
        await sio.emit('system_event', {'type': 'info', 'message': 'Activating voice synthesis...'})
        
        # Use asyncio.to_thread to run blocking TTS in background
        await asyncio.to_thread(voice_engine.speak, text)
        
        await sio.emit('system_event', {'type': 'success', 'message': 'Voice test complete.'})
        return {"status": "success", "text": text}
    except Exception as e:
        logger.error(f"Voice test failed: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/test/security")
async def test_security():
    """
    Test the Security Core monitoring.
    """
    try:
        logger.info("Testing Security Core...")
        await sio.emit('system_event', {'type': 'info', 'message': 'Running security diagnostics...'})
        
        # Check if security is running
        status = "Active" if security_core.observer.is_alive() else "Inactive"
        
        await sio.emit('security_status', {
            'monitor_status': status,
            'protected_path': security_core.monitor_path,
            'message': f'Security monitoring is {status}'
        })
        
        return {"status": "success", "security_monitor": status}
    except Exception as e:
        logger.error(f"Security test failed: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/voice/process")
async def process_voice(request: Request):
    """
    Process voice input from Arc Reactor mic button.
    Transcribes speech, sends to Brain, and optionally speaks response.
    """
    try:
        data = await request.json()
        transcript = data.get("transcript", "")
        
        if not transcript:
            return {"status": "error", "message": "No transcript provided"}
        
        logger.info(f"Processing voice input: {transcript}")
        await sio.emit('system_event', {'type': 'info', 'message': f'Processing: {transcript}'})
        
        # Send to Brain for LLM processing
        response = await brain.process_input(transcript)
        
        # Emit response to UI
        await sio.emit('voice_response', {
            'transcript': transcript,
            'response': response
        })
        
        # Trigger TTS in background
        asyncio.create_task(asyncio.to_thread(voice_engine.speak, response))
        
        return {"status": "success", "transcript": transcript, "response": response}
    except Exception as e:
        logger.error(f"Voice processing failed: {e}")
        return {"status":"error", "message": str(e)}

@app.post("/api/research")
async def research_topic(request: Request):
    """
    Research a topic using web scraping.
    """
    try:
        data = await request.json()
        query = data.get("query", "")
        
        if not query:
            return {"status": "error", "message": "No query provided"}
        
        logger.info(f"Researching: {query}")
        await sio.emit('system_event', {'type': 'info', 'message': f'Researching: {query}'})
        
        # Scrape web for information
        result = await web_scraper.research(query)
        
        await sio.emit('research_result', {'query': query, 'result': result})
        
        return {"status": "success", "query": query, "result": result}
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/memory/stats")
async def get_memory_stats():
    """
    Get memory statistics.
    """
    try:
        stats = memory.get_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        logger.error(f"Memory stats error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/memory/conversations")
async def get_conversations(limit: int = 10):
    """
    Get recent conversations.
    """
    try:
        conversations = memory.get_recent_conversations(limit)
        return {"status": "success", "conversations": conversations}
    except Exception as e:
        logger.error(f"Get conversations error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/memory/clear")
async def clear_memory():
    """
    Clear all memory (WARNING: Irreversible).
    """
    try:
        memory.clear_all()
        await sio.emit('system_event', {'type': 'warning', 'message': 'All memory cleared'})
        return {"status": "success", "message": "Memory cleared"}
    except Exception as e:
        logger.error(f"Clear memory error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/security/status")
async def get_security_status():
    """
    Get comprehensive security status.
    """
    try:
        sec_status = security_core.get_status()
        fw_status = firewall_manager.get_status()
        
        return {
            "status": "success",
            "security": sec_status,
            "firewall": fw_status
        }
    except Exception as e:
        logger.error(f"Security status error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/security/firewall/enable")
async def enable_firewall():
    """
    Enable the packet filter firewall (requires sudo).
    """
    try:
        success = firewall_manager.enable()
        if success:
            await sio.emit('firewall_status', {'status': 'enabled'})
            return {"status": "success", "message": "Firewall enabled"}
        else:
            return {"status": "error", "message": "Failed to enable firewall"}
    except Exception as e:
        logger.error(f"Enable firewall error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/security/firewall/disable")
async def disable_firewall():
    """
    Disable the packet filter firewall (requires sudo).
    """
    try:
        success = firewall_manager.disable()
        if success:
            await sio.emit('firewall_status', {'status': 'disabled'})
            return {"status": "success", "message": "Firewall disabled"}
        else:
            return {"status": "error", "message": "Failed to disable firewall"}
    except Exception as e:
        logger.error(f"Disable firewall error: {e}")
        return {"status": "error", "message": str(e)}

# Socket.IO Events
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")
    await sio.emit('system_event', {'type': 'connection', 'status': 'connected', 'message': 'Kalpana Core Online'}, room=sid)

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def user_command(sid, data):
    """Handle incoming user commands from the HUD"""
    logger.info(f"Received command: {data}")
    # TODO: Route to Brain/Planner
    await sio.emit('response', {'status': 'processing', 'data': data}, room=sid)

# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    logger.info("Kalpana System Startup Initiated...")
    # Start System Monitor
    asyncio.create_task(system_monitor.start_monitoring(sio))
    # Start Security Core
    security_core.start_protection()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Kalpana System Shutdown...")
    # Cleanup resources

if __name__ == "__main__":
    # Dev mode run
    uvicorn.run("backend.main:socket_app", host="0.0.0.0", port=8001, reload=True)
