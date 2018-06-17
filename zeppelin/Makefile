run:
	docker build -t zeppelin .
	docker run \
		-v $(PWD)/tmp:/wrk \
		-e ZEPPELIN_NOTEBOOK_STORAGE="org.apache.zeppelin.notebook.repo.S3NotebookRepo" \
		-e ZEPPELIN_NOTEBOOK_S3_BUCKET="codeforces-analysis" \
		-e ZEPPELIN_NOTEBOOK_S3_USER="zeppelin" \
		-v $(HOME)/.aws:/root/.aws \
		-p 8080:8080 \
		--rm \
		--name zeppelin \
		zeppelin

c9url:
	echo https://$(C9_PID).vfs.cloud9.us-east-1.amazonaws.com

athena:
	curl -X POST -H "Content-Type: application/json" -d @config/athena.json http://localhost:8080/api/interpreter/setting

shell:
	docker exec -ti zeppelin bash
