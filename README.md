# Python 自动化测试入门练习

这是一个可以直接运行的 Python 测试练习项目，使用一个小型计算模块和一个用户 API 客户端，演示日常最常见的自动化测试方法。

## 你会学到什么

- **单元测试**：独立验证函数的正常结果、边界值和异常。
- **参数化测试**：用一组输入重复验证同一规则。
- **Fixture**：用 pytest fixture 准备可复用的测试数据。
- **Mock**：隔离外部依赖，验证函数是否按预期调用其他组件。
- **HTTP 客户端测试**：用 `requests-mock` 模拟 HTTP 响应，不访问真实网络。
- **覆盖率**：查看哪些代码路径尚未被测试覆盖。
- **持续集成**：通过 GitHub Actions 在推送代码时自动运行测试。

## 项目结构

```text
python-testing-learning-kit/
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   └── learning_app/
│       ├── __init__.py
│       ├── calculator.py
│       ├── user_api.py
│       └── user_service.py
├── tests/
│   ├── conftest.py
│   ├── test_calculator.py
│   ├── test_user_api.py
│   └── test_user_service.py
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## 1. 准备环境（Windows PowerShell）

需要 Python 3.10 或更高版本。打开 PowerShell，在项目目录执行：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

直接使用虚拟环境里的 Python 可以避免 PowerShell 执行策略阻止激活脚本。

## 2. 运行测试

运行全部测试：

```powershell
.\.venv\Scripts\python.exe -m pytest
```

查看更详细的测试名称：

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

只运行一个测试文件或一个测试函数：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_divide_by_zero_raises
```

生成终端覆盖率报告：

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=learning_app --cov-report=term-missing
```

生成可在浏览器打开的 HTML 报告：

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=learning_app --cov-report=html
Start-Process htmlcov\index.html
```

覆盖率百分比不是质量保证。更重要的是测试是否验证了真正重要的行为和边界情况。

## 3. 推荐学习顺序

### 第一步：读 `tests/test_calculator.py`

先运行测试，再看 `src/learning_app/calculator.py`。试着把某个实现改错，重新运行测试，观察失败信息如何指出问题；然后还原正确行为。

一个 pytest 测试函数通常遵循 **Arrange / Act / Assert**：

1. **Arrange**：准备输入和前置条件。
2. **Act**：调用被测代码。
3. **Assert**：检查结果或异常。

```python
def test_add_returns_sum():
    result = add(2, 3)  # Act
    assert result == 5  # Assert
```

测试名称描述“应该发生什么”，不要只写 `test_1`。pytest 会自动发现名称以 `test_` 开头的文件和函数。

### 第二步：学习参数化和异常断言

`@pytest.mark.parametrize` 可以把多组输入传给同一个测试函数，避免复制粘贴测试逻辑。`pytest.raises` 用于确认指定异常确实发生。

练习：给 `multiply` 添加负数和零的测试；给 `divide` 添加更多小数输入。

### 第三步：学习 Fixture

`tests/conftest.py` 中的 `sample_user` 是一个 fixture。测试函数只要把 fixture 名称声明为参数，pytest 就会在测试前提供测试数据。

Fixture 适合放共享的测试准备逻辑；不要为了复用而把简单、局部的数据过度抽象。

### 第四步：学习外部依赖隔离

`tests/test_user_api.py` 使用 `requests-mock` 拦截 HTTP 请求，测试不会访问真实网络。这样测试更快、更稳定，也不会依赖某个线上服务是否可用。

`tests/test_user_service.py` 使用 `pytest-mock` 提供的 `mocker` 替换服务依赖，并验证调用参数。Mock 应只用于隔离边界或验证关键交互；业务逻辑本身尽量使用真实实现测试。

### 第五步：查看失败信息与覆盖率

故意修改一个断言，让测试失败，观察 pytest 显示的期望值和实际值。再运行覆盖率命令，检查未覆盖行，并判断是否需要补充有意义的用例。

## 4. 常见测试用例清单

写测试时可以按这个清单思考：

| 场景 | 本项目示例 |
|---|---|
| 正常输入与正常结果 | 加法、除法、成功获取用户 |
| 边界值 | 零、负数、最小合法用户 ID |
| 无效输入 | 非正整数用户 ID |
| 异常路径 | 除以零、HTTP 错误、网络超时、无效 JSON |
| 多组等价输入 | 参数化验证加法和除法 |
| 外部服务交互 | 校验请求 URL、HTTP 方法和超时参数 |
| 依赖调用 | Mock 用户 API，验证 service 的调用方式 |

实际项目还应根据业务增加权限、重复提交、数据状态变化、并发、数据库事务等测试。

## 5. 工具、插件与软件

### 本项目使用

| 工具/包 | 用途 |
|---|---|
| Python | 编程语言与运行环境 |
| `pytest` | 测试发现、断言、Fixture、参数化 |
| `pytest-cov` | 生成测试覆盖率报告 |
| `pytest-mock` | 用 pytest 风格创建 Mock |
| `requests` | Python HTTP 客户端 |
| `requests-mock` | 模拟 `requests` 发出的 HTTP 请求 |
| VS Code Python 扩展 | 选择解释器、发现和运行 pytest |
| Pylance | Python 代码补全和静态分析 |

VS Code 中安装 **Python** 和 **Pylance** 扩展。打开项目后，按 `Ctrl+Shift+P`，选择 `Python: Select Interpreter`，选中项目的 `.venv`。随后可在测试面板运行测试，或继续使用上面的命令行。

### 后续可选工具

- **Playwright**：浏览器端到端测试，适合验证网页在浏览器中的用户流程。
- **Selenium**：另一种成熟的浏览器自动化方案。
- **Postman / Bruno**：手动调试和组织 API 请求；它们不替代 Python 单元测试。
- **Allure**：生成更易阅读的测试报告，可在掌握 pytest 基础后再学习。

这些工具面向不同层次，不需要一开始全部安装。建议先掌握本项目的 pytest，再根据实际项目类型选择 API、浏览器或报告工具。

## 6. 练习任务

1. 给 `calculator.py` 增加 `subtract` 函数，并先写测试再实现。
2. 给 API 客户端添加“用户响应缺少 name 字段”的测试。
3. 在 `user_service.py` 增加一个明确的业务规则，并通过 Mock 测试它调用 API 的方式。
4. 删除一个测试断言，观察测试是否还能发现实现错误；思考测试是否真的检查了目标行为。
5. 把代码推送到 GitHub，查看 Actions 页面中的自动测试结果。

## 7. 常见问题

- **找不到 `pytest`**：确保使用 `.\.venv\Scripts\python.exe -m pytest`，并确认依赖已安装到同一个虚拟环境。
- **没有发现测试**：检查文件名是否以 `test_` 开头、测试函数是否以 `test_` 开头。
- **导入 `learning_app` 失败**：从项目根目录执行命令；`pyproject.toml` 已将 `src` 加入 pytest 的导入路径。
- **覆盖率命令不识别**：确认已安装 `pytest-cov`，或重新运行依赖安装命令。

## 8. 修改后重新安装

如果后续把项目作为可安装包继续扩展，可以再添加打包配置并使用可编辑安装。本入门项目不需要这一步，保持依赖和运行方式简单。
