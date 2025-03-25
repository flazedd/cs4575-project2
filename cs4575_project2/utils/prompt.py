class Prompt:
    def __init__(self, instance):
        self.instance_id = instance.get("instance_id", "")
        self.repo = instance.get("repo", "")
        self.base_commit = instance.get("base_commit", "")
        self.problem_statement = instance.get("problem_statement", "")
        self.hints_text = instance.get("hints_text", "")
        self.version = instance.get("version", "")
        self.environment_setup_commit = instance.get("environment_setup_commit", "")
        self.full_text = instance.get("text", "")

    def construct_prompt(self):
        prompt = f"""
You are a software engineer tasked with resolving a GitHub issue.

Repository: {self.repo}
Base Commit: {self.base_commit}
Environment Setup Commit: {self.environment_setup_commit}
Version: {self.version}
Instance ID: {self.instance_id}

Issue Description:
{self.problem_statement}

Full Context:
{self.full_text}

Hints (if any):
{self.hints_text}

Assume you have access to the complete repository context with all the relevant code files.
Your task is to generate a single patch file in standard diff format that resolves the issue described above.
Output only the patch file.
"""
        return prompt.strip()
