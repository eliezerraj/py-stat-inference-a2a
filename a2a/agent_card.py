from infrastructure.config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "description": "Statistical inference agent (windowed data analysis)",
    "version": settings.VERSION,
    "provider": {
        "organization": "eliezer-junior Org.",
        "url": settings.URL_AGENT,
    },
    "documentationUrl": f"{settings.URL_AGENT}/info",
    "supportedInterfaces": [
        {
            "url": f"{settings.URL_AGENT}/a2a/message",
            "protocolBinding": "HTTP+JSON",
            "protocolVersion": "1.0",
        }
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "stateTransitionHistory": False,
        "extendedAgentCard": False,
    },
    "defaultInputModes": ["application/json"],
    "defaultOutputModes": ["application/json"],
    "skills": [
        {
            "id": "COMPUTE_STAT",
            "name": "Compute Statistics",
            "description": "Computes descriptive statistics and trend metrics from an input numeric array.",
            "tags": ["statistics", "analytics", "timeseries"],
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": { "type": "number" }
                    }
                },
                "required": ["data"]
            },
            "examples": [
                {"data": [10.4, 11.0, 12.0, 13.5]}
            ],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        }
    ],
}
