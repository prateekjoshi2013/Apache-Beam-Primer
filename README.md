# Python setup

## Virtual Environment

### create venv

```sh
python3 -m venv /venv
```
### activate myenv env

```sh
source /venv/bin/activate
```

### deactivate env

```sh
deactivate
```

## Start Pipeline

### add gcp generated credentials.json file in python folder

### add .environment variables in .environment file

### start producer

```sh
make producer
```

### start processor

```sh
make processor
```

### start consumer

```sh
make consumer
```
