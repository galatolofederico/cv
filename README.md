# Curriculum Vitae

Latex template and python script to generate my curriculum using my [me.json](https://github.com/galatolofederico/me.json)

The latest version can be found [here](http://static.galatolo.me/cv.pdf)

## Usage

Just run

```
make
```

or using Docker

```
mkdir dist
docker build . -t  cv
docker run -v $(pwd)/dist:/dist -it cv_test ./dist.sh
```

The cv will be in `./dist`

to generate the updated curriculum

## License and attribution

All the code is released under the [CC BY-NC-SA 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/) license 

My contribution are the `generate.py` and some minor template improvements

Template Author: Adrien Friggeri [[repo](https://github.com/afriggeri/CV)]

A4 version: Marvin Frommhold [[repo](https://github.com/depressiveRobot/friggeri-cv-a4)]
