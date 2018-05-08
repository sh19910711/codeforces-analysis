run:
	docker build -t zeppelin .
	docker run \
		-v /tmp/zeppelin-notebooks:/zeppelin/notebook \
		-v $(HOME)/.aws:/root/.aws \
		-p 8080:$(PORT) \
		--rm \
		--name zeppelin \
		zeppelin

athena:
	curl -X POST -H "Content-Type: application/json" -d @config/athena.json http://localhost:8080/api/interpreter/setting

shell:
	docker exec -ti zeppelin bash
