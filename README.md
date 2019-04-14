# hasek

Important note:
> All of the code here has been taken from [Giraffez](https://github.com/capitalone/giraffez)
  So 100% of the credit should go to the team there!

Hasek allows for easy password and secret management from either the command
line or via Python code.


## Quick Installation

A virtual environment is highly recommended!

```bash
pip install git+https://github.com/fdosani/hasek.git
```
> Will be switching PyPi soon


## Example

First you can initialize the configuration with the following:
```bash
hasek config --init
```

Set a new connection for which you can store your credentials for:
```bash
hasek config --set connections.mydb1.host db1.local
hasek config --set connections.mydb1.username abc123
hasek config --set connections.mydb1.password password123
```

You can then read the secrets as follows:
```bash
hasek secret connections.db1.password
```
