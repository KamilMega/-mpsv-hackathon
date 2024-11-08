from openai import AzureOpenAI
import os
import json
from src.config import AZURE_API_KEY, AZURE_ENDPOINT, AZURE_EMBEDDING_DEPLOYMENT_ID, AZURE_GPT_DEPLOYMENT_ID


from src.utils.prompt import user_prompt, system_prompt

client = AzureOpenAI(
    azure_endpoint = AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version="2024-08-01-preview"
)


def extract_skills_and_jobdesc_from_job_description(job_description: str, profession: str) -> dict:
    completion = client.chat.completions.create(
        model="gpt-4o-2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.format(job_description=job_description, position_name=profession)},
        ],
        response_format={ "type": "json_object" }
    )

    skills_extraction = completion.choices[0].message.content
    skills_json = json.loads(skills_extraction)

    return skills_json



def extract_skills_and_descriptors(system_prompt: str, user_prompt: str, description: str, name: str) -> dict:
    completion = client.chat.completions.create(
        model="gpt-4o-2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.format(description=description, name=name)},
        ],
        response_format={ "type": "json_object" }
    )

    response_text = completion.choices[0].message.content
    parsed_output = json.loads(response_text)

    return parsed_output