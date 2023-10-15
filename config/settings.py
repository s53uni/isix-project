"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY ='django-insecure-e7u8rv^4nna)cfbte&#+x)5&9wogf!6v3kw)30dv7i6%i$r$)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 수정...
ALLOWED_HOSTS = ['*']

# Application definition

# new app이 생성되면 이곳에 등록하기
INSTALLED_APPS = [
    # new app
    'mainapp',
    # origin app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

### 내 서버 내에서 iframe 적용하기
X_FRAME_OPTIONS = "SAMEORIGIN"

### 내 서버 내에서 iframe 적용 안하기
# X_FRAME_OPTION = "DENY"

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        ### 수정...
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 사용할 데이터베이스 엔진
        'NAME': 'isix', # 데이터베이스 이름 
        'USER': 'root', # 접속할 Database 계정 아이디 ex) root
        'PASSWORD': '0000',  # 접속할 Database 계정 비밀번호 ex) 1234
        'HOST': 'localhost',   # host는 로컬 환경에서 동작한다면 ex) localhost
        'PORT': '3306', # 설치시 설정한 port 번호를 입력한다. ex) 3306
    },
}

### Logging 처리
# - DB 실행 내용을 console 창에서 확인할 수 있도록 처리
LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        }
    },
    'loggers':{
        'django.db.backends':{
            'handlers':['console'],
            'level':'DEBUG',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

### 수정...
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ko-kr'

### 수정...
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

### 정적파일을 관리하는 경로
# - 정적파일 : css, javascript, 이미지, 동영상 등(html은 제외)
STATIC_URL = 'static/'

### 추가...
### 각 앱(app)에서 관리할 수 있도록 정적파일 관리 폴더 정의하기
STATICFILES_DIRS = [BASE_DIR/'static']

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


### 로그인 상태에서 브라우저가 닫혔을 때 세션정보(로그인 정보) 삭제하기(로그아웃 처리)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 세션 엔진 설정 (기본값: 'django.contrib.sessions.backends.db' - 데이터베이스 백엔드)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 세션 쿠키의 유효 기간 (초) - 기본값: 1209600 (2주)
SESSION_COOKIE_AGE = 3600  # 1시간