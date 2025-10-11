FROM php:7

RUN apt -q -qq -y update && \
    apt -q -qq -y upgrade > /dev/null && \
    apt install -q -qq -y curl git unzip > /dev/null && \
    apt clean && \
    rm -rf /var/lib/apt/lists/

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN mkdir /app
COPY . /app

WORKDIR /app
RUN composer install

CMD ["php", "-S", "0.0.0.0:8080", "-t", "public", "-c", "php.ini"]
