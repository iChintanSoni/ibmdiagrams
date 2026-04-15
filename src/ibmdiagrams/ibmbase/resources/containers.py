# @file containers.py
#
# Copyright contributors to the ibmdiagrams project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Container resource definitions for IBM Cloud."""

import pandas as pd

CONTAINER_RESOURCES = {
    # Container Registry
    'ibm_cr_namespace': pd.DataFrame(),
    'ibm_cr_retention_policy': pd.DataFrame(),

    # Kubernetes Service
    'ibm_container_addons': pd.DataFrame(),
    'ibm_container_alb': pd.DataFrame(),
    'ibm_container_alb_cert': pd.DataFrame(),
    'ibm_container_alb_create': pd.DataFrame(),
    'ibm_container_api_key_reset': pd.DataFrame(),
    'ibm_container_bind_service': pd.DataFrame(),
    'ibm_container_cluster': pd.DataFrame(),
    'ibm_container_cluster_feature': pd.DataFrame(),
    'ibm_container_dedicated_host': pd.DataFrame(),
    'ibm_container_dedicated_host_pool': pd.DataFrame(),
    'ibm_container_nlb_dns': pd.DataFrame(),
    'ibm_container_storage_attachment': pd.DataFrame(),
    'ibm_container_vpc_alb': pd.DataFrame(),
    'ibm_container_vpc_alb_create': pd.DataFrame(),
    'ibm_container_vpc_cluster': pd.DataFrame(),
    'ibm_container_vpc_worker': pd.DataFrame(),
    'ibm_container_vpc_worker_pool': pd.DataFrame(),
    'ibm_container_worker_pool_zone_attachment': pd.DataFrame(),

    # Satellite
    'ibm_satellite_cluster': pd.DataFrame(),
    'ibm_satellite_cluster_worker_pool': pd.DataFrame(),
    'ibm_satellite_cluster_worker_pool_zone_attachment': pd.DataFrame(),
    'ibm_satellite_endpoint': pd.DataFrame(),
    'ibm_satellite_host': pd.DataFrame(),
    'ibm_satellite_link': pd.DataFrame(),
    'ibm_satellite_location': pd.DataFrame(),
    'ibm_satellite_location_nlb_dns': pd.DataFrame(),
}

# Made with Bob
