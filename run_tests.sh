#!/usr/bin/env bash
oe --restore -d amic_test -c amic -f 2020_05_16_19_41_20.dump.zip

sudo docker run --rm -it \
    --link wdb \
    -v /odoo_ar/odoo-11.0/amic/config:/opt/odoo/etc/ \
    -v /odoo_ar/odoo-11.0/amic/data_dir:/opt/odoo/data \
    -v /odoo_ar/odoo-11.0/amic/sources:/opt/odoo/custom-addons \
    -v /odoo_ar/odoo-11.0/extra-addons:/opt/odoo/extra-addons \
    -v /odoo_ar/odoo-11.0/dist-packages:/usr/lib/python3/dist-packages \
    -v /odoo_ar/odoo-11.0/dist-local-packages:/usr/local/lib/python3.7/dist-local-packages \
    -e WDB_SOCKET_SERVER=wdb \
    --link pg-amic:db \
    jobiols/odoo-jeo:11.0.debug -- \
        -i  amic_default \
   --stop-after-init -d amic_test --test-enable
