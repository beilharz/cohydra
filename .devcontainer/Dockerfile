ARG SN3T_TAG=

FROM mgjm/sn3t:base${SN3T_TAG:+-$SN3T_TAG}

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	graphviz \
	make \
	&& \
	apt-get autoremove -y && \
	apt-get clean -y && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
	pylint \
	rope \
	sphinx \
	sphinx-rtd-theme \
	sphinx-autopackagesummary \
	&& true

WORKDIR /root/testbed
ENV PATH=${PATH}:/root/testbed/tools
RUN ln -s /root/testbed/testbed $PYTHONPATH/testbed
