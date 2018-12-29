FROM zzh/flask

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 1
# ENV STATIC_INDEX 0
# RUN pip install kafka-python
RUN pip install -i https://pypi.douban.com/simple configparser scrapy scrapyd python-scrapyd-api apscheduler redis pdfkit openpyxl
# Add backend app
COPY ./boss_service /app

WORKDIR /app