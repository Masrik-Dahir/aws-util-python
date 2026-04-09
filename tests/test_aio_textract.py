from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.textract import (
    TextractBlock,
    TextractJobResult,
    _parse_blocks,
    _resolve_document,
    analyze_document,
    detect_document_text,
    extract_all,
    extract_form_fields,
    extract_tables,
    extract_text,
    get_document_text_detection,
    start_document_text_detection,
    wait_for_document_text_detection,
    analyze_expense,
    analyze_id,
    create_adapter,
    create_adapter_version,
    delete_adapter,
    delete_adapter_version,
    get_adapter,
    get_adapter_version,
    get_document_analysis,
    get_expense_analysis,
    get_lending_analysis,
    get_lending_analysis_summary,
    list_adapter_versions,
    list_adapters,
    list_tags_for_resource,
    start_document_analysis,
    start_expense_analysis,
    start_lending_analysis,
    tag_resource,
    untag_resource,
    update_adapter,
)


# ---------------------------------------------------------------------------
# _resolve_document helper
# ---------------------------------------------------------------------------


def test_resolve_document_bytes() -> None:
    result = _resolve_document(b"doc", None, None)
    assert result == {"Bytes": b"doc"}


def test_resolve_document_s3() -> None:
    result = _resolve_document(None, "bucket", "key")
    assert result == {"S3Object": {"Bucket": "bucket", "Name": "key"}}


def test_resolve_document_missing() -> None:
    with pytest.raises(ValueError, match="Provide either"):
        _resolve_document(None, None, None)


def test_resolve_document_partial_s3() -> None:
    with pytest.raises(ValueError, match="Provide either"):
        _resolve_document(None, "bucket", None)


# ---------------------------------------------------------------------------
# _parse_blocks helper
# ---------------------------------------------------------------------------


def test_parse_blocks_full() -> None:
    raw = [
        {
            "Id": "b1",
            "BlockType": "LINE",
            "Text": "Hello",
            "Confidence": 99.0,
            "Page": 1,
            "RowIndex": None,
            "ColumnIndex": None,
            "RowSpan": None,
            "ColumnSpan": None,
        }
    ]
    blocks = _parse_blocks(raw)
    assert len(blocks) == 1
    assert blocks[0].block_id == "b1"
    assert blocks[0].text == "Hello"


def test_parse_blocks_minimal() -> None:
    raw = [{"Id": "b2", "BlockType": "WORD"}]
    blocks = _parse_blocks(raw)
    assert blocks[0].text is None
    assert blocks[0].confidence is None
    assert blocks[0].page is None


# ---------------------------------------------------------------------------
# detect_document_text
# ---------------------------------------------------------------------------


async def test_detect_document_text_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [{"Id": "b1", "BlockType": "LINE", "Text": "Hello"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_document_text(document_bytes=b"doc")
    assert len(result) == 1
    assert result[0].block_type == "LINE"


async def test_detect_document_text_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_document_text(document_bytes=b"doc")
    assert result == []


async def test_detect_document_text_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="detect_document_text failed"):
        await detect_document_text(document_bytes=b"doc")


# ---------------------------------------------------------------------------
# analyze_document
# ---------------------------------------------------------------------------


async def test_analyze_document_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [{"Id": "b1", "BlockType": "TABLE"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await analyze_document(document_bytes=b"doc")
    assert len(result) == 1


async def test_analyze_document_custom_features(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Blocks": []}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await analyze_document(
        s3_bucket="b", s3_key="k", feature_types=["SIGNATURES"]
    )
    assert result == []


async def test_analyze_document_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="analyze_document failed"):
        await analyze_document(document_bytes=b"doc")


# ---------------------------------------------------------------------------
# start_document_text_detection
# ---------------------------------------------------------------------------


async def test_start_document_text_detection_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"JobId": "job-1"}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_document_text_detection("bucket", "key")
    assert result == "job-1"


async def test_start_document_text_detection_with_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"JobId": "job-2"}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_document_text_detection(
        "bucket", "key", output_bucket="out-bucket", output_prefix="prefix/"
    )
    assert result == "job-2"


