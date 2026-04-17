"""Integration tests for aws_util.data_flow_etl against LocalStack."""
from __future__ import annotations

import json
import time

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. s3_event_to_dynamodb
# ---------------------------------------------------------------------------


class TestS3EventToDynamodb:
    def test_writes_event(self, s3_bucket, dynamodb_table):
        from aws_util.data_flow_etl import s3_event_to_dynamodb

        # The dynamodb_table fixture has pk (HASH) + sk (RANGE) key schema.
        # s3_event_to_dynamodb reads JSON from S3 and batch-writes to DDB using
        # _to_ddb_item, so data must include pk and sk fields.
        s3 = ls_client("s3")
        records = [
            {"pk": "event-1", "sk": "2024-01-01", "data": "hello"},
            {"pk": "event-2", "sk": "2024-01-02", "data": "world"},
        ]
        s3.put_object(
            Bucket=s3_bucket,
            Key="events/test.json",
            Body=json.dumps(records),
        )

        result = s3_event_to_dynamodb(
            bucket=s3_bucket,
            key="events/test.json",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert result.records_written >= 1

        # Verify DynamoDB items
        ddb = ls_client("dynamodb")
        scan = ddb.scan(TableName=dynamodb_table)
        assert scan["Count"] >= 1


# ---------------------------------------------------------------------------
# 2. s3_csv_to_dynamodb_bulk
# ---------------------------------------------------------------------------


class TestS3CsvToDynamodbBulk:
    def test_loads_csv(self, s3_bucket, dynamodb_pk_table):
        from aws_util.data_flow_etl import s3_csv_to_dynamodb_bulk

        csv_data = "pk,name,value\nitem-1,Alice,100\nitem-2,Bob,200\n"
        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="data.csv", Body=csv_data.encode())

        # s3_csv_to_dynamodb_bulk takes column_mapping (optional), not pk_column
        result = s3_csv_to_dynamodb_bulk(
            bucket=s3_bucket,
            key="data.csv",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert result.records_written >= 2


# ---------------------------------------------------------------------------
# 3. cross_region_s3_replicator
# ---------------------------------------------------------------------------


class TestCrossRegionS3Replicator:
    def test_replicates_object(self, s3_bucket):
        from aws_util.data_flow_etl import cross_region_s3_replicator

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="rep/file-0.txt", Body="data-0")

        dest_bucket = f"test-dest-repl-{int(time.time())}"
        s3.create_bucket(Bucket=dest_bucket)

        # cross_region_s3_replicator takes source_bucket, source_key, dest_bucket,
        # dest_region, dest_key (optional), sns_topic_arn (optional), source_region (optional)
        result = cross_region_s3_replicator(
            source_bucket=s3_bucket,
            source_key="rep/file-0.txt",
            dest_bucket=dest_bucket,
            dest_region=REGION,
            dest_key="replicated/file-0.txt",
            source_region=REGION,
        )
        assert result.source_bucket == s3_bucket
        assert result.source_key == "rep/file-0.txt"
        assert result.dest_bucket == dest_bucket
        assert result.dest_key == "replicated/file-0.txt"
        assert result.dest_region == REGION

        # Verify destination
        obj = s3.get_object(Bucket=dest_bucket, Key="replicated/file-0.txt")
        assert obj["Body"].read().decode() == "data-0"

        # Cleanup
        s3.delete_object(Bucket=dest_bucket, Key="replicated/file-0.txt")
        s3.delete_bucket(Bucket=dest_bucket)


# ---------------------------------------------------------------------------
# 4. etl_status_tracker
# ---------------------------------------------------------------------------


class TestEtlStatusTracker:
    def test_tracks_status(self, dynamodb_table):
        from aws_util.data_flow_etl import etl_status_tracker

        # etl_status_tracker takes: table_name, pipeline_id, step_name, status, metadata, ...
        result = etl_status_tracker(
            table_name=dynamodb_table,
            pipeline_id="test-job-001",
            step_name="extract",
            status="RUNNING",
            metadata={"source": "s3", "destination": "dynamodb"},
            region_name=REGION,
        )
        assert result.pipeline_id == "test-job-001"
        assert result.step_name == "extract"
        assert result.status == "RUNNING"

        # Verify stored in DynamoDB
        ddb = ls_client("dynamodb")
        scan = ddb.scan(TableName=dynamodb_table)
        assert scan["Count"] >= 1


