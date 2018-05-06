CREATE EXTERNAL TABLE IF NOT EXISTS codeforces_analysis.submissions (
  `status_id` bigint,
  `contest_id` bigint,
  `create_time` string,
  `relative_time` string,
  `problem_index` string,
  `user_name` string,
  `participant_type` string,
  `language` string,
  `verdict` string,
  `passed_test_count` bigint,
  `execution_time` bigint,
  `execution_memory` bigint
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
)
LOCATION 's3://codeforces-analysis/data/gzip/submissions/'
TBLPROPERTIES ('has_encrypted_data'='false')
;
