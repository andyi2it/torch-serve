import argparse
import os

from huggingface_hub import HfApi, snapshot_download


def dir_path(path_str):
    if os.path.isdir(path_str):
        return path_str
    elif input(f"{path_str} does not exist, create directory? [y/n]").lower() == "y":
        os.makedirs(path_str)
        return path_str
    else:
        raise NotADirectoryError(path_str)


class HFModelNotFoundError(Exception):
    def __init__(self, model_str):
        super().__init__(f"HuggingFace model not found: '{model_str}'")


def hf_model(model_str):
    api = HfApi()
    models = [m.modelId for m in api.list_models()]
    if model_str in models:
        return model_str
    else:
        raise HFModelNotFoundError(model_str)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_path",
    "-o",
    type=dir_path,
    default="model",
    help="Output directory for downloaded model files",
)
parser.add_argument(
    "--model_name", "-m", type=hf_model, required=True, help="HuggingFace model name"
)
parser.add_argument("--revision", "-r", type=str, default="main", help="Revision")
args = parser.parse_args()
# Only download pytorch checkpoint files
allow_patterns = ["*.json", "*.pt", "*.bin", "*.txt", "*.model", "*.pth"]

snapshot_path = snapshot_download(
    repo_id=args.model_name,
    revision=args.revision,
    allow_patterns=allow_patterns,
    cache_dir=args.model_path,
    use_auth_token=False,
)
print(f"Files for '{args.model_name}' is downloaded to '{snapshot_path}'")