# ---------------------------------------------------------------------------
# 5. dynamodb_stream_to_s3_archive
# ---------------------------------------------------------------------------


class TestDynamodbStreamToS3Archive:
    def test_archives_records(self, s3_bucket):
        from aws_util.data_flow_etl import dynamodb_stream_to_s3_archive

        # dynamodb_stream_to_s3_archive takes records (list of dicts), bucket, prefix
        # The records are DynamoDB stream event records (as from event["Records"])
        records = [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "Keys": {"pk": {"S": f"archive-{i}"}},
                    "NewImage": {"pk": {"S": f"archive-{i}"}, "val": {"S": f"data-{i}"}},
                },
            }
            for i in range(5)
        ]

        result = dynamodb_stream_to_s3_archive(
            records=records,
            bucket=s3_bucket,
            prefix="archives",
            region_name=REGION,
        )
        assert result.records_archived == 5
        assert result.bucket == s3_bucket
        assert result.key.startswith("archives/")


# ---------------------------------------------------------------------------
# 6. s3_multipart_upload_manager
# ---------------------------------------------------------------------------


class TestS3MultipartUploadManager:
    def test_uploads_data(self, s3_bucket):
        from aws_util.data_flow_etl import s3_multipart_upload_manager

        # s3_multipart_upload_manager takes bucket, key, data (bytes), ...
        test_data = b"Hello, this is test data for multipart upload manager."

        result = s3_multipart_upload_manager(
            bucket=s3_bucket,
            key="uploads/test-file.bin",
            data=test_data,
            region_name=REGION,
        )
        assert result.bucket == s3_bucket
        assert result.key == "uploads/test-file.bin"
        assert result.parts_uploaded >= 1
        assert result.total_bytes == len(test_data)

        # Verify file was uploaded
        s3 = ls_client("s3")
        obj = s3.get_object(Bucket=s3_bucket, Key="uploads/test-file.bin")
        assert obj["Body"].read() == test_data


# ---------------------------------------------------------------------------
# 7. dynamodb_stream_to_opensearch
# ---------------------------------------------------------------------------


class TestDynamodbStreamToOpensearch:
    @pytest.mark.skip(reason="OpenSearch not available in LocalStack community")
    def test_indexes_records(self):
        from aws_util.data_flow_etl import dynamodb_stream_to_opensearch

        records = [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "Keys": {"pk": {"S": "os-1"}},
                    "NewImage": {"pk": {"S": "os-1"}, "name": {"S": "Alice"}},
                },
            },
        ]
        result = dynamodb_stream_to_opensearch(
            records=records,
            opensearch_endpoint="http://localhost:9200",
            index_name="test-index",
            id_key="pk",
            region_name=REGION,
        )
        assert isinstance(result.indexed, int)
        assert isinstance(result.failed, int)
        assert result.index_name == "test-index"


# ---------------------------------------------------------------------------
# 8. kinesis_to_firehose_transformer
# ---------------------------------------------------------------------------


