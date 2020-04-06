# Codel 🍲

Count lines of your code tastefully.

## Getting started

Before you start you should install:

- Python 3.x
- pip

## Installation

Enter this in your terminal:

```bash
pip install codel
```

## Usage

To count lines of files with extensions `.py` `.cpp` and `.h` enter this in your terminal:

```bash
codel count -e .py .cpp .h
```

To ignore files or folders use `-i` flag:

```bash
codel count -e .py -i test/**
```

### Configuration

It's possible to set default's for folder so you can use codel without flags. To manage your folder configuration use `config` command:

```bash
codel config -e .py -i test/**
```

If you want to apply the configuration globally you should use `-g` flag:

```bash
codel config -g -e .py -i test/**
```

## License

[MIT](LICENSE.md)

## Contribution

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details about contributing.

## Remark

This is coddle. I didn't know that before I started to develop this project. Bon appetit😘

![Coddle](https://cdn.greatlifepublishing.net/wp-content/uploads/sites/2/2018/06/22051835/Irish-Coddle-1-728x486.jpg)
