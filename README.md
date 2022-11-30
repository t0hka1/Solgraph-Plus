# Solgraph-Plus

```shell
$ pip install solgraphPlus
```

```python
import solgraphPlus.main as main
import sys

builded=main.build(sys.argv[1])
dotGraph=main.generateDot(builded)
```