class TestKinesisToFirehoseTransformer:
    def test_transforms_records(self, s3_bucket):
        from aws_util.data_flow_etl import kinesis_to_firehose_transformer

        kinesis = ls_client("kinesis")
        firehose = ls_client("firehose")
        iam = ls_client("iam")

        stream_name = f"test-kinesis-stream-{int(time.time())}"
        delivery_name = f"test-firehose-{int(time.time())}"

        # Create Kinesis stream
        try:
            kinesis.create_stream(StreamName=stream_name, ShardCount=1)
        except Exception:
            pass

        # Wait for stream to become ACTIVE
        for _ in range(30):
            desc = kinesis.describe_stream(StreamName=stream_name)
            if desc["StreamDescription"]["StreamStatus"] == "ACTIVE":
                break
            time.sleep(1)

        # Create a minimal IAM role for Firehose
        import json as _json

        role_name = f"test-firehose-role-{int(time.time())}"
        trust_policy = _json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "firehose.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }],
        })
        try:
            role_resp = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=trust_policy,
            )
            role_arn = role_resp["Role"]["Arn"]
        except Exception:
            role_arn = f"arn:aws:iam::000000000000:role/{role_name}"

        # Create Firehose delivery stream pointing at S3
        try:
            firehose.create_delivery_stream(
                DeliveryStreamName=delivery_name,
                S3DestinationConfiguration={
                    "RoleARN": role_arn,
                    "BucketARN": f"arn:aws:s3:::{s3_bucket}",
                    "Prefix": "firehose-output/",
                },
            )
        except Exception:
            pass

        # Wait a moment for the delivery stream
        time.sleep(2)

        # Put records into Kinesis
        for i in range(3):
            kinesis.put_record(
                StreamName=stream_name,
                Data=_json.dumps({"id": i, "value": f"record-{i}"}).encode(),
                PartitionKey="pk",
            )

        # Run the transformer
        result = kinesis_to_firehose_transformer(
            stream_name=stream_name,
            delivery_stream=delivery_name,
            shard_iterator_type="TRIM_HORIZON",
            max_records=100,
            region_name=REGION,
        )
        assert result.records_read >= 3
        assert result.records_written >= 1
        assert result.stream_name == stream_name
        assert result.delivery_stream == delivery_name

        # Cleanup
        try:
            kinesis.delete_stream(StreamName=stream_name, EnforceConsumerDeletion=True)
        except Exception:
            pass
        try:
            firehose.delete_delivery_stream(DeliveryStreamName=delivery_name)
        except Exception:
            pass
        try:
            iam.delete_role(RoleName=role_name)
        except Exception:
            pass

    def test_with_transform_function(self, s3_bucket):
        from aws_util.data_flow_etl import kinesis_to_firehose_transformer

        kinesis = ls_client("kinesis")
        firehose = ls_client("firehose")
        iam = ls_client("iam")

        stream_name = f"test-kin-xform-{int(time.time())}"
        delivery_name = f"test-fh-xform-{int(time.time())}"

        import json as _json

        # Create Kinesis stream
        try:
            kinesis.create_stream(StreamName=stream_name, ShardCount=1)
        except Exception:
            pass

        for _ in range(30):
            desc = kinesis.describe_stream(StreamName=stream_name)
            if desc["StreamDescription"]["StreamStatus"] == "ACTIVE":
                break
            time.sleep(1)

        role_name = f"test-fh-xform-role-{int(time.time())}"
        trust_policy = _json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "firehose.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }],
        })
        try:
            role_resp = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=trust_policy,
            )
            role_arn = role_resp["Role"]["Arn"]
        except Exception:
            role_arn = f"arn:aws:iam::000000000000:role/{role_name}"

        try:
            firehose.create_delivery_stream(
                DeliveryStreamName=delivery_name,
                S3DestinationConfiguration={
                    "RoleARN": role_arn,
                    "BucketARN": f"arn:aws:s3:::{s3_bucket}",
                    "Prefix": "firehose-xform/",
                },
            )
        except Exception:
            pass

        time.sleep(2)

        kinesis.put_record(
            StreamName=stream_name,
            Data=_json.dumps({"id": 1, "value": "original"}).encode(),
            PartitionKey="pk",
        )

        # Transform function that adds a field
        def add_processed_flag(record):
            record["processed"] = True
            return record

        result = kinesis_to_firehose_transformer(
            stream_name=stream_name,
            delivery_stream=delivery_name,
            transform_fn=add_processed_flag,
            shard_iterator_type="TRIM_HORIZON",
            max_records=10,
            region_name=REGION,
        )
        assert result.records_read >= 1
        assert result.records_written >= 1

        # Cleanup
        try:
            kinesis.delete_stream(StreamName=stream_name, EnforceConsumerDeletion=True)
        except Exception:
            pass
        try:
            firehose.delete_delivery_stream(DeliveryStreamName=delivery_name)
        except Exception:
            pass
        try:
            iam.delete_role(RoleName=role_name)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# 9. data_lake_partition_manager
# ---------------------------------------------------------------------------


class TestDataLakePartitionManager:
    @pytest.mark.skip(reason="Glue not available in LocalStack community")
    def test_adds_partitions(self):
        from aws_util.data_flow_etl import data_lake_partition_manager

        result = data_lake_partition_manager(
            database="test_db",
            table="test_table",
            s3_location="s3://test-bucket/data/",
            partition_values=[
                {"values": ["2024", "01"], "location": "s3://test-bucket/data/year=2024/month=01/"},
            ],
            region_name=REGION,
        )
        assert isinstance(result.partitions_added, int)
        assert result.database == "test_db"
        assert result.table == "test_table"


