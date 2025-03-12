# Copyright (c) Microsoft. All rights reserved.

import asyncio
from typing import Annotated

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from dotenv import load_dotenv
import os
from tool_create_finetuning_environment import initialize_finetuning_environment

load_dotenv()

# Plugin for IntelliFra
class FineTuningPlugin:
    """Plugin for finetuning environent, prepare training dataset etc."""

    @kernel_function(description="Creates finetuning training environment.")
    def create_training_environment(self) -> Annotated[str, "Returns the status of training environment creation."]:
        initialize_finetuning_environment(config={})
        return """
        Training Environment: Created Successfully
        """


# Simulate a conversation with the agent
USER_INPUTS = [
    "Create a training environment"
]

async def main():
    # 1. Create the agent
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME") ,  
            api_key=os.getenv("OPENAI_API_KEY") ,
            endpoint=os.getenv("OPENAI_API_BASE")  , # Used to point to your service
            service_id="intellifra", # Optional; for targeting specific services within Semantic Kernel
        ),
        name="FineTuningAgent",
        instructions="Create training environment.",
        plugins=[FineTuningPlugin()],
    )

    # 2. Create a chat history to hold the conversation
    chat_history = ChatHistory()

    for user_input in USER_INPUTS:
        # 3. Add the user input to the chat history
        chat_history.add_user_message(user_input)
        print(f"# User: {user_input}")
        # 4. Invoke the agent for a response
        response = await agent.get_response(chat_history)
        print(f"# {response.name}: {response.content} ")


if __name__ == "__main__":
    asyncio.run(main())