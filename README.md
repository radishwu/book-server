# book-server
book server

### Usage

```bash
#MacOS dev
export FLASK_APP=book
export FLASK_ENV=development
flask run
```

#### 安装依赖服务
- 安装splash服务
```bash
docker pull scrapinghub/splash #拉取镜像
docker run -p 8050:8050 scrapinghub/splash #启动实例
```