import json
import time
import requests
import random
import string
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse 
from common.protocol import ChatCompletionInput, ChatMessageHistory, ModelUtils
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/v1/models")
@app.get("/models")
def models():
    model = {"data":[]}
    for i in ModelUtils.convert:
        model["data"].append({
            "id": i,
            "object": "model",
            "owned_by": "Dentristan",
            "tokens": 99999,
            "fallbacks": None,
            "endpoints": [
                "/v1/chat/completions"
                ],
            "limits": None,
            "permission": []
            })
    return JSONResponse(content=model)
    

@app.post("/v1/chat/completions")
async def create_chat_completions(input_data: ChatCompletionInput):
    
    # Переменные и их получение
    history = ChatMessageHistory()
    model = input_data.model
    messages = input_data.messages
    stream = input_data.stream
    temperature = input_data.temperature
    max_tokens = input_data.max_tokens
    top_p = input_data.top_p
    presence_penalty = input_data.presence_penalty
    frequency_penalty = input_data.frequency_penalty
    n = input_data.n
    
    with open('tempfiles/response.json', 'r') as infile:
            responses = json.load(infile)
            
    completion_id = "".join(random.choices(string.ascii_letters + string.digits, k=28))
    completion_timestamp = int(time.time())
    
    # Стриминг
    async def stream_response():
        completion_data = {
            "id": f"chatcmpl-{completion_id}",
            "object": "chat.completion.chunk",
            "created": completion_timestamp,
            "model": model,
            "choices": [
                {"delta": {"content": ""}, "index": 0, "finish_reason": None}
            ],
        }
        async for chunk in responses:
            completion_data["choices"][0]["delta"]["content"] = chunk
            yield f"data: {json.dumps(completion_data)}\n\n"
        
        # Завершаем генератор после обработки всех данных
        completion_data = {
            "choices": [{"delta": {}, "finish_reason": "stop", "index": 0}],
            "created": completion_timestamp,
            "id": f"chatcmpl-{completion_id}",
            "model": model,
            "object": "chat.completion.chunk",
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    # Обнуляем контекст здесь, после обработки запроса
    history.messages = []
    
    yield StreamingResponse(stream_response(), media_type="text/event-stream")
    
    
    try:
        print (responses)
        yield responses['data'][0][0]
    except Exception as error:
        raise error

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2566)
