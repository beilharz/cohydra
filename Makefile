export NS3_TAG ?= 3.30-python3
export SUMO_TAG ?= 1.4.0
SN3T_TAG ?= $(shell if [ -z "`git status --porcelain`" ]; then git rev-parse --short HEAD; else echo dirty; fi)
export SN3T_TAG := ${SN3T_TAG}

docker_build := docker build --build-arg NS3_TAG --build-arg SUMO_TAG --build-arg SN3T_TAG

.PHONY: latest ns-3 sumo testbed-base testbed testbed-dev docs

all: ns-3 sumo testbed-base testbed testbed-dev
	#
	# build tag ${SN3T_TAG}
	#

git-is-clean:
ifeq '${shell git status --porcelain}' ''
	@ # git is clean
else
	${error Git status is not clean.}
endif
	

latest: git-is-clean all
	docker tag mgjm/ns-3:${NS3_TAG} mgjm/ns-3:latest
	docker tag mgjm/sumo:${SUMO_TAG} mgjm/sumo:latest
	docker tag mgjm/sn3t:base-${SN3T_TAG} mgjm/sn3t:base
	docker tag mgjm/sn3t:${SN3T_TAG} mgjm/sn3t:latest
	docker tag mgjm/sn3t:dev-${SN3T_TAG} mgjm/sn3t:dev

ns-3:
	${docker_build} -t mgjm/ns-3:${NS3_TAG} container-images/ns-3

sumo:
	${docker_build} -t mgjm/sumo:${SUMO_TAG} container-images/sumo

testbed-base:
	${docker_build} -t mgjm/sn3t:base-${SN3T_TAG} container-images/testbed-base

testbed:
	${docker_build} -t mgjm/sn3t:${SN3T_TAG} .

testbed-dev:
	${docker_build} -t mgjm/sn3t:dev-${SN3T_TAG} container-images/testbed-dev

save: git-is-clean
	docker save \
		mgjm/ns-3:${NS3_TAG} \
		mgjm/ns-3:latest \
		mgjm/sumo:${SUMO_TAG} \
		mgjm/sumo:latest \
		mgjm/sn3t:base-${SN3T_TAG} \
		mgjm/sn3t:base \
		mgjm/sn3t:${SN3T_TAG} \
		mgjm/sn3t:latest \
		mgjm/sn3t:dev-${SN3T_TAG} \
		mgjm/sn3t:dev

docs:
	$(MAKE) -C docs
