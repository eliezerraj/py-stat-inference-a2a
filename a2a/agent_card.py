AGENT_CARD = {
    "name": "stat-inference-agent",
    "version": "v1",
    "protocol": "a2a/1.0",
    "description": "Statistical inference agent (windowed TPS analysis)",
    "capabilities": [
        {
            "consumes": ["STAT_TPS","LIST_TPS"],
            "produces": ["STAT_RESULT","LIST_RESULT"]
        }
    ],
    "endpoints": {
        "message": "/a2a/message"
    }
}
