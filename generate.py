import json
import time

import utils

from groq import Groq
import dotenv
import os

dotenv.load_dotenv()

client = Groq(

)


def generate(prompt="i am playing a game make me anime style song", bearer_token=None):
    completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {
                "role": "system",
                "content": "you are a maker of songs. you make songs according to the user’s request to make a song you must give a description of the musical style, the singer’s characteristics, the topic. Keep a slight link to computer science. the musical style must be expressed as a list of keywords such as `Synth-pop ballad, melancholic piano, glitchy electronics, ethereal female vocals, 60 BPM, Electronic, retro game synths, driving bass, arcade-style arpeggios`\n"
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    content = completion.choices[0].message.content
    # remove "<think>" and "</think>" blocks
    # find the first "<think>" and remove it and all the text until the first "</think>"
    start = content.find("<think>")
    if start != -1:
        end = content.find("</think>", start)
        if end != -1:
            content = content[:start] + content[end + len("</think>"):]
    # remove all "<think>" and "</think>" blocks
    content = content.replace("<think>", "")
    content = content.replace("</think>", "")
    print(content)
    model_public_name = "FUZZ-0.8"
    jobs = utils.generate_prompt(
        topic=content,
        instrumental=False,
        model_public_name=model_public_name,
        bearer_token=bearer_token)

    if not jobs:
        print("Failed to generate prompt.")
        return None
    # print the jobs
    print(jobs)
    # get the first job
    job = jobs['jobs'][0]
    # get the first job id
    job_id = job["id"]
    # call https://wb.riffusion.com/generate/status/{job_id} to get the status of the job
    status = utils.get_job_status(job_id, bearer_token)
    while status["status"] != "complete":
        print("Waiting for job to complete...")
        time.sleep(5)
        status = utils.get_job_status(job_id, bearer_token)
    # save status to file as json
    with open("status.json", "w") as f:
        f.write(json.dumps(status, indent=4))
    # get the first audio_url
    audio_url = utils.get_generations([job_id], bearer_token)['generations'][0]['audio_url']
    # print the audio_url
    print(audio_url)
    return status, audio_url, content


if __name__ == "__main__":
    generate("i am playing a game make me anime style song", bearer_token=os.getenv("RIFFUSION_TOKEN"))
