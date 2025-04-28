import logging
import os

from openai import OpenAI
from anthropic import Anthropic

ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"
OPENAI_MODEL = "gpt-4o-mini"
MAX_TOKENS = 2048
TEMPERATURE = 0.5


def make_llm_inference(provider, system_prompt, user_prompt):

    logging.debug(f"=== LLM REQUEST ({provider}) ===")
    logging.debug(user_prompt)

    prompt = {"role": "user", "content": user_prompt}

    if provider == "anthropic":
        llm_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        resp = llm_client.messages.create(
            model=ANTHROPIC_MODEL,
            system=system_prompt,
            messages=[prompt],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        response = resp.content[0].text
    elif provider == "openai":
        llm_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = llm_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                prompt,
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        response = completion.choices[0].message.content
    else:
        raise Exception(f"Unsupported LLM provider: {provider}")

    logging.debug(f"=== LLM RESPONSE ({provider}) ===")
    logging.debug(response)

    return response
