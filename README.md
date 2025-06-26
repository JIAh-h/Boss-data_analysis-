# Boss直聘数据可视化项目

## 项目简介

本项目旨在通过爬取Boss直聘网站上的招聘数据，并对这些数据进行清洗、处理和可视化展示。项目主要包括一个基于Selenium和Scrapy（虽然代码中是Selenium驱动的爬虫，但考虑到之前列出的spider目录，可以提及Scrapy作为潜在扩展或概念上的指代）的爬虫模块用于数据采集，以及一个基于Django框架的Web应用用于数据的存储、管理和可视化呈现。

## 功能特性

*   **职位数据爬取**：使用Selenium模拟浏览器行为，自动爬取Boss直聘网站上的职位信息，包括职位名称、薪资、工作地点、公司信息、学历要求、工作经验等。
*   **数据清洗与存储**：对爬取到的原始数据进行清洗和结构化处理，并将处理后的数据存储到MySQL数据库中。
*   **数据可视化**：通过Django Web应用，以图表（如柱状图、饼图、词云等）的形式展示招聘数据的统计分析结果，帮助用户直观了解行业趋势、薪资分布、热门技能等。
*   **Web界面展示**：提供一个用户友好的Web界面，方便用户查询和浏览招聘数据。

## 技术栈

*   **后端框架**：Python 3, Django
*   **爬虫框架/库**：Selenium, Scrapy (用于概念性指代，实际核心爬虫是Selenium)
*   **数据处理**：Pandas, NumPy
*   **数据可视化**：Matplotlib, Wordcloud
*   **数据库**：MySQL (通过PyMySQL连接)
*   **Web服务器**：Django内置开发服务器

## 创建步骤

### 1. 环境准备

*   **Python**: 确保您的系统安装了Python 3.x版本。
*   **pip**: Python包管理器，通常随Python一起安装。
*   **Chrome浏览器**: 爬虫需要Chrome浏览器才能运行。
*   **ChromeDriver**: 下载与您Chrome浏览器版本兼容的ChromeDriver。将其放置在项目根目录下的 `spiders/` 目录中。您可以从[ChromeDriver官方网站](https://chromedriver.chromium.org/downloads)下载。

### 2. 安装项目依赖

在项目根目录下打开终端，运行以下命令安装所有Python依赖：

```bash
pip install -r requirements.txt
```

### 3. 数据库配置

1.  确保您的系统安装并运行了MySQL数据库。
2.  在MySQL中创建一个新的数据库，例如 `boss_zhipin_data`。
3.  打开 `Boss直聘数据可视化/settings.py` 文件（请根据实际项目结构调整路径），找到 `DATABASES` 配置项，修改为您自己的MySQL数据库连接信息：

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'boss_zhipin_data', # 您的数据库名称
            'USER': 'your_mysql_username', # 您的MySQL用户名
            'PASSWORD': 'your_mysql_password', # 您的MySQL密码
            'HOST': '127.0.0.1', # 数据库主机，如果是本地则为127.0.0.1
            'PORT': '3306', # MySQL端口，默认为3306
        }
    }
    ```

4.  在项目根目录下运行以下命令，进行数据库迁移，创建数据表：

    ```bash
    python manage.py makemigrations myApp
    python manage.py migrate
    ```

### 4. 运行爬虫

在项目根目录下，进入 `spiders` 目录，然后运行爬虫脚本。
**请注意：** 运行爬虫可能需要较长时间，具体取决于爬取的数据量和网络状况。

```bash
cd spiders
python spiderMain.py
```
**重要提示**: 爬虫运行时，可能会打开Chrome浏览器窗口。请勿关闭该窗口，直到爬取完成。

### 5. 运行Django应用

在项目根目录下打开终端，运行以下命令启动Django开发服务器：

```bash
python manage.py runserver
```

### 6. 访问项目

在浏览器中访问 `http://127.0.0.1:8000/` (或其他Django服务器提示的地址)，即可访问数据可视化Web应用。

## 项目文件结构 (核心部分)

*   `manage.py`: Django项目的管理脚本。
*   `requirements.txt`: 项目所有Python依赖包列表。
*   `spiders/`: 存放爬虫相关文件，包括 `spiderMain.py` (爬虫逻辑) 和 `chromedriver.exe` (Chrome浏览器驱动)。
*   `myApp/`: Django应用程序目录，包含模型 (`models.py`)、视图 (`views.py`)、URL配置 (`urls.py`) 等。
*   `templates/`: 存放Django模板文件，用于渲染Web页面。
*   `static/`: 存放静态文件，如CSS、JavaScript和图片。
*   `Boss直聘数据可视化/`: Django项目的核心配置目录，包含 `settings.py` (项目设置) 和 `urls.py` (项目URL配置)。

## 许可证 (可选)

本项目遵循 [MIT 许可证](LICENSE)。

## 贡献 (可选)

欢迎对本项目进行贡献！如果您有任何建议或改进，请提交Issue或Pull Request。 