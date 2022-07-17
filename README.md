<<<<<<< HEAD
# GlobalMap
GlobalMap by DataShader, to support customized layer to demonstrate different datasets.
=======
## How to build the visualization

```bash
conda env create -f environment.yml
```

The preprocess the _observations.csv_ file to remove unneeded columns, and to convert the lat/long fields to metres.

```bash
python preprocess.py
```

Generate the tiles as follows:

```bash
python generate_tiles.py
```

Then run a webserver to serve them:

```
python -m http.server 8009
```

And open http://localhost:8009/