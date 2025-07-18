import os

from src.core.config.config_reader import app_config

class PromptLibrary:
    def __init__(self, prompt_dir: str = None):
        if prompt_dir is None:
            prompt_dir = app_config.app.prompt_dir
        self.prompt_dir = prompt_dir

    def get_prompt(self, prompt_key: str, **kwargs) -> str:
        """
        Retrieve the prompt text given a prompt_key (filename without extension),
        and fill in any variables in the prompt using kwargs.
        Example: prompt contains 'Hello {name}', call get_prompt('greet', name='World')
        """
        # Assume all prompts are markdown files
        if not prompt_key.endswith('.md'):
            prompt_key += '.md'
        prompt_path = os.path.join(self.prompt_dir, prompt_key)
        if not os.path.isfile(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        if kwargs:
            try:
                prompt = prompt.format(**kwargs)
            except KeyError as e:
                raise ValueError(f"Missing variable for prompt: {e}")
        return prompt
