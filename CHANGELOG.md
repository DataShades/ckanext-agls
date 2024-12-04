# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/DataShades/ckanext-agls/compare/v0.0.1...HEAD)</small>

### Fixed

- fix: restore latlon view ([e108d41](https://github.com/DataShades/ckanext-agls/commit/e108d4192c86ebe2c0c79070cbca8da75f99cacf) by Sergey Motornyuk).
- fix: fix shapely asShape import ([68a996c](https://github.com/DataShades/ckanext-agls/commit/68a996c1aad6fe2ed7b3dbb46efde7e166108ba4) by mutantsan).

### Removed

- remove: export buttons archived into agls/snippets/package_export.html ([7a07a04](https://github.com/DataShades/ckanext-agls/commit/7a07a04b5edddce24c74092bf90790afca551786) by Sergey Motornyuk).

<!-- insertion marker -->
## [v0.0.1](https://github.com/DataShades/ckanext-agls/releases/tag/v0.0.1) - 2023-06-12

<small>[Compare with first commit](https://github.com/DataShades/ckanext-agls/compare/99e5719444a7769ac962990019d33be042985d52...v0.0.1)</small>

### Added

- Add blocks ([12d1b35](https://github.com/DataShades/ckanext-agls/commit/12d1b354dffae08d8c82ccf490af4595d767e52e) by Sergey Motornyuk).
- add cli ([db08e0f](https://github.com/DataShades/ckanext-agls/commit/db08e0f61948136ea72fcd49c8d0249c9aa0e9e4) by Sergey Motornyuk).
- Add option to update freq ([99963b3](https://github.com/DataShades/ckanext-agls/commit/99963b3d427c7b2cd877e76327cb43e599444882) by Sergey Motornyuk).
- Add tasmanian government ([1820e05](https://github.com/DataShades/ckanext-agls/commit/1820e05cde8c251b2ecd7beb162a6380165fb67e) by root).
- Add gazetteer API. ([6296e85](https://github.com/DataShades/ckanext-agls/commit/6296e857ecac9d81c739cd3a1b1cd8f749829911) by Alex Sadleir).
- Add markup for redirect analytics ([0bd6ee1](https://github.com/DataShades/ckanext-agls/commit/0bd6ee1b2399851e0589449653a9e7859223ba1e) by Alex Sadleir).
- Add annually update period ([c07d20d](https://github.com/DataShades/ckanext-agls/commit/c07d20d80a5f0086406b571c447abcd7a041b1ea) by root).
- add vcard ([38c9102](https://github.com/DataShades/ckanext-agls/commit/38c9102cc69e11e02ee2449f8946f25d6f637dff) by Alex Sadleir).
- add ckan patch enhancements ([26a11a2](https://github.com/DataShades/ckanext-agls/commit/26a11a2fc7ed279223f3df8b9699a6811b1e2d57) by Alex Sadleir).
- add fields of research/geospatial topics input/output ([5596e8f](https://github.com/DataShades/ckanext-agls/commit/5596e8f0592c52da8087505316d85dbb889aae88) by Alex Sadleir).
- add fields of research/geospatial topics ([4015752](https://github.com/DataShades/ckanext-agls/commit/401575209bb0fc3cd44bdcb62650644ca6ee889c) by Alex Sadleir).
- Add additional fields for organisation: telephone/email/homepage/jurisdiction ([7bf7b5a](https://github.com/DataShades/ckanext-agls/commit/7bf7b5a417fff2cc5ce783ac36299a1bfe0d0574) by Alex Sadleir).

### Fixed

- fix fontawesome icons call ([59b8143](https://github.com/DataShades/ckanext-agls/commit/59b81432a5d4a64bebbde5debb9cb5fa867f0c20) by Yan Rudenko).
- Fix vocabulary creation ([ee33653](https://github.com/DataShades/ckanext-agls/commit/ee3365371142901b92775bd7877bc434f149329d) by Sergey Motornyuk).
- fixed datapicker and added /data to api paths ([93e16ff](https://github.com/DataShades/ckanext-agls/commit/93e16ff100fb2bb5a832c2f7255ea22d9ebd4066) by Sergey Motornyuk).
- fix null org ([19444d8](https://github.com/DataShades/ckanext-agls/commit/19444d8d6b1d444b8e3eeb67f5cf398f1f6cede1) by root).
- fix error 500 when dataset has no owner org ([cfe38b4](https://github.com/DataShades/ckanext-agls/commit/cfe38b4c26e927cfc0dfedae57ac2c6c9a64791c) by root).
- fix error 500 ([403fd54](https://github.com/DataShades/ckanext-agls/commit/403fd54ad779c14854e842e498cf60df312ca493) by root).
- Fix data.spatial unescaped ([43ec76f](https://github.com/DataShades/ckanext-agls/commit/43ec76f708529bef688dbd1f841050f681ae6816) by root).
- fix harvest source title ([08db677](https://github.com/DataShades/ckanext-agls/commit/08db6777384fafb857ea79e7b45f38700140a220) by Alex Sadleir).
- fix org error on first creation of dataset ([23eb11e](https://github.com/DataShades/ckanext-agls/commit/23eb11e130643b950763c0381ffc266aafdf7e77) by Alex Sadleir).
- fixes ([b92f93b](https://github.com/DataShades/ckanext-agls/commit/b92f93bd0356050db9626126eec9fd67c9a7c3d0) by Alex Sadleir).
- fix tags ([dacc197](https://github.com/DataShades/ckanext-agls/commit/dacc1975ac87f3594a8587d80990010f1e922573) by Alex Sadleir).
- Fix licence and python namespace ([560bb2f](https://github.com/DataShades/ckanext-agls/commit/560bb2fa05eb958d152e6c4abb7920015ebb0e49) by Alex Sadleir).

### Changed

- Change update frequency to a dropdown list based on ANZLIC ([38234a7](https://github.com/DataShades/ckanext-agls/commit/38234a797818eca658590f82102d3a24cb09a5fd) by Alex Sadleir).

### Removed

- remove block resource_item_explore ([5346c2b](https://github.com/DataShades/ckanext-agls/commit/5346c2b18fa495e9389b572dbf76cea554442502) by Serhii Sviezhentsev).
- remove block package_info ([cb7efe1](https://github.com/DataShades/ckanext-agls/commit/cb7efe18b4d1c4e79a51e394d7786ecd85ec8b2e) by Serhii Sviezhentsev).
- Remove local Gazetteer DB and add site specific customisations to templates ([a347ae6](https://github.com/DataShades/ckanext-agls/commit/a347ae68847639113766bf163c05cd2e77ddd472) by Alex Sadleir).
- Remove source field which is now available in CKAN 2.2 ([534c1e3](https://github.com/DataShades/ckanext-agls/commit/534c1e3fb365810d2d278113f77ea25d2b417e1b) by root).
- remove last active user ([d6a0571](https://github.com/DataShades/ckanext-agls/commit/d6a05712aba9740f2d96c9a273edd40aa757c077) by root).

