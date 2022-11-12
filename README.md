# Intro_to_AI_assignment1
## Install library
```
pip install -r requirement.txt
```
## Run Watersort
First, you need to create an input file. You can find example files in `io_watersort/input`.

Then, run the `watersort.py` file with the following syntax:
```
python watersort.py <input file name> [algorithm]
```
`[algorithm]` can be:
* dfs
* Astar

For example:
```
python watersort_dfs.py input1.txt dfs
```
The output will be created in `io_watersort/output` with the corresponding file name
## Run bloxorz
Run the `bloxorz.py` file:
```
python bloxorz.py <Number of file> <solver>
```
`<solver>` can be:
* DFS
* GA


`<Number of file>` can be:
* 1
* 2
* ...

Example
```
python bloxorz.py 1 GA
```
The output will be created in `io_bloxorz/output` with the corresponding file name
