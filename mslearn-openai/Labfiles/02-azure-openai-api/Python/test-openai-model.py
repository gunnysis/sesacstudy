import os
from dotenv import load_dotenv

# Add Azure OpenAI package
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

        if not azure_oai_endpoint or not azure_oai_key or not azure_oai_deployment:
            raise ValueError("Missing required Azure OpenAI configuration settings.")
        
        # Initialize the Azure OpenAI client...
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version="2025-01-01-preview"
        )
        system_message = """당신은 친절한 AI 도우미입니다."""

        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            


            messages_array: list[ChatCompletionMessageParam] = [
                {"role": "system", "content": system_message },
                {"role": "user", "content": input_text }
            ]
            


            response = client.chat.completions.create(
                model = azure_oai_deployment,
                temperature = 0.7,
                messages=messages_array,
                max_tokens = 1200,
            )

            generate_text = response.choices[0].message.content or ""
            messages_array.append({"role": "user", "content": input_text})
            print("Answer: " + generate_text + "\n")
            
            

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()