# ---------------------------------------------------------------------------
# 10. repair_partitions
# ---------------------------------------------------------------------------


class TestRepairPartitions:
    @pytest.mark.skip(reason="Athena not available in LocalStack community")
    def test_repairs_partitions(self):
        from aws_util.data_flow_etl import repair_partitions

        result = repair_partitions(
            database="test_db",
            table="test_table",
            region_name=REGION,
        )
        assert result.database == "test_db"
        assert result.table == "test_table"
        assert result.partitions_repaired >= 0


# ---------------------------------------------------------------------------
# 11. msk_topic_to_s3_archiver
# ---------------------------------------------------------------------------


class TestMskTopicToS3Archiver:
    @pytest.mark.skip(reason="MSK not available in LocalStack community")
    def test_archives_topic(self, s3_bucket):
        from aws_util.data_flow_etl import msk_topic_to_s3_archiver

        result = msk_topic_to_s3_archiver(
            cluster_arn="arn:aws:kafka:us-east-1:000000000000:cluster/test-cluster/uuid",
            topic_name="test-topic",
            bucket=s3_bucket,
            key_prefix="msk-archive",
            region_name=REGION,
        )
        assert isinstance(result.cluster_arn, str)
        assert isinstance(result.bootstrap_brokers, str)
        assert isinstance(result.s3_config_key, str)
        assert isinstance(result.config_written, bool)


# ---------------------------------------------------------------------------
# 12. msk_schema_registry_enforcer
# ---------------------------------------------------------------------------


class TestMskSchemaRegistryEnforcer:
    @pytest.mark.skip(reason="Glue Schema Registry not available in LocalStack community")
    def test_validates_schema(self, sqs_queue):
        from aws_util.data_flow_etl import msk_schema_registry_enforcer

        result = msk_schema_registry_enforcer(
            registry_name="test-registry",
            schema_name="test-schema",
            message_payload='{"name": "Alice", "age": 30}',
            dlq_url=sqs_queue,
            region_name=REGION,
        )
        assert isinstance(result.schema_name, str)
        assert isinstance(result.valid, bool)
        assert isinstance(result.schema_version, int)


# ---------------------------------------------------------------------------
# 13. documentdb_change_stream_to_sqs
# ---------------------------------------------------------------------------


class TestDocumentdbChangeStreamToSqs:
    @pytest.mark.skip(reason="DocumentDB not available in LocalStack community")
    def test_streams_changes(self, sqs_queue):
        from aws_util.data_flow_etl import documentdb_change_stream_to_sqs

        result = documentdb_change_stream_to_sqs(
            cluster_identifier="test-docdb-cluster",
            queue_url=sqs_queue,
            collection_name="test-collection",
            region_name=REGION,
        )
        assert isinstance(result.cluster_endpoint, str)
        assert isinstance(result.reader_endpoint, str)
        assert isinstance(result.config_message_id, str)


# ---------------------------------------------------------------------------
# 14. neptune_graph_backup_to_s3
# ---------------------------------------------------------------------------


class TestNeptuneGraphBackupToS3:
    @pytest.mark.skip(reason="Neptune not available in LocalStack community")
    def test_creates_backup(self, dynamodb_pk_table):
        from aws_util.data_flow_etl import neptune_graph_backup_to_s3

        result = neptune_graph_backup_to_s3(
            cluster_identifier="test-neptune-cluster",
            snapshot_identifier="test-snapshot",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert isinstance(result.snapshot_arn, str)
        assert isinstance(result.status, str)


# ---------------------------------------------------------------------------
# 15. keyspaces_ttl_enforcer
# ---------------------------------------------------------------------------


class TestKeyspacesTtlEnforcer:
    @pytest.mark.skip(reason="Keyspaces not available in LocalStack community")
    def test_enforces_ttl(self):
        from aws_util.data_flow_etl import keyspaces_ttl_enforcer

        result = keyspaces_ttl_enforcer(
            keyspace_name="test_keyspace",
            table_name="test_table",
            ttl_column="expires_at",
            ttl_enabled=True,
            region_name=REGION,
        )
        assert isinstance(result.table_name, str)
        assert isinstance(result.ttl_status, str)
        assert isinstance(result.ttl_column, str)
        assert isinstance(result.metric_published, bool)
