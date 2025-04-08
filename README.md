# Contract

https://etherscan.io/token/0xcf7e6742266ad5a76ee042e26d3f766c34195e5f#code

# Clone the openzeppelin repo

```bash
cd project
cd src
cd utils
git clone https://github.com/OpenZeppelin/openzeppelin-contracts
```
# how to run you first spec

- install docker

[guide on installing docker](https://docs.docker.com/engine/install/)

- docker requires the user in the docker group if running as non root

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```
- logout and login again or reboot the system
- provide you certora key in bootstrap.sh
- run the bootstrap script
```bash
chmod +x ./bootstrap.sh
./bootstrap.sh
```
- run the following command inside the container
```bash
certoraRun src/ERC20Token.sol --verify ERC20Token:specs/ERC20Token.spec
```

- Or run the following command inside the container for Pool.sol
```bash
certoraRun src/Pool.sol \
  --verify Pool:specs/Pool.spec \
  --optimistic_loop
```
- you can also run the following commands to install another version of the solidity compiler(solc), the default is v0.8.0

```bash
solc-select install 0.8.1
solc-select use 0.8.1 
```
