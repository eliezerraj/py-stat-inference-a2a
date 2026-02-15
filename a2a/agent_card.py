from config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "version": settings.VERSION,
    "url": settings.URL_AGENT,
    "version": "v1",
    "protocol": "a2a/1.0",
    "description": "Statistical inference agent (windowed data analysis)",
    "maintainer": {
        "contact": "eliezerral@gmail.com",
        "organization": "MLOps"
    },
    "capabilities": [
        {
            "intent": "STATISTICAL_ANALYSIS",
            "consumes": ["COMPUTE_STAT"],
            "produces": ["COMPUTE_STAT_RESULT"],
            "input_modes": ["application/json"],
            "output_modes": ["application/json"],
            "schema": {
                "type": "object",
                "properties": { 
                    "data": { "type": "array" , "items": { "type": "number" },
                    },
                },
                "required": ["data"]
            },
        },
    ],
    "skills": {
        "compute_statistic": "Compute all statistics from a given array of values",
    },
    "endpoints": {
        "message": "/a2a/message",
        "health": "/info",
    },
    "security": {
        "type": "none", 
        "description": "Localhost testing mode"
    }
}
