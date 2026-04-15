# @file compute.py
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

"""Compute resource definitions for IBM Cloud."""

import pandas as pd

COMPUTE_RESOURCES = {
    # Classic Infrastructure - Compute
    'ibm_compute_autoscale_group': pd.DataFrame(),
    'ibm_compute_autoscale_policy': pd.DataFrame(),
    'ibm_compute_bare_metal': pd.DataFrame(),
    'ibm_compute_dedicated_host': pd.DataFrame(),
    'ibm_compute_monitor': pd.DataFrame(),
    'ibm_compute_placement_group': pd.DataFrame(),
    'ibm_compute_provisioning_hook': pd.DataFrame(),
    'ibm_compute_reserved_capacity': pd.DataFrame(),
    'ibm_compute_ssh_key': pd.DataFrame(),
    'ibm_compute_ssl_certificate': pd.DataFrame(),
    'ibm_compute_user': pd.DataFrame(),
    'ibm_compute_vm_instance': pd.DataFrame(),

    # VPC Infrastructure - Compute
    'ibm_is_bare_metal_server': pd.DataFrame(),
    'ibm_is_bare_metal_server_action': pd.DataFrame(),
    'ibm_is_bare_metal_server_disk': pd.DataFrame(),
    'ibm_is_bare_metal_server_network_interface': pd.DataFrame(),
    'ibm_is_bare_metal_server_network_interface_allow_float': pd.DataFrame(),
    'ibm_is_bare_metal_server_network_interface_floating_ip': pd.DataFrame(),
    'ibm_is_dedicated_host': pd.DataFrame(),
    'ibm_is_dedicated_host_disk_management': pd.DataFrame(),
    'ibm_is_dedicated_host_group': pd.DataFrame(),
    'ibm_is_image': pd.DataFrame(),
    'ibm_is_instance': pd.DataFrame(),
    'ibm_is_instance_action': pd.DataFrame(),
    'ibm_is_instance_disk_management': pd.DataFrame(),
    'ibm_is_instance_group': pd.DataFrame(),
    'ibm_is_instance_group_manager': pd.DataFrame(),
    'ibm_is_instance_group_manager_action': pd.DataFrame(),
    'ibm_is_instance_group_manager_policy': pd.DataFrame(),
    'ibm_is_instance_group_membership': pd.DataFrame(),
    'ibm_is_instance_network_interface': pd.DataFrame(),
    'ibm_is_instance_network_interface_floating_ip': pd.DataFrame(),
    'ibm_is_instance_template': pd.DataFrame(),
    'ibm_is_instance_volume_attachment': pd.DataFrame(),
    'ibm_is_placement_group': pd.DataFrame(),
    'ibm_is_ssh_key': pd.DataFrame(),
    'ibm_is_snapshot': pd.DataFrame(),

    # Power Systems - Compute
    'ibm_pi_capture': pd.DataFrame(),
    'ibm_pi_console_language': pd.DataFrame(),
    'ibm_pi_image': pd.DataFrame(),
    'ibm_pi_image_export': pd.DataFrame(),
    'ibm_pi_instance': pd.DataFrame(),
    'ibm_pi_instance_action': pd.DataFrame(),
    'ibm_pi_key': pd.DataFrame(),
    'ibm_pi_placement_group': pd.DataFrame(),
    'ibm_pi_shared_processor_pool': pd.DataFrame(),
    'ibm_pi_snapshot': pd.DataFrame(),
    'ibm_pi_spp_placement_group': pd.DataFrame(),
}

# Made with Bob
