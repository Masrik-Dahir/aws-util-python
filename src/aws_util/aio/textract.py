"""Native async Textract utilities using the async engine."""

from __future__ import annotations

import asyncio
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.textract import (
    AnalyzeExpenseResult,
    AnalyzeIdResult,
    CreateAdapterResult,
    CreateAdapterVersionResult,
    GetAdapterResult,
    GetAdapterVersionResult,
    GetDocumentAnalysisResult,
    GetExpenseAnalysisResult,
    GetLendingAnalysisResult,
    GetLendingAnalysisSummaryResult,
    ListAdaptersResult,
    ListAdapterVersionsResult,
    ListTagsForResourceResult,
    StartDocumentAnalysisResult,
    StartExpenseAnalysisResult,
    StartLendingAnalysisResult,
    TextractBlock,
    TextractJobResult,
    UpdateAdapterResult,
)

_TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "PARTIAL_SUCCESS"}

__all__ = [
    "AnalyzeExpenseResult",
    "AnalyzeIdResult",
    "CreateAdapterResult",
    "CreateAdapterVersionResult",
    "GetAdapterResult",
    "GetAdapterVersionResult",
    "GetDocumentAnalysisResult",
    "GetExpenseAnalysisResult",
    "GetLendingAnalysisResult",
    "GetLendingAnalysisSummaryResult",
    "ListAdapterVersionsResult",
    "ListAdaptersResult",
    "ListTagsForResourceResult",
    "StartDocumentAnalysisResult",
    "StartExpenseAnalysisResult",
    "StartLendingAnalysisResult",
    "TextractBlock",
    "TextractJobResult",
    "UpdateAdapterResult",
    "analyze_document",
    "analyze_expense",
    "analyze_id",
    "create_adapter",
    "create_adapter_version",
    "delete_adapter",
    "delete_adapter_version",
    "detect_document_text",
    "extract_all",
    "extract_form_fields",
    "extract_tables",
    "extract_text",
    "get_adapter",
    "get_adapter_version",
    "get_document_analysis",
    "get_document_text_detection",
    "get_expense_analysis",
    "get_lending_analysis",
    "get_lending_analysis_summary",
    "list_adapter_versions",
    "list_adapters",
    "list_tags_for_resource",
    "start_document_analysis",
    "start_document_text_detection",
    "start_expense_analysis",
    "start_lending_analysis",
    "tag_resource",
    "untag_resource",
    "update_adapter",
    "wait_for_document_text_detection",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_document(
    document_bytes: bytes | None,
    s3_bucket: str | None,
    s3_key: str | None,
) -> dict:
    """Build the Textract Document parameter."""
    if document_bytes is not None:
        return {"Bytes": document_bytes}
    if s3_bucket and s3_key:
        return {"S3Object": {"Bucket": s3_bucket, "Name": s3_key}}
    raise ValueError("Provide either document_bytes or both s3_bucket and s3_key")


def _parse_blocks(raw: list[dict]) -> list[TextractBlock]:
    """Convert raw API block dicts to :class:`TextractBlock` models."""
    blocks: list[TextractBlock] = []
    for b in raw:
        blocks.append(
            TextractBlock(
                block_id=b["Id"],
                block_type=b["BlockType"],
                text=b.get("Text"),
                confidence=b.get("Confidence"),
                page=b.get("Page"),
                row_index=b.get("RowIndex"),
                column_index=b.get("ColumnIndex"),
                row_span=b.get("RowSpan"),
                column_span=b.get("ColumnSpan"),
            )
        )
    return blocks


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def detect_document_text(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> list[TextractBlock]:
    """Synchronously detect all text in a document (max 10 MB / 1 page for bytes).

    Args:
        document_bytes: Raw document bytes (JPEG, PNG, or single-page PDF).
        s3_bucket: Source S3 bucket (required for multi-page PDFs).
        s3_key: Source S3 object key.
        region_name: AWS region override.

    Returns:
        A list of :class:`TextractBlock` objects with detected text.

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    document = _resolve_document(document_bytes, s3_bucket, s3_key)
    try:
        resp = await client.call("DetectDocumentText", Document=document)
    except Exception as exc:
        raise wrap_aws_error(exc, "detect_document_text failed") from exc
    return _parse_blocks(resp.get("Blocks", []))


async def analyze_document(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    feature_types: list[str] | None = None,
    region_name: str | None = None,
) -> list[TextractBlock]:
    """Analyse a document for forms, tables, and signatures.

    Args:
        document_bytes: Raw document bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        feature_types: Analysis features to enable.  Choices are
            ``"TABLES"``, ``"FORMS"``, ``"SIGNATURES"``, and
            ``"LAYOUT"``.  Defaults to ``["TABLES", "FORMS"]``.
        region_name: AWS region override.

    Returns:
        A list of :class:`TextractBlock` objects.

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    document = _resolve_document(document_bytes, s3_bucket, s3_key)
    try:
        resp = await client.call(
            "AnalyzeDocument",
            Document=document,
            FeatureTypes=feature_types or ["TABLES", "FORMS"],
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "analyze_document failed") from exc
    return _parse_blocks(resp.get("Blocks", []))


async def start_document_text_detection(
    s3_bucket: str,
    s3_key: str,
    output_bucket: str | None = None,
    output_prefix: str | None = None,
    region_name: str | None = None,
) -> str:
    """Start an asynchronous Textract text detection job for multi-page documents.

    Args:
        s3_bucket: Source S3 bucket containing the document.
        s3_key: Source S3 object key (PDF or TIFF).
        output_bucket: Optional S3 bucket for job output.
        output_prefix: Optional S3 prefix for job output.
        region_name: AWS region override.

    Returns:
        The Textract job ID.

    Raises:
        RuntimeError: If the job submission fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {
        "DocumentLocation": {"S3Object": {"Bucket": s3_bucket, "Name": s3_key}}
    }
    if output_bucket:
        kwargs["OutputConfig"] = {"S3Bucket": output_bucket}
        if output_prefix:
            kwargs["OutputConfig"]["S3Prefix"] = output_prefix
    try:
        resp = await client.call("StartDocumentTextDetection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"start_document_text_detection failed for s3://{s3_bucket}/{s3_key}"
        ) from exc
    return resp["JobId"]


async def get_document_text_detection(
    job_id: str,
    region_name: str | None = None,
) -> TextractJobResult:
    """Fetch the results of an asynchronous Textract text detection job.

    Handles pagination automatically.

    Args:
        job_id: Job ID returned by :func:`start_document_text_detection`.
        region_name: AWS region override.

    Returns:
        A :class:`TextractJobResult` with current status and all blocks.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    blocks: list[TextractBlock] = []
    status = "IN_PROGRESS"
    status_message: str | None = None
    kwargs: dict[str, Any] = {"JobId": job_id}
    try:
        while True:
            resp = await client.call("GetDocumentTextDetection", **kwargs)
            status = resp["JobStatus"]
            status_message = resp.get("StatusMessage")
            blocks.extend(_parse_blocks(resp.get("Blocks", [])))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_document_text_detection failed for job {job_id!r}") from exc
    return TextractJobResult(
        job_id=job_id,
        status=status,
        status_message=status_message,
        blocks=blocks,
    )


async def wait_for_document_text_detection(
    job_id: str,
    poll_interval: float = 5.0,
    timeout: float = 600.0,
    region_name: str | None = None,
) -> TextractJobResult:
    """Poll until a Textract text detection job completes.

    Args:
        job_id: Job ID to wait for.
        poll_interval: Seconds between status checks (default ``5``).
        timeout: Maximum seconds to wait (default ``600``).
        region_name: AWS region override.

    Returns:
        The final :class:`TextractJobResult`.

    Raises:
        TimeoutError: If the job does not finish within *timeout*.
    """
    import time

    deadline = time.monotonic() + timeout
    while True:
        result = await get_document_text_detection(job_id, region_name=region_name)
        if result.status in _TERMINAL_STATUSES:
            return result
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Textract job {job_id!r} did not finish within {timeout}s")
        await asyncio.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def extract_text(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> str:
    """Extract all raw text from a document as a single string.

    Calls :func:`detect_document_text` and joins all LINE-type blocks in
    reading order.

    Args:
        document_bytes: Raw document bytes (JPEG, PNG, or single-page PDF).
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        region_name: AWS region override.

    Returns:
        All detected text as a newline-separated string.

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    blocks = await detect_document_text(
        document_bytes=document_bytes,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        region_name=region_name,
    )
    lines = [b.text for b in blocks if b.block_type == "LINE" and b.text]
    return "\n".join(lines)


async def extract_tables(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> list[list[list[str]]]:
    """Extract tables from a document as nested lists.

    Each table is a list of rows; each row is a list of cell strings.  Empty
    or undetected cells are represented as empty strings.

    Args:
        document_bytes: Raw document bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        region_name: AWS region override.

    Returns:
        A list of tables.  Each table is ``list[row]``; each row is
        ``list[str]``.

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    blocks = await analyze_document(
        document_bytes=document_bytes,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        feature_types=["TABLES"],
        region_name=region_name,
    )
    tables: list[list[list[str]]] = []
    cells = [b for b in blocks if b.block_type == "CELL"]

    if not cells:
        return tables

    pages: dict[int, list[TextractBlock]] = {}
    for cell in cells:
        page = cell.page or 1
        pages.setdefault(page, []).append(cell)

    for page_cells in pages.values():
        max_row = max((c.row_index or 0) for c in page_cells)
        max_col = max((c.column_index or 0) for c in page_cells)
        grid: list[list[str]] = [[""] * max_col for _ in range(max_row)]
        for cell in page_cells:
            r = (cell.row_index or 1) - 1
            c = (cell.column_index or 1) - 1
            if 0 <= r < max_row and 0 <= c < max_col:
                grid[r][c] = cell.text or ""
        tables.append(grid)

    return tables


async def extract_form_fields(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> dict[str, str]:
    """Extract key-value form fields from a document.

    Calls :func:`analyze_document` with ``FORMS`` feature and pairs each
    KEY block with its associated VALUE block.

    Args:
        document_bytes: Raw document bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        region_name: AWS region override.

    Returns:
        A dict mapping form field key -> value (both as strings).

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    blocks = await analyze_document(
        document_bytes=document_bytes,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        feature_types=["FORMS"],
        region_name=region_name,
    )
    key_blocks = [b for b in blocks if b.block_type == "KEY_VALUE_SET" and b.text]
    return {b.block_id: b.text for b in key_blocks if b.text}


async def extract_all(
    document_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Extract text, tables, and form fields from a document in one call.

    Runs :func:`analyze_document` once with all features enabled and returns
    a dict with ``"text"``, ``"tables"``, and ``"form_fields"`` keys.

    Args:
        document_bytes: Raw document bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        region_name: AWS region override.

    Returns:
        A dict with keys:
        - ``"text"`` -- newline-separated plain text (str)
        - ``"tables"`` -- list of table grids (list[list[list[str]]])
        - ``"form_fields"`` -- key/value pairs from forms (dict[str, str])

    Raises:
        ValueError: If neither document source is provided.
        RuntimeError: If the API call fails.
    """
    blocks = await analyze_document(
        document_bytes=document_bytes,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        feature_types=["TABLES", "FORMS"],
        region_name=region_name,
    )

    # --- text ---
    lines = [b.text for b in blocks if b.block_type == "LINE" and b.text]
    text = "\n".join(lines)

    # --- tables ---
    cells = [b for b in blocks if b.block_type == "CELL"]
    tables: list[list[list[str]]] = []
    if cells:
        pages: dict[int, list[TextractBlock]] = {}
        for cell in cells:
            pages.setdefault(cell.page or 1, []).append(cell)
        for page_cells in pages.values():
            max_row = max((c.row_index or 0) for c in page_cells)
            max_col = max((c.column_index or 0) for c in page_cells)
            grid: list[list[str]] = [[""] * max_col for _ in range(max_row)]
            for cell in page_cells:
                r = (cell.row_index or 1) - 1
                c = (cell.column_index or 1) - 1
                if 0 <= r < max_row and 0 <= c < max_col:
                    grid[r][c] = cell.text or ""
            tables.append(grid)

    # --- form fields ---
    key_blocks = [b for b in blocks if b.block_type == "KEY_VALUE_SET" and b.text]
    form_fields = {b.block_id: b.text for b in key_blocks if b.text}

    return {"text": text, "tables": tables, "form_fields": form_fields}


async def analyze_expense(
    document: dict[str, Any],
    region_name: str | None = None,
) -> AnalyzeExpenseResult:
    """Analyze expense.

    Args:
        document: Document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Document"] = document
    try:
        resp = await client.call("AnalyzeExpense", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to analyze expense") from exc
    return AnalyzeExpenseResult(
        document_metadata=resp.get("DocumentMetadata"),
        expense_documents=resp.get("ExpenseDocuments"),
    )


async def analyze_id(
    document_pages: list[dict[str, Any]],
    region_name: str | None = None,
) -> AnalyzeIdResult:
    """Analyze id.

    Args:
        document_pages: Document pages.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentPages"] = document_pages
    try:
        resp = await client.call("AnalyzeID", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to analyze id") from exc
    return AnalyzeIdResult(
        identity_documents=resp.get("IdentityDocuments"),
        document_metadata=resp.get("DocumentMetadata"),
        analyze_id_model_version=resp.get("AnalyzeIDModelVersion"),
    )


async def create_adapter(
    adapter_name: str,
    feature_types: list[str],
    *,
    client_request_token: str | None = None,
    description: str | None = None,
    auto_update: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAdapterResult:
    """Create adapter.

    Args:
        adapter_name: Adapter name.
        feature_types: Feature types.
        client_request_token: Client request token.
        description: Description.
        auto_update: Auto update.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterName"] = adapter_name
    kwargs["FeatureTypes"] = feature_types
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if description is not None:
        kwargs["Description"] = description
    if auto_update is not None:
        kwargs["AutoUpdate"] = auto_update
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateAdapter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create adapter") from exc
    return CreateAdapterResult(
        adapter_id=resp.get("AdapterId"),
    )


async def create_adapter_version(
    adapter_id: str,
    dataset_config: dict[str, Any],
    output_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    kms_key_id: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAdapterVersionResult:
    """Create adapter version.

    Args:
        adapter_id: Adapter id.
        dataset_config: Dataset config.
        output_config: Output config.
        client_request_token: Client request token.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    kwargs["DatasetConfig"] = dataset_config
    kwargs["OutputConfig"] = output_config
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateAdapterVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create adapter version") from exc
    return CreateAdapterVersionResult(
        adapter_id=resp.get("AdapterId"),
        adapter_version=resp.get("AdapterVersion"),
    )


async def delete_adapter(
    adapter_id: str,
    region_name: str | None = None,
) -> None:
    """Delete adapter.

    Args:
        adapter_id: Adapter id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    try:
        await client.call("DeleteAdapter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete adapter") from exc
    return None


async def delete_adapter_version(
    adapter_id: str,
    adapter_version: str,
    region_name: str | None = None,
) -> None:
    """Delete adapter version.

    Args:
        adapter_id: Adapter id.
        adapter_version: Adapter version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    kwargs["AdapterVersion"] = adapter_version
    try:
        await client.call("DeleteAdapterVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete adapter version") from exc
    return None


async def get_adapter(
    adapter_id: str,
    region_name: str | None = None,
) -> GetAdapterResult:
    """Get adapter.

    Args:
        adapter_id: Adapter id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    try:
        resp = await client.call("GetAdapter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get adapter") from exc
    return GetAdapterResult(
        adapter_id=resp.get("AdapterId"),
        adapter_name=resp.get("AdapterName"),
        creation_time=resp.get("CreationTime"),
        description=resp.get("Description"),
        feature_types=resp.get("FeatureTypes"),
        auto_update=resp.get("AutoUpdate"),
        tags=resp.get("Tags"),
    )


async def get_adapter_version(
    adapter_id: str,
    adapter_version: str,
    region_name: str | None = None,
) -> GetAdapterVersionResult:
    """Get adapter version.

    Args:
        adapter_id: Adapter id.
        adapter_version: Adapter version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    kwargs["AdapterVersion"] = adapter_version
    try:
        resp = await client.call("GetAdapterVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get adapter version") from exc
    return GetAdapterVersionResult(
        adapter_id=resp.get("AdapterId"),
        adapter_version=resp.get("AdapterVersion"),
        creation_time=resp.get("CreationTime"),
        feature_types=resp.get("FeatureTypes"),
        status=resp.get("Status"),
        status_message=resp.get("StatusMessage"),
        dataset_config=resp.get("DatasetConfig"),
        kms_key_id=resp.get("KMSKeyId"),
        output_config=resp.get("OutputConfig"),
        evaluation_metrics=resp.get("EvaluationMetrics"),
        tags=resp.get("Tags"),
    )


async def get_document_analysis(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetDocumentAnalysisResult:
    """Get document analysis.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetDocumentAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get document analysis") from exc
    return GetDocumentAnalysisResult(
        document_metadata=resp.get("DocumentMetadata"),
        job_status=resp.get("JobStatus"),
        next_token=resp.get("NextToken"),
        blocks=resp.get("Blocks"),
        warnings=resp.get("Warnings"),
        status_message=resp.get("StatusMessage"),
        analyze_document_model_version=resp.get("AnalyzeDocumentModelVersion"),
    )


async def get_expense_analysis(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetExpenseAnalysisResult:
    """Get expense analysis.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetExpenseAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get expense analysis") from exc
    return GetExpenseAnalysisResult(
        document_metadata=resp.get("DocumentMetadata"),
        job_status=resp.get("JobStatus"),
        next_token=resp.get("NextToken"),
        expense_documents=resp.get("ExpenseDocuments"),
        warnings=resp.get("Warnings"),
        status_message=resp.get("StatusMessage"),
        analyze_expense_model_version=resp.get("AnalyzeExpenseModelVersion"),
    )


async def get_lending_analysis(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetLendingAnalysisResult:
    """Get lending analysis.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetLendingAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get lending analysis") from exc
    return GetLendingAnalysisResult(
        document_metadata=resp.get("DocumentMetadata"),
        job_status=resp.get("JobStatus"),
        next_token=resp.get("NextToken"),
        results=resp.get("Results"),
        warnings=resp.get("Warnings"),
        status_message=resp.get("StatusMessage"),
        analyze_lending_model_version=resp.get("AnalyzeLendingModelVersion"),
    )


async def get_lending_analysis_summary(
    job_id: str,
    region_name: str | None = None,
) -> GetLendingAnalysisSummaryResult:
    """Get lending analysis summary.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = await client.call("GetLendingAnalysisSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get lending analysis summary") from exc
    return GetLendingAnalysisSummaryResult(
        document_metadata=resp.get("DocumentMetadata"),
        job_status=resp.get("JobStatus"),
        summary=resp.get("Summary"),
        warnings=resp.get("Warnings"),
        status_message=resp.get("StatusMessage"),
        analyze_lending_model_version=resp.get("AnalyzeLendingModelVersion"),
    )


async def list_adapter_versions(
    *,
    adapter_id: str | None = None,
    after_creation_time: str | None = None,
    before_creation_time: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAdapterVersionsResult:
    """List adapter versions.

    Args:
        adapter_id: Adapter id.
        after_creation_time: After creation time.
        before_creation_time: Before creation time.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    if adapter_id is not None:
        kwargs["AdapterId"] = adapter_id
    if after_creation_time is not None:
        kwargs["AfterCreationTime"] = after_creation_time
    if before_creation_time is not None:
        kwargs["BeforeCreationTime"] = before_creation_time
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListAdapterVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list adapter versions") from exc
    return ListAdapterVersionsResult(
        adapter_versions=resp.get("AdapterVersions"),
        next_token=resp.get("NextToken"),
    )


async def list_adapters(
    *,
    after_creation_time: str | None = None,
    before_creation_time: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAdaptersResult:
    """List adapters.

    Args:
        after_creation_time: After creation time.
        before_creation_time: Before creation time.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    if after_creation_time is not None:
        kwargs["AfterCreationTime"] = after_creation_time
    if before_creation_time is not None:
        kwargs["BeforeCreationTime"] = before_creation_time
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListAdapters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list adapters") from exc
    return ListAdaptersResult(
        adapters=resp.get("Adapters"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def start_document_analysis(
    document_location: dict[str, Any],
    feature_types: list[str],
    *,
    client_request_token: str | None = None,
    job_tag: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    output_config: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    queries_config: dict[str, Any] | None = None,
    adapters_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartDocumentAnalysisResult:
    """Start document analysis.

    Args:
        document_location: Document location.
        feature_types: Feature types.
        client_request_token: Client request token.
        job_tag: Job tag.
        notification_channel: Notification channel.
        output_config: Output config.
        kms_key_id: Kms key id.
        queries_config: Queries config.
        adapters_config: Adapters config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentLocation"] = document_location
    kwargs["FeatureTypes"] = feature_types
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if output_config is not None:
        kwargs["OutputConfig"] = output_config
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    if queries_config is not None:
        kwargs["QueriesConfig"] = queries_config
    if adapters_config is not None:
        kwargs["AdaptersConfig"] = adapters_config
    try:
        resp = await client.call("StartDocumentAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start document analysis") from exc
    return StartDocumentAnalysisResult(
        job_id=resp.get("JobId"),
    )


async def start_expense_analysis(
    document_location: dict[str, Any],
    *,
    client_request_token: str | None = None,
    job_tag: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    output_config: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> StartExpenseAnalysisResult:
    """Start expense analysis.

    Args:
        document_location: Document location.
        client_request_token: Client request token.
        job_tag: Job tag.
        notification_channel: Notification channel.
        output_config: Output config.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentLocation"] = document_location
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if output_config is not None:
        kwargs["OutputConfig"] = output_config
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    try:
        resp = await client.call("StartExpenseAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start expense analysis") from exc
    return StartExpenseAnalysisResult(
        job_id=resp.get("JobId"),
    )


async def start_lending_analysis(
    document_location: dict[str, Any],
    *,
    client_request_token: str | None = None,
    job_tag: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    output_config: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> StartLendingAnalysisResult:
    """Start lending analysis.

    Args:
        document_location: Document location.
        client_request_token: Client request token.
        job_tag: Job tag.
        notification_channel: Notification channel.
        output_config: Output config.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentLocation"] = document_location
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if output_config is not None:
        kwargs["OutputConfig"] = output_config
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    try:
        resp = await client.call("StartLendingAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start lending analysis") from exc
    return StartLendingAnalysisResult(
        job_id=resp.get("JobId"),
    )


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_adapter(
    adapter_id: str,
    *,
    description: str | None = None,
    adapter_name: str | None = None,
    auto_update: str | None = None,
    region_name: str | None = None,
) -> UpdateAdapterResult:
    """Update adapter.

    Args:
        adapter_id: Adapter id.
        description: Description.
        adapter_name: Adapter name.
        auto_update: Auto update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("textract", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdapterId"] = adapter_id
    if description is not None:
        kwargs["Description"] = description
    if adapter_name is not None:
        kwargs["AdapterName"] = adapter_name
    if auto_update is not None:
        kwargs["AutoUpdate"] = auto_update
    try:
        resp = await client.call("UpdateAdapter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update adapter") from exc
    return UpdateAdapterResult(
        adapter_id=resp.get("AdapterId"),
        adapter_name=resp.get("AdapterName"),
        creation_time=resp.get("CreationTime"),
        description=resp.get("Description"),
        feature_types=resp.get("FeatureTypes"),
        auto_update=resp.get("AutoUpdate"),
    )
