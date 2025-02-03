# FastFAQ

A multilingual FAQ Management Solution created using FastAPI.

## Tech Stack
- FastAPI
- PostgreSQL
- Redis

## Key Differentiators

1. **Scalability** - Due to a cleaner database schema, new languages for FAQs can be added without a fuss with just a single change.
2. **Fast** - Uses BackgroundTasks and asynchorous programming along with redis caching for querying FAQs within no time.
3. **Test Driven** - Built with the methodology of test first and code second to ensure correct responses.
4. **Accurate Translation** - Uses Google Cloud API directly to ensure that html tags coming from ckeditor don't cause an issue while translation.

## Getting Started


Clone the repository:

```
git clone https://github.com/BlazeStorm001/FastFAQ.git
cd fastfaq
```

Create a new project on Google Cloud console and obtain a [Service Key](https://cloud.google.com/iam/docs/keys-create-delete) (json) and place it in the root of the project as `gcp_cred.json`.


Ensure docker is installed and run the following command:

```
docker-compose up --build
```

Access the shell of the docker container and run unit tests:

```
docker exec -it faq_api bash
pytest
```
You can access the Swagger documentation by accessing `localhost:8000/docs` and ensure working of endpoints



## API Usage


This API provides endpoints to retrieve frequently asked questions (FAQs) in multiple languages. The default language is English (`en`), but users can request FAQs in different languages.


### 1. Get All FAQs in English
#### **Endpoint**
```http
GET /api/faqs
```
#### **Description**
Retrieves all FAQs in English.

#### **Response**
```json
[
    {
        "id": 1,
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern web framework for building APIs with Python.",
        "language": "en"
    },
    {
        "id": 2,
        "question": "How do I reset my password?",
        "answer": "Click on 'Forgot Password' and follow the instructions.",
        "language": "en"
    }
]
```

---

### 2. Get an FAQ by ID in English
#### **Endpoint**
```http
GET /api/faqs/?id={faq_id}
```
#### **Description**
Retrieves an FAQ by its unique ID in English.

#### **Parameters**
| Parameter | Type  | Required | Description |
|-----------|-------|----------|-------------|
| `id`      | `int` | Yes      | The unique ID of the FAQ |

#### **Response**
```json
{
    "id": 1,
    "question": "What is FastAPI?",
    "answer": "FastAPI is a modern web framework for building APIs with Python.",
    "language": "en"
}
```

---

### 3. Get All FAQs in a Specific Language
#### **Endpoint**
```http
GET /api/faqs/?lang={language_code}
```
#### **Description**
Retrieves all FAQs in the requested language. If an FAQ is not available in the requested language, the English version is returned.

#### **Parameters**
| Parameter      | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `lang`        | `str`  | Yes      | The two-letter language code (e.g., `hi` for Hindi, `fr` for French) |

#### **Response (if Hindi version exists)**
```json
[
    {
        "id": 1,
        "question": "फ़ास्टएपीआई क्या है?",
        "answer": "FastAPI एक आधुनिक वेब फ्रेमवर्क है जो Python में APIs बनाने के लिए उपयोग किया जाता है।",
        "language": "hi"
    },
    {
        "id": 2,
        "question": "त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है",
        "answer": "<p>त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है</p>",
        "language": "hi"
    }
]
```

#### **Response (if Hindi version is unavailable for some FAQs, fallback to English)**
```json
[
    {
        "id": 1,
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern web framework for building APIs with Python.",
        "language": "en"
    },
    {
        "id": 2,
        "question": "त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है",
        "answer": "<p>त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है</p>",
        "language": "hi"
    }

]
```

---

### 4. Get an FAQ by ID in a Specific Language
#### **Endpoint**
```http
GET /api/faqs/?id={faq_id}&lang={language_code}
```
#### **Description**
Retrieves an FAQ by ID in the requested language. If the requested language version is unavailable, the English version is returned. If neither is available, it returns a `404 Not Found` error.

#### **Parameters**
| Parameter      | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `id`         | `int`  | Yes      | The unique ID of the FAQ |
| `lang`       | `str`  | Yes      | The two-letter language code (e.g., `hi` for Hindi, `fr` for French) |

#### **Response (if Hindi version exists)**
```json
{
    "id": 1,
    "question": "फ़ास्टएपीआई क्या है?",
    "answer": "FastAPI एक आधुनिक वेब फ्रेमवर्क है जो Python में APIs बनाने के लिए उपयोग किया जाता है।",
    "language": "hi"
}
```

#### **Response (if Hindi version is unavailable, fallback to English)**
```json
{
    "id": 1,
    "question": "What is FastAPI?",
    "answer": "FastAPI is a modern web framework for building APIs with Python.",
    "language": "en"
}
```

#### **Response (if FAQ ID does not exist)**
```json
{
    "detail": "FAQ not found"
}
```

---

## Error Responses
| Status Code | Meaning | Description |
|-------------|---------|-------------|
| `400`       | Bad Request | Invalid parameters in the request eg. wrong language code. |
| `404`       | Not Found | The requested FAQ ID does not exist in the database. |

---

## Example Usage

**Get all FAQs in English**
```sh
curl -X GET "http://localhost:8000/api/faqs"
```

**Get an FAQ by ID (e.g., ID = 1)**
```sh
curl -X GET "http://localhost:8000/api/faqs/?id=1"
```

**Get all FAQs in Hindi**
```sh
curl -X GET "http://localhost:8000/api/faqs/?lang=hi"
```

**Get an FAQ by ID in Hindi (fallback to English if unavailable)**
```sh
curl -X GET "http://localhost:8000/api/faqs/?id=1&lang=hi"
```

---

## Notes
- The default language is **English (`en`)**.
- If a requested language version is unavailable, it falls back to the English version.
- If an FAQ ID does not exist, a `404 Not Found` error is returned.

---


