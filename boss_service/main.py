# coding:utf-8
from config import runmodel, craeteapi, logger, app
from version.v3.bossConfig import app as boss_v3, version
import Res

app.register_blueprint(boss_v3, url_prefix=Res.Dms_Url_Prefix)


if __name__ == '__main__':
    # from gevent.pywsgi import WSGIServer
    # WSGIServer(('0.0.0.0', 5002), app).serve_forever()
    logger.info(Res.start)
    logger.info(version)
    # app.run(host=Res.host, debug=True, port=Res.port)
    app.run(host=Res.host,  port=Res.port)
