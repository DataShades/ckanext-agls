# -*- coding: utf-8 -*-

import requests
from flask import Blueprint, jsonify
import ckan.plugins.toolkit as tk

agls = Blueprint("agls", __name__)


def get_blueprints():
    return [agls]


def gmd(id):
    raise NotImplemented("GMD endpoint not implemented for python 3")


def geo_autocomplete():
    q = tk.request.params.get("q", "")
    rows = tk.config.get("ckan.agls.gazetter_rows") or "200"
    record_list = []
    if q:
        r = requests.get(
            "http://www.ga.gov.au/gazetteer-search/gazetteer2012/select/?q=name:*"
            + q
            + "*"
            "&rows="
            + rows
            + "&fq=feature_code:POPL or feature_code:LOCB or feature_code:SUB or feature_code:URBN or feature_code:STAT or feature_code:CONT"
        ).json()
        for record in r["response"]["docs"]:
            if record.get("authority_id") != "AHO":
                result_dict = {"name": record.get("id") + ": " + record.get("name")}
                record_list.append(result_dict)
    return jsonify(record_list)


def geo_latlon():
    q = tk.request.params.get("q", "")
    record_list = []
    if q:
        r = requests.get(
            "http://www.ga.gov.au/gazetteer-search/gazetteer2012/select/?q=id:" + q
        ).json()

        for record in r["response"]["docs"]:
            locationParts = record["location"].split(",")
            latitude = locationParts[0]
            longitude = locationParts[1]
            result_dict = {
                "id": record.get("id"),
                "name": record.get("id") + ": " + record.get("name"),
                "latitude": latitude,
                "longitude": longitude,
                "geojson": '{"type": "Point","coordinates": ['
                + longitude
                + ","
                + latitude
                + "]}",
            }
            return result_dict
    return {}


agls.add_url_rule(
    "/dataset/<id>/gmd", view_func=gmd,
)
agls.add_url_rule(
    "/api/2/util/gazetteer/autocomplete", view_func=geo_autocomplete,
)
agls.add_url_rule(
    "/api/2/util/gazetteer/latlon", view_func=geo_latlon,
)
