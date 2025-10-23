# IRSL 

## build

```shell
docker compose -f docker-compose.yml build
```

## run
```shell
docker compose -f docker-compose.yml up
```

## decode filename

```shell
python3  decode_filename.py -i wiki_org -o wiki
```

## convert

```shell
python3 conv_pukiwiki_to_md.py -i wiki -o wiki_mdf -m
```

## post to esa

```shell
python3 upfiles.py -i wiki_mdf -t <token> -n <team_name> -p <prefix>
```

# pukiwiki2markdown (original document)

## Demo

* https://sandbox.saino.me/pukiwiki2markdown/

## Development

```shell
$ php composer.phar install
$ php composer.phar start
```

## API

```shell
curl -XPOST <pukiwiki2markdown URL>/api/v1/convert -H 'Content-Type: application/json' -d '{"body": "*Header1\n**Header2\n"}'
```
