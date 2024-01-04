import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-35-turbo",
            "gpt-3.5-turbo-16k",
        }
    },
)

config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': 'Your OpenAi api key',
    }
]

# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""Create a page about monkeys using Python to generate HTML, Javascript and CSS code. The HTML should include a top navigation bar and example images of monkeys from the links: https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D , https://images.unsplash.com/photo-1463852247062-1bbca38f7805?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8NXx8fGVufDB8fHx8fA%3D%3D , https://images.unsplash.com/photo-1570288685280-7802a8f8c4fa?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTF8fHxlbnwwfHx8fHw%3D with descriptions. The CSS should style the navigation bar and images. The JavaScript should display an alert when an image is clicked.""",
)

user_proxy.send(
    recipient=assistant,
    message="""Create a file named monkeys_page_generation.py and add there a python script with you have generated"""
)