# testbed


## Contributors

 - Malte Andersch
 - Arne Boockmeyer
 - Felix Gohla
 - Martin Michaelis
 - Benedikt Schenkel

## Installation

### Installation With Docker

The testbed can be obtained via docker.
The easiest solution is using the VSCode *Remote - Containers* extension.
After cloning the repository and opening it in the container, your scenarios will by executing them with `python3`.

Otherwise, you can build the [Dockerfile](./Dockerfile) in the project's root directory yourself by running `make`. In the container, the testbed will be added to your
`PYTHONPATH`. But you need to make sure, that you run the container with privileges to access the host network in order to have access to the host's network interfaces. You of course need to modify the volume mount to allow the testbed access to your scenarios.

```sh
docker run -it --rm --cap-add=ALL -v /var/run/docker.sock:/var/run/docker.sock --net host --pid host --userns host --privileged mgjm/sn3t:latest
```

The main image is based on the images in the [container-images](./container-images) directory.  
The [`ns-3`](./container-images/ns-3/Dockerfile) image is just an installation of ns-3 (currently *ns-3.30*) on top of a Debian Buster.
The [`testbed-base`](./container-images/testbed-base/Dockerfile) installs all neccessary dependencies for the testbed,
[`testbed-dev`](./container-images/testbed-dev/Dockerfile) is for development purposes (docker-cli in the container).

### Installation Without Docker

In the case you do not want to use the prebuilt docker, a normal ns-3 installation with *NetAnim* Python bindings will work, too.
The Python libraries / directory provided by ns-3 has to be in your `PYTHONPATH`, though.
The testbed so far has only been tested with **Debian 10 Buster** and **Ubuntu 18.04 Bionic Beaver**.

There is no installation via `pip`.
