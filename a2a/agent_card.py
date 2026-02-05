from config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "version": settings.VERSION,
    "url": settings.URL_AGENT,
    "version": "v1",
    "protocol": "a2a/1.0",
    "description": "Statistical inference agent (windowed data analysis)",
    "capabilities": [
        {
            "consumes": ["COMPUTE_STAT"],
            "produces": ["COMPUTE_STAT_RESULT"]
        }
    ],
    "skills": {
        "compute_statistic": "Compute all statistics from a given array of values",
    },
    "endpoints": {
        "message": "/a2a/message"
    }
}
