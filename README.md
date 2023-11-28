# Inventário de especies nativas y análisis de calidad del agua, através de la detección y manipulación de imágenes digitales aéreas en el Parque Natural Municipal Salto Kuppers de la ciudad de Eldorado 

Repositório creado para gestionar y almacenar los codigos relacionados al proyecto desarrollado en el PNM Salto Kuppers.

* [Prerparando ambiente de desarrollo](#Prerparando-ambiente-de-desarrollo)
* [Importando datos](#Importando-datos)

## Prerparando ambiente de desarrollo:
Para este proyecto, usaremos:

* Python
  * [poetry](https://python-poetry.org/): para gestión de dependencias
  * [sqlAlchemy](https://python-poetry.org/): ORM para la base de datos;
  * [geoAlchemy](https://python-poetry.org/): ORM para la base de datos espaciales;
* [PostGIS](https://postgis.net/): Base de datos PostgreSQL con extención GIS habilitada;
Una posibilidad es usar _PostGIS_ en una instancia [Docker](https://www.docker.com/), si no posee una instalado en su máquina.
A seguir son presentados los principales pasos para usar _Docker_

### Git-Github
`git clone git@github.com:TUSIGyT/PNM_Salto_Kuppers.git`

### Python
Haremos uso de [poetry](https://python-poetry.org/docs/#installation) para facilitar la gestión de las dependencias del proyecto.
Una vez instalado, basta acceder a la carpeta donde hiciste el colne del presente repositório y instalar las dependencias:

`poetry install`

### Docker
Para saber al respecto de docker, visite <https://www.docker.com/>.

Para saber como instalar docker, visite <https://docs.docker.com/desktop/>

#### Creando imagen PostGIS en Docker
Descargand la imagen _PostGIS_

`docker pull postgis/postgis`

#### Instalando e configurando el container:
`docker run --name postgis -e POSTGRES_PASSWORD=postgres -d postgis/postgis`

No dejes de crear un archivo `.env` con la variable de ambiente `DB_URL`, talcual como presentado en [env-sample](env-sample).

##### Iniciando el container al prender la computadora
`docker start postgis`

:warning: Si por algún motivo haz cambiado el parámetro `--name` en el paso anterior, considere que tendrás que usar en el presente comando el nombre usado.

### Creando la base de datos `pnm_salto_kuppers`
```commandline
# usando PSQL del docker 
docker exec -ti postgis psql -U postgres
CREATE DATABASE pnm_salto_kuppers
\connect pnm_salto_kuppers
CREATE EXTENSION postgis;
```

### Creando las tablas
El modelo de las tablas están en [models.py](models.py).

:warning: Antes de ejecutar el comando a seguir, confirmar que haz creado en archivo [`.env`](env-sample) con la variables de ambiente `DB_URL`.

```python
python3 create_tables.py
```

## Importando datos
Por ahora hay solamente un campo realizado, en el cual se relevaron especies de flora.
Los datos relevados están en [data/form-1__muestreo.csv](data/form-1__muestreo.csv).
La herramienta [import_tools](import_tools.py) lee dicho csv, lo convierte a dato espacial y lo importa a la base de datos.
Más adelante lo tendremos que modificar de forma que se pueda definir qué archivos deberán ser incorporados a la base de datos.
