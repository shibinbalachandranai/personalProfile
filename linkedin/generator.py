import random
import anthropic
import config


def generate_post(topic: str = None) -> str:
    if topic is None:
        topic = random.choice(config.TOPIC_POOL)

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=config.SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Write a LinkedIn post about: {topic}"}
        ],
    )

    return message.content[0].text
