import os
import openai
import dotenv


def main():
    try:
        dotenv.load_dotenv()

        # Flag to show citations
        show_citations = True

        # Get configuration systems
        azure_oai_endpoint = os.environ["AZURE_OAI_ENDPOINT"]
        azure_oai_key = os.environ["AZURE_OAI_KEY"]
        azure_oai_deployment = os.environ["AZURE_OAI_DEPLOYMENT"]
        azure_search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
        azure_search_key = os.environ["AZURE_SEARCH_KEY"]
        azure_search_index = os.environ["AZURE_SEARCH_INDEX"]

        # Initialize the Azure OpenAI Client
        client = openai.AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version="2024-02-15-preview"
        )

        # Get the Promprt
        text = input('\nEnter a question:\n')

        # 데이터 소스 설정 (신규 data_sources / azure_search 형식)
        extension_config = dict(data_sources=[
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": azure_search_endpoint,
                    "index_name": azure_search_index,
                    "authentication": {
                        "type": "api_key",
                        "key": azure_search_key
                    }
                }
            }
        ])

        # Send request to Azure OpenAI model
        print("...Sending the following request to Azure OpenAI endpoint...")
        print("Request: " + text + "\n")

        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.5,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a helpful travel agent"},
                {"role": "user", "content": text}
            ],
            extra_body=extension_config
        )

        # Print response
        message = response.choices[0].message
        print("Response: " + (message.content or "") + "\n")

        if (show_citations):
            # 인용(Citation) 출력 — 신규 형식은 context 안에 citations 가 바로 들어 있음
            print("Citations:")
            for c in message.context["citations"]:  # type: ignore[attr-defined]
                print(" Title: " + c['title'] + "\n URL: " + c['url'])

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
