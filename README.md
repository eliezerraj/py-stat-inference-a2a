# py-stat-inference-a2a

py-stat-inference-a2a

# Features

### Range

It answers:
“How far did the system swing between best and worst case?”

    Example
    A = [9, 9, 9, 9, 9]
    B = [9, 9, 9, 9, 15]   # throttle

    Metric	A	B
    Mean	9	9.8
    Std	    0	2.4
    Range	0	6

### P95
It answers:
“What TPS do we hit most of the time when stressed?”

    Example
    A = [8, 8, 8, 8, 8]
    B = [8, 8, 8, 8, 15]
    C = [8, 15, 8, 15, 8]

        Mean	Std	    p95
    A	8	    0	    8
    B	9.4	    3.1	    15
    C	10.2	3.6	    15

    STD struggles to separate B vs C.
    p95 immediately says: “Both hit the ceiling

### MAD

it answers:
“On average, how far is TPS from its typical value?”

    Two TPS windows:
    W1 = [8, 8, 8, 8, 8]
    W2 = [8, 9, 8, 7, 8]
    W3 = [8, 8, 8, 8, 12]

    Window	STD	    MAD
    W1	    0.0	    0.0
    W2	    0.7	    0.6
    W3	    1.6	    0.64

    Interpretation:
    
    With STD:
    W2 and W3 look equally unstable

    With MAD: 
    W2 = smooth
    W3 = bursty

    This matches real TPS semantics.

    STD overreacts to one burst.
    MAD reflects typical deviation, not rare spikes.

### N_SLOPE

It answers:

“How fast is TPS changing relative to its level?”

    Example
    TPS = [8, 9, 10, 11, 12]
    mean = 10
    slope = 1
    normalized slope = 0.10

    Interpretation:
    TPS grows ~10% per step

### AUTO_CORRELATION

It answers:

“If TPS is high now, will it stay high next step?”

    Example patterns

    Smooth throttling
    [9, 9, 10, 10, 10]
    autocorr ≈ 0.9

    Bursty traffic
    [8, 15, 8, 15, 8]
    autocorr ≈ 0

    Control oscillation
    [8, 14, 8, 14, 8]
    autocorr < 0


## Diagram

# create venv

    python3 -m venv .venv

# activate

    source .venv/bin/activate

# install requirements

    pip install -r requirements.txt

# run (root)

    uvicorn main:app --host 0.0.0.0 --port 8000 --no-access-log --log-level debug

## test Local

    export VERSION=0.1
    export ACCOUNT=aws:999999999
    export APP_NAME=py-stat-inference-a2a.localhost
    export HOST=127.0.0.1 
    export URL_AGENT=http://127.0.0.1:8000     
    export PORT=8000
    export WINDOW_SIZE=30
    export SESSION_TIMEOUT=3000
    export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
    export LOG_LEVEL=DEBUG 
    export OTEL_STDOUT_LOG_GROUP=True
    export LOG_GROUP=/mnt/c/Eliezer/log/py-stat-inference-a2a.log

## Endpoint    

    curl --location 'http://localhost:8000/.well-known/agent.json'

    curl --location 'http://localhost:8000/agent_card_register'

    curl --location 'http://localhost:8000/a2a/message' \
        --header 'Content-Type: application/json' \
        --data '{
        "source_agent": "producer-agent",
        "target_agent": "stat-inference-agent",
        "message_type": "COMPUTE_STAT",
        "payload": {
            "data": [10,10,10,10,10,10,2]
        }
    }'