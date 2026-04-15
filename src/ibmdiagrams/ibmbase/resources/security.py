# @file security.py
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

"""Security resource definitions for IBM Cloud."""

import pandas as pd

SECURITY_RESOURCES = {
    # Classic Infrastructure - Security
    'ibm_security_group': pd.DataFrame(),
    'ibm_security_group_rule': pd.DataFrame(),
    'ibm_ssl_certificate': pd.DataFrame(),

    # Certificate Manager
    'ibm_certificate_manager_import': pd.DataFrame(),
    'ibm_certificate_manager_order': pd.DataFrame(),

    # Context Based Restrictions
    'ibm_cbr_rule': pd.DataFrame(),
    'ibm_cbr_zone': pd.DataFrame(),

    # Hyper Protect Crypto Services
    'ibm_hpcs': pd.DataFrame(),
    'ibm_hpcs_key_template': pd.DataFrame(),
    'ibm_hpcs_keystore': pd.DataFrame(),
    'ibm_hpcs_managed_key': pd.DataFrame(),
    'ibm_hpcs_vault': pd.DataFrame(),

    # Identity & Access Management (IAM)
    'ibm_api_key': pd.DataFrame(),
    'ibm_iam_access_group': pd.DataFrame(),
    'ibm_iam_access_group_account_settings': pd.DataFrame(),
    'ibm_iam_access_group_dynamic_rule': pd.DataFrame(),
    'ibm_iam_access_group_members': pd.DataFrame(),
    'ibm_iam_access_group_policy': pd.DataFrame(),
    'ibm_iam_account_settings': pd.DataFrame(),
    'ibm_iam_authorization_policy': pd.DataFrame(),
    'ibm_iam_authorization_policy_detach': pd.DataFrame(),
    'ibm_iam_custom_role': pd.DataFrame(),
    'ibm_iam_service-api-key': pd.DataFrame(),
    'ibm_iam_service_id': pd.DataFrame(),
    'ibm_iam_service_policy': pd.DataFrame(),
    'ibm_iam_trusted_profile': pd.DataFrame(),
    'ibm_iam_trusted_profile_claim_rule': pd.DataFrame(),
    'ibm_iam_trusted_profile_link': pd.DataFrame(),
    'ibm_iam_trusted_profile_policy': pd.DataFrame(),
    'ibm_iam_user_invite': pd.DataFrame(),
    'ibm_iam_user_policy': pd.DataFrame(),
    'ibm_iam_user_settings': pd.DataFrame(),

    # Key Management Service
    'ibm_kms_instance_policies': pd.DataFrame(),
    'ibm_kms_key': pd.DataFrame(),
    'ibm_kms_key_alias': pd.DataFrame(),
    'ibm_kms_key_policies': pd.DataFrame(),
    'ibm_kms_key_rings': pd.DataFrame(),
    'ibm_kms_key_with_policy_overrides': pd.DataFrame(),
    'ibm_kp_key': pd.DataFrame(),

    # Secrets Manager
    'ibm_secrets_manager_secret': pd.DataFrame(),
    'ibm_sm_arbitrary_secret': pd.DataFrame(),
    'ibm_sm_en_registration': pd.DataFrame(),
    'ibm_sm_iam_credentials_configuration': pd.DataFrame(),
    'ibm_sm_iam_credentials_secret': pd.DataFrame(),
    'ibm_sm_imported_certificate': pd.DataFrame(),
    'ibm_sm_kv_secret': pd.DataFrame(),
    'ibm_sm_private_certificate': pd.DataFrame(),
    'ibm_sm_private_certificate_configuration_action_set_signed': pd.DataFrame(),
    'ibm_sm_private_certificate_configuration_action_sign_csr': pd.DataFrame(),
    'ibm_sm_private_certificate_configuration_intermediate_ca': pd.DataFrame(),
    'ibm_sm_private_certificate_configuration_root_ca': pd.DataFrame(),
    'ibm_sm_private_certificate_configuration_template': pd.DataFrame(),
    'ibm_sm_public_certificate': pd.DataFrame(),
    'ibm_sm_public_certificate_action_validate_manual_dns': pd.DataFrame(),
    'ibm_sm_public_certificate_configuration_ca_lets_encrypt': pd.DataFrame(),
    'ibm_sm_public_certificate_configuration_dns_cis': pd.DataFrame(),
    'ibm_sm_public_certificate_configuration_dns_classic_infrastructure': pd.DataFrame(),
    'ibm_sm_secret_group': pd.DataFrame(),
    'ibm_sm_service_credentials_secret': pd.DataFrame(),
    'ibm_sm_username_password_secret': pd.DataFrame(),

    # Security and Compliance Center
    'ibm_scc_account_settings': pd.DataFrame(),
    'ibm_scc_posture_collector': pd.DataFrame(),
    'ibm_scc_posture_credential': pd.DataFrame(),
    'ibm_scc_posture_profile_impact': pd.DataFrame(),
    'ibm_scc_posture_scan_initiate_validation': pd.DataFrame(),
    'ibm_scc_posture_scope': pd.DataFrame(),
    'ibm_scc_rule': pd.DataFrame(),
    'ibm_scc_rule_attachment': pd.DataFrame(),
    'ibm_scc_si_note': pd.DataFrame(),
    'ibm_scc_si_occurrence': pd.DataFrame(),
    'ibm_scc_template': pd.DataFrame(),
    'ibm_scc_template_attachment': pd.DataFrame(),
}

# Made with Bob
