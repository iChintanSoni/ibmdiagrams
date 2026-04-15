# @file storage.py
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

"""Storage resource definitions for IBM Cloud."""

import pandas as pd

STORAGE_RESOURCES = {
    # Classic Infrastructure - Storage
    'ibm_object_storage_account': pd.DataFrame(),
    'ibm_storage_block': pd.DataFrame(),
    'ibm_storage_evault': pd.DataFrame(),
    'ibm_storage_file': pd.DataFrame(),

    # Object Storage
    'ibm_cos_bucket': pd.DataFrame(),
    'ibm_cos_bucket_object': pd.DataFrame(),
    'ibm_cos_replication': pd.DataFrame(),

    # VPC Infrastructure - Storage
    'ibm_is_backup_policy': pd.DataFrame(),
    'ibm_is_backup_policy_plan': pd.DataFrame(),
    'ibm_is_volume': pd.DataFrame(),

    # Power Systems - Storage
    'ibm_pi_volume': pd.DataFrame(),
    'ibm_pi_volume_attach': pd.DataFrame(),
    'ibm_pi_volume_group': pd.DataFrame(),
    'ibm_pi_volume_group_action': pd.DataFrame(),
    'ibm_pi_volume_onboarding': pd.DataFrame(),
}

# Made with Bob
