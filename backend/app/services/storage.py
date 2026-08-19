from pathlib import Path
from typing import Protocol
from app.config import settings

import boto3
from botocore.exceptions import ClientError


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
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY_ID.get_secret_value(),
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY.get_secret_value(),
            region_name=settings.S3_REGION,
        )

        self._cache_dir = Path(__file__).resolve().parents[2] / "blogs" / "_s3_cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def save(self, local_file_path: str) -> str:
        src = Path(local_file_path)
        key = src.name
        
        self.client.upload_file(str(src), self.bucket_name, key)
        return key

    def resolve(self, key: str) -> Path:
        dest = self._cache_dir / key
        if not dest.exists():
            try:
                self.client.download_file(self.bucket_name, key, str(dest))
            except Exception as e:
                raise FileNotFoundError(f"File not found for key: {key}") from e
        return dest

    def get_url(self, key: str) -> str | None:
        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=3600,  # URL expires in 1 hour
            )
        except ClientError:
            return None

    def exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchKey"):
                return False
            raise
            

def _build_storage() -> BlogStorage:
    backend = getattr(settings, "BACKEND", "local")

    if backend == "local":
        output_dir = Path(settings.OUTPUT_DIR)
        if not output_dir.is_absolute():
            output_dir = Path(__file__).resolve().parents[2] / output_dir
        return LocalStorage(str(output_dir))
    elif backend == "s3":
        if not settings.S3_BUCKET_NAME:
            raise ValueError("S3_BUCKET_NAME must be set when BACKEND=s3")
        return S3Storage(settings.S3_BUCKET_NAME)
    
    raise ValueError(f"Unknown BACKEND: {backend}")


storage: BlogStorage = _build_storage()