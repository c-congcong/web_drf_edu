"""
Django settings for edu_api project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1cxl(0a#9*4j-70w)i_4ds&a-mw&@#pnb)9g@l2^)!4y=^vy53'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'api.baizhishop.com',
    'www.baizhishop.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    # 'django_filter',

    # x admin配置
    'xadmin',
    'crispy_forms',
    'reversion',
    # 富文本编辑器配置
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器的上传模块

    'home',
    'user',
    'course',
    'cart',
    'order',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edu_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'edu_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "edu_api1",
        # 'HOST': "localhost",
        'HOST': "127.0.0.1",
        'USER': "root",
        'PASSWORD': '123456',
        'PORT': 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 项目的日志配置
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 格式化日志信息
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 日志的过滤信息
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理日志的方法
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            # 记录到文件中的日志等级
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置  日志的文件名  日志的保存目录
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/lesson_api.log"),
            # 日志文件的大小  100M
            'maxBytes': 100 * 1024 * 1024,
            # 日志文件的最大数量
            'backupCount': 10,
            # 日志的格式
            'formatter': 'verbose'
        },
    },
    # 日志对象，与django集成使用
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# DRF 默认配置
REST_FRAMEWORK = {
    # 全局异常配置
    "EXCEPTION_HANDLER": "edu_api.utils.exceptions.exception_handler",
    # 添加认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# 允许跨域请求
CORS_ORIGIN_ALLOW_ALL = True

# jwt配置
JWT_AUTH = {
    # 有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    # 自定义jwt返回值的格式方法
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'user.utils.jwt_response_payload_handler',
}

# 注册自定义用户模型 格式必须是app.表明
AUTH_USER_MODEL = 'user.UserInfo'

# 自定义多条件登录
AUTHENTICATION_BACKENDS = [
    'user.utils.UserAuthBackend',
]

# django 连接redis设置

CACHES = {
    # 默认库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务端端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/1",
        # 使用客户端方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务端端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/15",
        # 使用客户端方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 购物车
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务端端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/10",
        # 使用客户端方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# develope 配置
KEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 展示哪些工具栏
        'height': 300,  # 编辑器的高度
        # 'width': 300,
    },
}
CKEDITOR_UPLOAD_PATH = ''

# 支付宝配置信息
ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # 真实支付宝网关地址
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?",  # 沙箱支付宝网关地址
    "appid": "2016102600767444",
    "app_notify_url": None,
    "app_private_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "alipay_public_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "sign_type": "RSA2",
    "debug": False,
    # "return_url": "http://www.baizhistore.cn:8080/payments/result",  # 同步回调地址
    "return_url": "http://localhost:8080/pay",  # 同步回调地址
    "notify_url": "http://api.baizhishop.com:9001/payments/pay/",  # 异步结果通知
}
