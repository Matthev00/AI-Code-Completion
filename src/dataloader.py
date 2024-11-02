import os
import ast
import random


class CodeCopletionDataset:
    def __init__(
        self,
        data_dir: str = "data/raw",
        max_length: int = 150,
        min_length: int = 20,
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
        total_length = len(code_block)
        middle_length = random.randint(self._min_length, self._max_length)
        remaining_length = total_length - middle_length

        prefix_length = random.randint(self._min_length, remaining_length // 2)
        suffix_length = remaining_length - prefix_length

        # Ensure suffix is not too long
        if suffix_length > self._max_length:
            suffix_length = self._max_length

        prefix = code_block[:prefix_length]
        middle = code_block[prefix_length:prefix_length + middle_length]
        suffix = code_block[prefix_length + middle_length:prefix_length + middle_length + suffix_length]

        return prefix, middle, suffix

    def _establish_num_samples(self, block_length):
        if block_length < self._max_length * 2:
            return 1
        elif block_length < self._max_length * 4:
            return 2
        else:
            return 3

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


class CodeCompletionDataLoader:
    def __init__(self, dataset):
        self.dataset = dataset
        self.idx = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.idx < len(self.dataset):
            sample = self.dataset[self.idx]
            self.idx += 1
            return sample
        else:
            raise StopIteration


def main():
    dataset = CodeCopletionDataset()[:50]
    dataloader = CodeCompletionDataLoader(dataset)
    print(next(dataloader)[2])


if __name__ == "__main__":
    main() 
