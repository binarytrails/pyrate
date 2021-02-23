# @author dotPY-hax
# @author Vsevolod Ivanov

class CLI:
    def __init__(self):
        self.prompt_text = '>'

    def cli_prompt(self):
        prompt = input(self.prompt_text)
        return prompt

    def cli_print(self, content):
        if isinstance(content, list):
            for line in content[:-1]:
                print(line)
            self.prompt_text = content[-1]
        else:
            print(content)
