# Curriculum Vitae

Latex template and python script to generate my curriculum using my [me.json](https://github.com/galatolofederico/me.json)

## Usage

Just run

```
make
```

or 

```
make cv-eng-academic
```

or using Docker

```
mkdir dist
docker build . -t  cv
docker run --rm -v $(pwd)/dist:/dist -it cv ./dist.sh
```

The cv will be in `./dist`

to generate the updated curriculum

## License and attribution

All the code is released under the [CC BY-NC-SA 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/) license 

My contribution are the `generate.py` and some minor template improvements

Template Author: Adrien Friggeri [[repo](https://github.com/afriggeri/CV)]

A4 version: Marvin Frommhold [[repo](https://github.com/depressiveRobot/friggeri-cv-a4)]
