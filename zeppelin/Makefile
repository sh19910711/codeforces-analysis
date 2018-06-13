run:
	docker build -t zeppelin .
	docker run \
		-v /tmp/zeppelin-notebooks:/zeppelin/notebook \
		-v $(HOME)/.aws:/root/.aws \
		-p 8080:$(PORT) \
		--rm \
		--name zeppelin \
		zeppelin

c9url:
	echo https://$(C9_PID).vfs.cloud9.us-east-1.amazonaws.com

athena:
	curl -X POST -H "Content-Type: application/json" -d @config/athena.json http://localhost:8080/api/interpreter/setting

shell:
	docker exec -ti zeppelin bash
