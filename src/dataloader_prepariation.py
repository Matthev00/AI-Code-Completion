import os
import ast
import random


class CodeCopletionDataset:
    def __init__(
        self,
        data_dir: str = "data/raw",
        max_length: int = 500,
        min_length: int = 10,
        seed: int = 42,
    ):
        self.samples = []
        self.data_dir = data_dir
        random.seed(seed)
        """
        This function reads all .py files from the specified directory and makes a list of samples(prefix, middle ,sufix) for code completion task.

        Args:
        data_dir (str): The path to the directory containing .py files.
        """
        self.samples = []

        for root, _, files in os.walk(data_dir):
            for file in files:
                with open(os.path.join(root, file), "r") as f:
                    source_code = f.read()
                    tree = ast.parse(source_code)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) or isinstance(
                            node, ast.ClassDef
                        ):
                            start = node.lineno - 1
                            end = node.end_lineno

                            code_block = source_code.splitlines()[start:end]
                            code_block_str = "\n".join(code_block)

                            if len(code_block_str) >= max_length:
                                start_prefix = random.randint(
                                    0, len(code_block_str) - max_length
                                )
                                end_prefix = start_prefix + random.randint(
                                    min_length, max_length
                                )

                                start_middle = end_prefix
                                end_middle = start_middle + random.randint(
                                    min_length, max_length
                                )

                                start_suffix = end_middle

                                prefix = code_block_str[:end_prefix]
                                middle = code_block_str[start_middle:end_middle]
                                suffix = code_block_str[start_suffix:]

                                self.samples.append((prefix, middle, suffix))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


df = CodeCopletionDataset()

print(len(df))
print(df[3][0])
