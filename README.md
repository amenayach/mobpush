# mobpush
A Flask app that syncs mobile with pc, where you can send text and files

## Install requirements on your machine
```sh
$ pip3 install -r requirements.txt
```

## Run on your machine
```sh
$ py -m flask run --host=0.0.0.0 --port=9797
```

## Or simply on Windows
```sh
$ mobpush.bat
```

## Run on docker
Build the docker image:
```sh
$ buildimage.bat
```

To run on docker
```sh
$ docker run -p 9797:5000 --name mobpush mobpush
```
To run on docker from Windows
```sh
$ runcontainer.bat
```

## Open the web UI

Head to http://localhost:9797 on pc

On mobile open in your web browser using your pc IP:

http://[pc-ip]:9797
