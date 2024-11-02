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
        """
        This function reads all .py files from the specified directory and makes a list of samples(prefix, middle ,sufix) for code completion task.

        Args:
        data_dir (str): The path to the directory containing .py files.
        """
        self.samples = []
        self._data_dir = data_dir
        self._max_length = max_length
        self._min_length = min_length
        random.seed(seed)

        for root, _, files in os.walk(data_dir):
            for file in files:
                with open(os.path.join(root, file), "r") as f:
                    source_code = f.read()
                    tree = ast.parse(source_code)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) or isinstance(
                            node, ast.ClassDef
                        ):
                            code_block_str = self._find_code_block(source_code, node)

                            num_samples_per_block = self._establish_num_samples(
                                len(code_block_str)
                            )

                            for _ in range(num_samples_per_block):
                                if len(code_block_str) >= self._max_length:
                                    self.samples.append(
                                        self._generate_sample(code_block_str)
                                    )

    def _find_code_block(self, source_code: str, node) -> str:
        start = node.lineno - 1
        end = node.end_lineno

        code_block = source_code.splitlines()[start:end]
        return "\n".join(code_block)

    def _generate_sample(self, code_block: str) -> tuple[str, str, str]:
        start_prefix = random.randint(0, len(code_block) - self._max_length)
        end_prefix = start_prefix + random.randint(self._min_length, self._max_length)

        start_middle = end_prefix
        end_middle = start_middle + random.randint(self._min_length, self._max_length)

        start_suffix = end_middle

        prefix = code_block[:end_prefix]
        middle = code_block[start_middle:end_middle]
        suffix = code_block[start_suffix:]

        return prefix, middle, suffix

    def _establish_num_samples(self, block_length):
        if block_length < self._max_length * 2:
            num_samples = 1
        elif block_length < self._max_length * 4:
            num_samples = 2
        elif block_length < self._max_length * 6:
            num_samples = 3
        return num_samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


df = CodeCopletionDataset()

print(len(df))
print(df[3][0])
