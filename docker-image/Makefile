NAME=tjhei/burnman:v4

build:
	docker build -t ${NAME} .
	@echo "built ${NAME}"

push:
	docker push ${NAME}
	@echo "pushed ${NAME}"

#run:
#	@docker rm -f test-jenkins-slave 2>/dev/null || true
#	docker run \
#		-it --rm  -v /var/run/docker.sock:/var/run/docker.sock                \
#		--name test-jenkins-slave \
#		tjhei/test-jenkins-slave /bin/bash
.phony: build
