from dotenv import load_dotenv
import os
import time
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"),
)

file = client.files.create(
    file = open("Skoe_Neuroscience_2017.pdf", "rb"),
    purpose = "assistants"
)

assistant = client.beta.assistants.create(
    name = "research-friend",
    instructions = "You are reviewing a research article determine if it meets several criterion. You always respond in JSON format.",
    tools = [{"type": "retrieval"}],
    model = "gpt-4-0125-preview",
    file_ids = ["file-6erlJyPHj9N5VXhsWD0ncjwo"]
)

thread = client.beta.threads.create()

#User asks question
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "Provided in JSON format, how many participants were there in this study?"
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id,
)

counter = 0
while run.status != 'completed':
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if counter % 10 == 0:
        #print(f"\t\t{run}")
        counter += 1
    time.sleep(5)

messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

for message in reversed(messages.data):
    print(message.role + ": " + message.content[0].text.value)


