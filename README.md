# EEE231 Directed Graph Editor

## 0. Table of Contents

- [EEE231 Directed Graph Editor](#eee231-directed-graph-editor)
  - [0. Table of Contents](#0-table-of-contents)
  - [1. Background](#1-background)
    - [1.0 Install](#10-install)
    - [1.1 Usage](#11-usage)
    - [1.2 Name Convention](#12-name-convention)
    - [1.3 Development Process](#13-development-process)
  - [2. Architecture](#2-architecture)
    - [2.0 Module](#20-module)
    - [2.1 Class](#21-class)
  - [3. License](#3-license)
  - [4. External Link](#4-external-link)
  - [5. ChangeLog](#5-changelog)

## 1. Background

### 1.0 Install

- Clone GitHub Repository `git clone git@github.com:Spehhhhh/EEE228.git`
- Switch to the directory `cd EEE231`

### 1.1 Usage

- This project uses pipenv to manage the virtual environment.
- Install Poetry `curl -sSL https://install.python-poetry.org | python3 -`
- Set environment variables `echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.zshrc`
- Install package `poetry install`
- Activate the virtual environment for the current project `poetry shell`
- Generate lockfile `poetry lock --no-update`
- Run the main program `poetry run python main.py`

### 1.2 Name Convention

- Class Naming Convention: `CapWords`
- Function Naming Convention: `lower_with_under()`
- Variables Naming Convention: `lower_with_under`

### 1.3 Development Process

Each group develops code in its own branch. After completing the development of the features and writing the unit tests. Pull Request to Main branch.

How do I create a branch?

``` BASH
$ git pull
$ git checkout -b dggui
$ git push --set-upstream origin dggui
```

How to properly Clone a branch Branch in an upstream repository?

``` BASH
$ git clone https://github.com/pirlite2/EEE231-group-B.git
$ cd EEE231-group-B
$ git checkout -b dggui origin/dggui # git checkout -b {your_local_branch_name} origin/<remote_branch_name>
```

How do I get my own feature branch to synchronize the code in the main branch?

``` BASH
$ git pull
$ git checkout feature1 # The branch you want to synchronize your code with
$ git merge main
```

We use `Black` for code formatting.

## 2. Architecture

### 2.0 Module

| Module | Folder Location | Feature | Detailed documentation |
|---|---|---|---|
| `directedgraph` | `/directedgraph` |  | [🔗](docs/) |
| `dgutils` | `/directedgraph/dgutils` | Software External Interfaces | [🔗](docs/dgutils.md) |
| `dggui` | `/directedgraph/dggui` | Software UI | [🔗](docs/dggui.md) |
| `dgapp` | `/directedgraph/dgapp` | Software Event | [🔗](docs/dgapp.md) |
| `dgcore` | `/directedgraph/dgcore` | Graph Resource Model | [🔗](docs/dgcore.md) |

### 2.1 Class

![Class Diagram Overview](/docs/class_diagram_overview.png)

![Class Diagram](/docs/class_diagram.png)

| Class | Feature |
|---|---|
| `directedgraph.dgcore.Graph` | Used to control Graph |
| `directedgraph.dgcore.GraphComponent` | Used to control specific Arc and Node |
| `directedgraph.dgcore.Node` |  |
| `directedgraph.dgcore.SourceNode` |  |
| `directedgraph.dgcore.GroundNode` |  |
| `directedgraph.dgcore.Arc` |  |
| `directedgraph.dggui.GraphEditorMainWindow` |  |
| `directedgraph.dggui.InputDialogNode` | Input Dialog GUI |
| `directedgraph.dggui.InputDialogArc` | Input Dialog GUI |
| `directedgraph.dggui.NodeItem` | Node GUI |
| `directedgraph.dggui.SourceNodeItem` | SourceNode GUI |
| `directedgraph.dggui.GroundNodeItem` | GroundNode GUI |
| `directedgraph.dggui.ArcItem` | Arc GUI |
| `directedgraph.dgutils.FileManager` | Reading and saving XML |
| `directedgraph.dgutils.GraphSimulator` | Exporting Graph as a simulation file |

A GraphEditorGUI instance corresponds to a software window.

A Graph Class instance corresponds to a Directed Graph.

GraphComponent Class is the software component library. All Nodes Class and Arcs Class inherit from GraphComponent.

Most of the Methods in GraphController are Use Cases, where a Method corresponds to some user action on the GUI. For example, when the user clicks the Create button, the GUI calls the Method in the GraphController instead of the GUI manipulating the database directly.

In the case of the FileManager Class, when the user calls read_graph, the function takes a local xml file as an argument, reads the data and returns a Graph instance. Typically, a local xml file will correspond to a Graph instance.

The advantage of this design is that, firstly, the software can launch multiple Graphs and multiple GUI interfaces at the same time. Secondly, the fine-grained class classification makes teamwork less difficult and the GUI team only needs to focus on interface design.

## 3. License

[GNU General Public License v3.0](LICENSE)

## 4. External Link

- Naming Conventions
  - [Python Naming Conventions](https://www.python.org/dev/peps/pep-0008/)
  - [naming - How should I name functions that return values in Python? - Software Engineering Stack Exchange](https://softwareengineering.stackexchange.com/questions/334135/how-should-i-name-functions-that-return-values-in-python)
  - [coding style - Python file naming convention? - Software Engineering Stack Exchange](https://softwareengineering.stackexchange.com/questions/308972/python-file-naming-convention)
  - [Function naming conventions - Stack Overflow](https://stackoverflow.com/questions/1991324/function-naming-conventions)
  - [Swift.org - API Design Guidelines](https://swift.org/documentation/api-design-guidelines/#strive-for-fluent-usage)
  - [naming-convention-guides/python at master · naming-convention/naming-convention-guides](https://github.com/naming-convention/naming-convention-guides/tree/master/python)
  - [styleguide | Style guides for Google-originated open-source projects](https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations)
- Commit Message Conventions
  - [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- PySide6
  - [PySide6 Doc](https://wiki.qt.io/Qt_for_Python)

## 5. ChangeLog

- 210507 add Development Process
- 210501 add Branch
- 210501 fix Contributors
- 210414 add Architecture
- 210412 add Naming Conventions
- 210324 init
