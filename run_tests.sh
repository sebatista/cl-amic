#!/usr/bin/env bash
# backup /var/odoo/backups/
oe --restore -d amic_test -c amic -f test.dump.zip

# no se linkea con wdb
# se usan los fuentes bajados de la imagen
# se usa la imagen debug

sudo docker run --rm -it \
    -v /odoo_ar/odoo-11.0/amic/config:/opt/odoo/etc/ \
    -v /odoo_ar/odoo-11.0/amic/data_dir:/opt/odoo/data \
    -v /odoo_ar/odoo-11.0/amic/sources:/opt/odoo/custom-addons \
    -v /odoo_ar/odoo-11.0/extra-addons:/opt/odoo/extra-addons \
    -v /odoo_ar/odoo-11.0/dist-packages:/usr/lib/python3/dist-packages \
    -v /odoo_ar/odoo-11.0/dist-local-packages:/usr/local/lib/python3.7/dist-local-packages \
    -e WDB_SOCKET_SERVER=wdb \
    --link pg-amic:db \
    jobiols/odoo-jeo:11.0.debug -- \
        -i  mrp_easy_prod,mrp_lot_attributes,mrp_ot,mrp_production_cancel,pre_printed_stock_picking \
   --stop-after-init -d amic_test --test-enable
