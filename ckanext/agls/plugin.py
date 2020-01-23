# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import datetime
import json
import logging
import os

import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as tk
from shapely.geometry import asShape

import ckanext.agls.views as views

log = logging.getLogger(__name__)



def custom_output_validator(key, data, errors, context):
    value = data.get(key)
    value = (
        value.replace("{", "")
        .replace("}", "")
        .replace(',"', ", ")
        .replace('"', "")
        .replace(",", ", ")
    )
    data[key] = value


def get_group_select_list():
    result = []
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    groups = tk.get_action("group_list")(context, {})

    for group in groups:
        result.append({"value": group})
    return result


def group_id():
    id = tk.request.params.get("group") or tk.request.params.get("groups__0__id")
    return id


# vocab setup
# "Geospatial Topic" and "Field(s) of Research" are tag vocabularies.
def create_geospatial_topics():
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    vocab = model.Vocabulary.get("geospatial_topics")
    if not vocab:
        data = {"name": "geospatial_topics"}
        vocab = tk.get_action("vocabulary_create")(context, data)
        for tag in (
            "Farming",
            "Biota",
            "Boundaries",
            "Climatology Meteorology and Atmosphere",
            "Economy",
            "Elevation",
            "Environment",
            "Geoscientific information",
            "Health",
            "Imagery base maps and Earth cover",
            "Intelligence and Military",
            "Inland waters",
            "Location",
            "Oceans",
            "Planning and Cadastre",
            "Society",
            "Transportation",
            "Utilities and Communication",
        ):
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            tk.get_action("tag_create")(context, data)


def geospatial_topics():
    create_geospatial_topics()
    try:
        tag_list = tk.get_action("tag_list")
        geospatial_topics = tag_list(data_dict={"vocabulary_id": "geospatial_topics"})
        return geospatial_topics
    except tk.ObjectNotFound:
        return None


def groups():
    query = model.Group.all(group_type="group")

    def convert_to_dict(user):
        out = {}
        for k in ["id", "name", "title"]:
            out[k] = getattr(user, k)
        return out

    out = map(convert_to_dict, query.all())
    return out


def create_fields_of_research():

    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    vocab = model.Vocabulary.get("fields_of_research")
    if not vocab:
        print("Loading ABS Fields of Research for the first time, please wait...")
        data = {"name": "fields_of_research"}
        vocab = tk.get_action("vocabulary_create")(context, data)
        with open(
            os.path.dirname(os.path.abspath(__file__)) + "/ABS Fields Of Research.csv",
            "rb",
        ) as csvfile:
            forcsv = csv.reader(csvfile)
            for row in forcsv:
                data = {
                    "name": row[1].strip().replace(",", "")[:100],
                    "vocabulary_id": vocab["id"],
                }
                tk.get_action("tag_create")(context, data)
        print("ABS Fields of Research loaded")


def fields_of_research():
    create_fields_of_research()
    try:
        tag_list = tk.get_action("tag_list")
        fields_of_research = tag_list(
            data_dict={"vocabulary_id": "fields_of_research", "all_fields": False}
        )
        return fields_of_research
    except tk.ObjectNotFound:
        return None


def delete_fields_theme():
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    vocab = model.Vocabulary.get("fields_theme")
    if vocab:
        log.info("Found Fields Theme, please wait...")
        data = {"id": vocab.id}
        vocab = tk.get_action("vocabulary_delete")(context, data)
        log.info("Success delete vocab")


def delete_tags_fields_theme():
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    vocab = model.Vocabulary.get("fields_theme")
    tag_list = tk.get_action("tag_list")
    fields_theme = tag_list(data_dict={"vocabulary_id": "fields_theme"})
    log.info("fields_theme_tags = %s, type = %s", fields_theme, type(fields_theme))
    for tag in fields_theme:
        data = {"id": tag, "vocabulary_id": vocab.id}
        tk.get_action("tag_delete")(context, data)
        log.info("tag_delete = %s", data)
        log.info("tag = %s, type = %s, vocab = %s", tag, type(tag), vocab.id)


def create_fields_theme():
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    vocab = model.Vocabulary.get("fields_theme")
    if not vocab:
        log.info("Loading Fields Theme for the first time, please wait...")
        data = {"name": "fields_theme"}
        vocab = tk.get_action("vocabulary_create")(context, data)
        log.info("Success create vocab")
        for tag in (
            "Law and Order",
            "Education and Training",
            "Health",
            "Social and Community Services",
            "Recreation and Culture",
            "Primary Industries",
            "Business and Industrial Development",
            "Government Administration",
            "Finance",
            "Land and Resource Management",
            "Infrastructure and Communications",
            "Conservation and Environment",
            "Labour",
            "Emergency Management",
        ):
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            tk.get_action("tag_create")(context, data)
            log.info("tag_create = %s", data)


def fields_theme():
    create_fields_theme()
    # delete_tags_fields_theme()
    # delete_fields_theme()
    try:
        tag_list = tk.get_action("tag_list")
        fields_theme = tag_list(
            data_dict={"vocabulary_id": "fields_theme", "all_fields": False}
        )
        return fields_theme
    except tk.ObjectNotFound:
        return None


def spatial_bound(spatial_str):
    if spatial_str and spatial_str != "":
        spatial_dict = json.loads(spatial_str)
        return asShape(spatial_dict).bounds
    return None


def get_user_full(username):
    try:
        return tk.get_action("user_show")(
            {"return_minimal": True, "keep_sensitive_data": True, "keep_email": True},
            {"id": username},
        )
    except tk.ObjectNotFound:
        return None


def get_org_full(id):
    try:
        return tk.get_action("organization_show")(
            {"include_datasets": False}, {"id": id}
        )
    except tk.ObjectNotFound:
        return None


def is_site(site_name):
    result = site_name in tk.config.get("ckan.site_url", "")
    return result


def get_now():
    return datetime.datetime.now().strftime("%Y-%M-%d")


def iso_languages_list():
    return tk.config.get("iso638.2")


class AGLSDatasetPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IConfigurer, inherit=False)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IBlueprint)
    p.implements(p.IValidators)

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "fields_of_research": fields_of_research,
            "geospatial_topics": geospatial_topics,
            "fields_theme": fields_theme,
            "get_group_select_list": get_group_select_list,
            "spatial_bound": spatial_bound,
            "get_user_full": get_user_full,
            "get_org_full": get_org_full,
            "groups": groups,
            "group_id": group_id,
            "is_site": is_site,
            "get_now": get_now,
            "iso_languages_list": iso_languages_list,
        }

    def get_validators(self):
        return {"custom_output_validator": custom_output_validator}

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_public_directory(config, "theme/public")
        tk.add_public_directory(config, "fanstatic/ckanext-agls")
        tk.add_resource("fanstatic", "ckanext-agls")

        here = os.path.dirname(__file__)

        with open(os.path.join(here, "languages.json")) as languages:
            config["iso638.2"] = json.load(languages)
        # config['licenses_group_url'] = 'http://%(ckan.site_url)/licenses.json'
