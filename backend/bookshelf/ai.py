import json
import os
import openai
from django.conf import settings

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_book_detail(name):

    openai.api_key =settings.OPENAI_API_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "َYou are a bibliophile.  Follow these steps to answer the user queries.  Step 1 - Try to "
                        "find the book name . step2 write a short summary of the book you found.  Provide your answer "
                        "in JSON form. Reply with only the answer in JSON form and include no other commentary  "
                        "\n```json"},

            {"role": "user", "content": " give me summary about the book name: " + name   }
        ]
    )

    return json.loads(completion.choices[0].message.content)
