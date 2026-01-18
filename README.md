## Transcript Extraction Microservice for my transcripter project 

This service is a standalone Python microservice responsible for extracting transcripts from YouTube videos and returning them in a clean, normalized JSON format.

It is designed to be consumed by other services (a Next.js application) and follows strict separation of concerns.

The service supports a multi-tier transcript strategy:

* Primary source: YouTube’s native transcript API
* Fallback source: SupaData API (used when no native transcript is available)

---

## Responsibilities
This microservice is responsible for:

* Accepting a YouTube video ID as input
* Retrieving the transcript from available providers
* Falling back automatically when a provider fails
* Returning a standardized transcript format
* Centralizing transcript-related error handling
* Remaining independently deployable and replaceable
---

## Architecture Overview

The service is designed to be part of a microservices-based system.

High-level flow:

1. A client (e.g., Next.js API route) sends a POST request with a video ID
2. The service attempts to fetch the transcript from YouTube
3. If unavailable, it automatically falls back to SupaData
4. The service returns a normalized JSON response
5. Errors are returned in a structured and predictable format

This allows upstream services to remain simple and provider-agnostic.

---

## API Contract

### Endpoint

```
POST /transcript
```

### Request Body

```json
{
  "video_id": "#123"
}
```

### Successful Response

```json
{
  "source": "youtube",
  "transcript": [
    {
      "text": "Today we learn neural networks",
      "start": 12.3
    },
    {
      "text": "A neural network is...",
      "start": 18.9
    }
  ]
}
```

### Error Response

```json
{
  "error": {
    "code": "TRANSCRIPT_NOT_FOUND",
    "message": "No transcript available from any provider"
  }
}
```

Error responses are always returned in this format to ensure predictable handling by consuming services.

---

## Transcript Normalization

Regardless of the transcript provider, the service always returns transcripts in the same structure:

* `text`: The spoken text segment
* `start`: Start time of the segment in seconds

This guarantees that downstream services can process transcripts without conditional logic based on the provider.

---

## Project Structure

```
transcript-service/
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── .env.example
│
├── routes/
│   └── transcript.py
│
├── services/
│   ├── youtube_service.py
│   └── supadata_service.py
│
├── utils/
│   ├── errors.py
│   └── formatter.py
│
└── README.md
```

The structure is intentionally designed modular to support easy extension and provider replacement in future. 

---

## Environment Variables

The service relies on the following environment variables:

```
SUPADATA_API_KEY
```

These should be configured in the deployment environment (Railway, AWS, etc.) and not committed to source control.

---


## Deployment

This service is designed to be deployed independently.

Recommended setup:

* Containerized using Docker
* Deployed on Railway, AWS, or any container-compatible platform
* Exposed via a public HTTP endpoint
* Consumed by a separate orchestration service (in my case by Next.js API routes(transcripter repo))

Because the service is stateless, it can be horizontally scaled if needed.

---

## Some Design Decisions

* **Single Responsibility**: The service focuses only on transcript extraction
* **Provider Abstraction**: Transcript sources are hidden behind a unified interface
* **Fallback Strategy**: Automatic fallback improves robustness
* **Standardized Output**: Simplifies downstream processing
* **Independent Deployment**: Enables safe updates and experimentation

---


## Intended Consumers

This service is intended to be consumed by:

* Backend orchestration services
* Serverless API routes
* Data processing pipelines
* Educational and content-generation systems
* By the way it is open-source and you can use it for you products. 

