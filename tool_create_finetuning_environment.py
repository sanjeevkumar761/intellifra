import os
import json

def initialize_finetuning_environment(config):
    """
    Initializes the fine-tuning environment based on the provided configuration file.

    Args:
        config_path (str): Path to the configuration JSON file.

    Returns:
        dict: Configuration settings.
    """
    print("Initializing fine-tuning environment...")

    # import required libraries
    """
    This script sets up an Azure Machine Learning (ML) client using the DefaultAzureCredential for authentication. 
    It imports necessary libraries and handles exceptions during the ML client initialization.

    Modules imported:
    - time: Provides various time-related functions.
    - azure.identity: Provides authentication capabilities with DefaultAzureCredential and InteractiveBrowserCredential.
    - azure.ai.ml: Contains classes and functions for interacting with Azure ML services, including MLClient, Input, pipeline, load_component, command, Data, Environment, BuildContext, Model, Input, Output, and AssetTypes.
    - azure.core.exceptions: Contains exceptions for handling resource-related errors.
    - os: Provides a way to interact with the operating system.

    Variables:
    - credential: An instance of DefaultAzureCredential used for authenticating with Azure services.
    - ml_client: An instance of MLClient initialized using the provided credentials. If the initialization fails, an exception is caught and printed.
    """
    import time
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    from azure.ai.ml import MLClient, Input
    from azure.ai.ml.dsl import pipeline
    from azure.ai.ml import load_component
    from azure.ai.ml import command
    from azure.ai.ml.entities import Data, Environment, BuildContext
    from azure.ai.ml.entities import Model
    from azure.ai.ml import Input
    from azure.ai.ml import Output
    from azure.ai.ml.constants import AssetTypes
    from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
    import os 

    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    workspace = os.getenv("AZUREML_WORKSPACE")
    credential = DefaultAzureCredential()
    ml_client = None
    try:
        ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
    except Exception as ex:
        print(ex)

    env_name = "deepseek-training"
    env_docker_image = Environment(
                    build=BuildContext(path = "environment_train", dockerfile_path="Dockerfile"),
                    name=env_name,
                    description="Environment created for llm fine-tuning.",
                    version="1"
                )
    env_asset_train = ml_client.environments.create_or_update(env_docker_image)    

    return config