async def test_start_document_text_detection_output_no_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"JobId": "job-3"}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_document_text_detection(
        "bucket", "key", output_bucket="out-bucket"
    )
    assert result == "job-3"


async def test_start_document_text_detection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_document_text_detection failed"):
        await start_document_text_detection("bucket", "key")


# ---------------------------------------------------------------------------
# get_document_text_detection
# ---------------------------------------------------------------------------


async def test_get_document_text_detection_single_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobStatus": "SUCCEEDED",
        "StatusMessage": "OK",
        "Blocks": [{"Id": "b1", "BlockType": "LINE", "Text": "Hi"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_document_text_detection("job-1")
    assert result.status == "SUCCEEDED"
    assert result.status_message == "OK"
    assert len(result.blocks) == 1


async def test_get_document_text_detection_paginated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "JobStatus": "SUCCEEDED",
            "Blocks": [{"Id": "b1", "BlockType": "LINE"}],
            "NextToken": "tok-1",
        },
        {
            "JobStatus": "SUCCEEDED",
            "Blocks": [{"Id": "b2", "BlockType": "WORD"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_document_text_detection("job-1")
    assert len(result.blocks) == 2


async def test_get_document_text_detection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_document_text_detection failed"):
        await get_document_text_detection("job-1")


# ---------------------------------------------------------------------------
# wait_for_document_text_detection
# ---------------------------------------------------------------------------


async def test_wait_for_document_text_detection_immediate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobStatus": "SUCCEEDED",
        "Blocks": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("aws_util.aio.textract.asyncio.sleep", AsyncMock())
    result = await wait_for_document_text_detection("job-1")
    assert result.succeeded is True


async def test_wait_for_document_text_detection_polls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"JobStatus": "IN_PROGRESS", "Blocks": []},
        {"JobStatus": "SUCCEEDED", "Blocks": []},
    ]
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("aws_util.aio.textract.asyncio.sleep", AsyncMock())
    result = await wait_for_document_text_detection("job-1")
    assert result.status == "SUCCEEDED"


async def test_wait_for_document_text_detection_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import time as _time

    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobStatus": "IN_PROGRESS",
        "Blocks": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("aws_util.aio.textract.asyncio.sleep", AsyncMock())

    call_count = 0

    def fake_monotonic() -> float:
        nonlocal call_count
        call_count += 1
        if call_count <= 1:
            return 0.0
        return 1000.0

    monkeypatch.setattr(_time, "monotonic", fake_monotonic)
    with pytest.raises(TimeoutError, match="did not finish"):
        await wait_for_document_text_detection("job-1", timeout=1.0)


async def test_wait_for_partial_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobStatus": "PARTIAL_SUCCESS",
        "Blocks": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("aws_util.aio.textract.asyncio.sleep", AsyncMock())
    result = await wait_for_document_text_detection("job-1")
    assert result.status == "PARTIAL_SUCCESS"


async def test_wait_for_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobStatus": "FAILED",
        "StatusMessage": "Error!",
        "Blocks": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("aws_util.aio.textract.asyncio.sleep", AsyncMock())
    result = await wait_for_document_text_detection("job-1")
    assert result.status == "FAILED"


# ---------------------------------------------------------------------------
# extract_text
# ---------------------------------------------------------------------------


async def test_extract_text_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {"Id": "b1", "BlockType": "LINE", "Text": "Hello"},
            {"Id": "b2", "BlockType": "LINE", "Text": "World"},
            {"Id": "b3", "BlockType": "WORD", "Text": "Hello"},
            {"Id": "b4", "BlockType": "LINE"},  # no text
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_text(document_bytes=b"doc")
    assert result == "Hello\nWorld"


# ---------------------------------------------------------------------------
# extract_tables
# ---------------------------------------------------------------------------


async def test_extract_tables_with_cells(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {
                "Id": "c1",
                "BlockType": "CELL",
                "Text": "A1",
                "Page": 1,
                "RowIndex": 1,
                "ColumnIndex": 1,
            },
            {
                "Id": "c2",
                "BlockType": "CELL",
                "Text": "A2",
                "Page": 1,
                "RowIndex": 1,
                "ColumnIndex": 2,
            },
            {
                "Id": "c3",
                "BlockType": "CELL",
                "Text": "B1",
                "Page": 1,
                "RowIndex": 2,
                "ColumnIndex": 1,
            },
            {
                "Id": "c4",
                "BlockType": "CELL",
                "Page": 1,
                "RowIndex": 2,
                "ColumnIndex": 2,
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_tables(document_bytes=b"doc")
    assert len(result) == 1
    assert result[0][0] == ["A1", "A2"]
    assert result[0][1] == ["B1", ""]


async def test_extract_tables_no_cells(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [{"Id": "b1", "BlockType": "LINE", "Text": "Hi"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_tables(document_bytes=b"doc")
    assert result == []


async def test_extract_tables_no_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cells with no page attribute default to page 1."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {
                "Id": "c1",
                "BlockType": "CELL",
                "Text": "val",
                "RowIndex": 1,
                "ColumnIndex": 1,
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_tables(document_bytes=b"doc")
    assert len(result) == 1
    assert result[0] == [["val"]]


# ---------------------------------------------------------------------------
# extract_form_fields
# ---------------------------------------------------------------------------


async def test_extract_form_fields_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {
                "Id": "kv1",
                "BlockType": "KEY_VALUE_SET",
                "Text": "Name",
            },
            {
                "Id": "kv2",
                "BlockType": "KEY_VALUE_SET",
                "Text": "Address",
            },
            {
                "Id": "kv3",
                "BlockType": "KEY_VALUE_SET",
            },  # no text
            {
                "Id": "b1",
                "BlockType": "LINE",
                "Text": "Other",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_form_fields(document_bytes=b"doc")
    assert result == {"kv1": "Name", "kv2": "Address"}


# ---------------------------------------------------------------------------
# extract_all
# ---------------------------------------------------------------------------


async def test_extract_all_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {"Id": "b1", "BlockType": "LINE", "Text": "Hello"},
            {
                "Id": "c1",
                "BlockType": "CELL",
                "Text": "A1",
                "Page": 1,
                "RowIndex": 1,
                "ColumnIndex": 1,
            },
            {
                "Id": "kv1",
                "BlockType": "KEY_VALUE_SET",
                "Text": "Name",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_all(document_bytes=b"doc")
    assert result["text"] == "Hello"
    assert len(result["tables"]) == 1
    assert result["form_fields"] == {"kv1": "Name"}


async def test_extract_all_no_cells(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [{"Id": "b1", "BlockType": "LINE", "Text": "Hello"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_all(document_bytes=b"doc")
    assert result["tables"] == []
    assert result["form_fields"] == {}


async def test_extract_all_cells_no_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cells without page default to page 1 in extract_all."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Blocks": [
            {
                "Id": "c1",
                "BlockType": "CELL",
                "Text": "val",
                "RowIndex": 1,
                "ColumnIndex": 1,
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await extract_all(document_bytes=b"doc")
    assert result["tables"] == [[["val"]]]


async def test_analyze_expense(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await analyze_expense({}, )
    mock_client.call.assert_called_once()


async def test_analyze_expense_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await analyze_expense({}, )


async def test_analyze_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await analyze_id([], )
    mock_client.call.assert_called_once()


async def test_analyze_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await analyze_id([], )


async def test_create_adapter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_adapter("test-adapter_name", [], )
    mock_client.call.assert_called_once()


async def test_create_adapter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_adapter("test-adapter_name", [], )


async def test_create_adapter_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_adapter_version("test-adapter_id", {}, {}, )
    mock_client.call.assert_called_once()


async def test_create_adapter_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_adapter_version("test-adapter_id", {}, {}, )


async def test_delete_adapter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_adapter("test-adapter_id", )
    mock_client.call.assert_called_once()


async def test_delete_adapter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_adapter("test-adapter_id", )


async def test_delete_adapter_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_adapter_version("test-adapter_id", "test-adapter_version", )
    mock_client.call.assert_called_once()


async def test_delete_adapter_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_adapter_version("test-adapter_id", "test-adapter_version", )


async def test_get_adapter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_adapter("test-adapter_id", )
    mock_client.call.assert_called_once()


async def test_get_adapter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_adapter("test-adapter_id", )


async def test_get_adapter_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_adapter_version("test-adapter_id", "test-adapter_version", )
    mock_client.call.assert_called_once()


async def test_get_adapter_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_adapter_version("test-adapter_id", "test-adapter_version", )


async def test_get_document_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_document_analysis("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_document_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_document_analysis("test-job_id", )


async def test_get_expense_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_expense_analysis("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_expense_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_expense_analysis("test-job_id", )


async def test_get_lending_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_lending_analysis("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_lending_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_lending_analysis("test-job_id", )


async def test_get_lending_analysis_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_lending_analysis_summary("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_lending_analysis_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_lending_analysis_summary("test-job_id", )


async def test_list_adapter_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_adapter_versions()
    mock_client.call.assert_called_once()


async def test_list_adapter_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_adapter_versions()


async def test_list_adapters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_adapters()
    mock_client.call.assert_called_once()


async def test_list_adapters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_adapters()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_start_document_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_document_analysis({}, [], )
    mock_client.call.assert_called_once()


async def test_start_document_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_document_analysis({}, [], )


async def test_start_expense_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_expense_analysis({}, )
    mock_client.call.assert_called_once()


async def test_start_expense_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_expense_analysis({}, )


async def test_start_lending_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_lending_analysis({}, )
    mock_client.call.assert_called_once()


async def test_start_lending_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_lending_analysis({}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_adapter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_adapter("test-adapter_id", )
    mock_client.call.assert_called_once()


async def test_update_adapter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.textract.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_adapter("test-adapter_id", )


@pytest.mark.asyncio
async def test_create_adapter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import create_adapter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await create_adapter("test-adapter_name", "test-feature_types", client_request_token="test-client_request_token", description="test-description", auto_update=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_adapter_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import create_adapter_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await create_adapter_version("test-adapter_id", {}, {}, client_request_token="test-client_request_token", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_document_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import get_document_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await get_document_analysis("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_expense_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import get_expense_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await get_expense_analysis("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_lending_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import get_lending_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await get_lending_analysis("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_adapter_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import list_adapter_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await list_adapter_versions(adapter_id="test-adapter_id", after_creation_time="test-after_creation_time", before_creation_time="test-before_creation_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_adapters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import list_adapters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await list_adapters(after_creation_time="test-after_creation_time", before_creation_time="test-before_creation_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_document_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import start_document_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await start_document_analysis("test-document_location", "test-feature_types", client_request_token="test-client_request_token", job_tag="test-job_tag", notification_channel="test-notification_channel", output_config={}, kms_key_id="test-kms_key_id", queries_config={}, adapters_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_expense_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import start_expense_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await start_expense_analysis("test-document_location", client_request_token="test-client_request_token", job_tag="test-job_tag", notification_channel="test-notification_channel", output_config={}, kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_lending_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import start_lending_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await start_lending_analysis("test-document_location", client_request_token="test-client_request_token", job_tag="test-job_tag", notification_channel="test-notification_channel", output_config={}, kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_adapter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.textract import update_adapter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.textract.async_client", lambda *a, **kw: mock_client)
    await update_adapter("test-adapter_id", description="test-description", adapter_name="test-adapter_name", auto_update=True, region_name="us-east-1")
    mock_client.call.assert_called_once()
