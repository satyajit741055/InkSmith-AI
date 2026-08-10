from pathlib import Path
from typing import Protocol
from app.config import settings


class BlogStorage(Protocol):
    def save(self, local_file_path: str) -> str: ...
    def resolve(self, key: str) -> Path: ...
    def get_url(self, key: str) -> str | None: ...
    def exists(self, key: str) -> bool: ...


class LocalStorage:
    """
    Stores files on local disk, under `base_dir`.
    """

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, local_file_path: str) -> str:
        src = Path(local_file_path)
        key = src.name

        dest = self.base_dir / key
        if src.resolve() != dest.resolve():
            dest.write_bytes(src.read_bytes())

        return key

    def resolve(self, key: str) -> Path:
        path = self.base_dir / key
        if not path.exists():
            raise FileNotFoundError(f"File not found for key: {key}")
        return path

    def get_url(self, key: str) -> str | None:
        return None

    def exists(self, key: str) -> bool:
        return (self.base_dir / key).exists()

class S3Storage:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    def save(self, local_file_path: str) -> str:
        # TODO: Implement S3 upload
        pass

    def resolve(self, key: str) -> Path:
        # TODO: Implement S3 download
        pass

    def get_url(self, key: str) -> str | None:
        # TODO: Implement S3 URL generation
        pass

    def exists(self, key: str) -> bool:
        # TODO: Implement S3 exists check
        pass

def _build_storage() -> BlogStorage:
    backend = getattr(settings, "BACKEND", "local")

    if backend == "local":
        output_dir = Path(settings.OUTPUT_DIR)
        if not output_dir.is_absolute():
            output_dir = Path(__file__).resolve().parents[2] / output_dir
        return LocalStorage(str(output_dir))
    elif backend == "s3":
        return S3Storage(settings.S3_BUCKET_NAME)
    
    raise ValueError(f"Unknown BACKEND: {backend}")


storage: BlogStorage = _build_storage()