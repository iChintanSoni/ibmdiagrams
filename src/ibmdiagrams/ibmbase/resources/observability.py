# @file observability.py
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

"""Observability and other miscellaneous resource definitions for IBM Cloud."""

import pandas as pd

OBSERVABILITY_RESOURCES = {
    # Activity Tracker API
    'ibm_atracker_route': pd.DataFrame(),
    'ibm_atracker_settings': pd.DataFrame(),
    'ibm_atracker_target': pd.DataFrame(),

    # Observability
    'ibm_ob_logging': pd.DataFrame(),
    'ibm_ob_monitoring': pd.DataFrame(),

    # App Configuration
    'ibm_app_config_collection': pd.DataFrame(),
    'ibm_app_config_environment': pd.DataFrame(),
    'ibm_app_config_feature': pd.DataFrame(),
    'ibm_app_config_property': pd.DataFrame(),
    'ibm_app_config_segment': pd.DataFrame(),
    'ibm_app_config_snapshot': pd.DataFrame(),

    # AppID Management
    'ibm_appid_action_url': pd.DataFrame(),
    'ibm_appid_apm': pd.DataFrame(),
    'ibm_appid_application': pd.DataFrame(),
    'ibm_appid_application_roles': pd.DataFrame(),
    'ibm_appid_application_scopes': pd.DataFrame(),
    'ibm_appid_audit_status': pd.DataFrame(),
    'ibm_appid_cloud_directory_template': pd.DataFrame(),
    'ibm_appid_cloud_directory_user': pd.DataFrame(),
    'ibm_appid_idp_cloud_directory': pd.DataFrame(),
    'ibm_appid_idp_custom': pd.DataFrame(),
    'ibm_appid_idp_facebook': pd.DataFrame(),
    'ibm_appid_idp_google': pd.DataFrame(),
    'ibm_appid_idp_saml': pd.DataFrame(),
    'ibm_appid_languages': pd.DataFrame(),
    'ibm_appid_mfa': pd.DataFrame(),
    'ibm_appid_mfa_channel': pd.DataFrame(),
    'ibm_appid_password_regex': pd.DataFrame(),
    'ibm_appid_redirect_urls': pd.DataFrame(),
    'ibm_appid_role': pd.DataFrame(),
    'ibm_appid_theme_color': pd.DataFrame(),
    'ibm_appid_theme_text': pd.DataFrame(),
    'ibm_appid_token_config': pd.DataFrame(),
    'ibm_appid_user_roles': pd.DataFrame(),

    # Catalog Management
    'ibm_cm_catalog': pd.DataFrame(),
    'ibm_cm_object': pd.DataFrame(),
    'ibm_cm_offering': pd.DataFrame(),
    'ibm_cm_offering_instance': pd.DataFrame(),
    'ibm_cm_version': pd.DataFrame(),

    # Cloud Foundry
    'ibm_app': pd.DataFrame(),
    'ibm_app_domain_private': pd.DataFrame(),
    'ibm_app_domain_shared': pd.DataFrame(),
    'ibm_app_route': pd.DataFrame(),
    'ibm_org': pd.DataFrame(),
    'ibm_service_instance': pd.DataFrame(),
    'ibm_service_key': pd.DataFrame(),
    'ibm_space': pd.DataFrame(),

    # Cloud Shell
    'ibm_cloud_shell_account_settings': pd.DataFrame(),

    # Continuous Delivery
    'ibm_cd_tekton_pipeline': pd.DataFrame(),
    'ibm_cd_tekton_pipeline_definition': pd.DataFrame(),
    'ibm_cd_tekton_pipeline_property': pd.DataFrame(),
    'ibm_cd_tekton_pipeline_trigger': pd.DataFrame(),
    'ibm_cd_toolchain': pd.DataFrame(),
    'ibm_cd_toolchain_tool_appconfig': pd.DataFrame(),
    'ibm_cd_toolchain_tool_artifactory': pd.DataFrame(),
    'ibm_cd_toolchain_tool_bitbucketgit': pd.DataFrame(),
    'ibm_cd_toolchain_tool_custom': pd.DataFrame(),
    'ibm_cd_toolchain_tool_devopsinsights': pd.DataFrame(),
    'ibm_cd_toolchain_tool_githubconsolidated': pd.DataFrame(),
    'ibm_cd_toolchain_tool_gitlab': pd.DataFrame(),
    'ibm_cd_toolchain_tool_hashicorpvault': pd.DataFrame(),
    'ibm_cd_toolchain_tool_hostedgit': pd.DataFrame(),
    'ibm_cd_toolchain_tool_jenkins': pd.DataFrame(),
    'ibm_cd_toolchain_tool_jira': pd.DataFrame(),
    'ibm_cd_toolchain_tool_keyprotect': pd.DataFrame(),
    'ibm_cd_toolchain_tool_nexus': pd.DataFrame(),
    'ibm_cd_toolchain_tool_pagerduty': pd.DataFrame(),
    'ibm_cd_toolchain_tool_pipeline': pd.DataFrame(),
    'ibm_cd_toolchain_tool_privateworker': pd.DataFrame(),
    'ibm_cd_toolchain_tool_saucelabs': pd.DataFrame(),
    'ibm_cd_toolchain_tool_secretsmanager': pd.DataFrame(),
    'ibm_cd_toolchain_tool_securitycompliance': pd.DataFrame(),
    'ibm_cd_toolchain_tool_slack': pd.DataFrame(),
    'ibm_cd_toolchain_tool_sonarqube': pd.DataFrame(),

    # Enterprise Management
    'ibm_enterprise': pd.DataFrame(),
    'ibm_enterprise_account': pd.DataFrame(),
    'ibm_enterprise_account_group': pd.DataFrame(),

    # Event Notifications
    'ibm_en_destination': pd.DataFrame(),
    'ibm_en_destination_android': pd.DataFrame(),
    'ibm_en_destination_ce': pd.DataFrame(),
    'ibm_en_destination_cf': pd.DataFrame(),
    'ibm_en_destination_chrome': pd.DataFrame(),
    'ibm_en_integration_cos': pd.DataFrame(),
    'ibm_en_destination_firefox': pd.DataFrame(),
    'ibm_en_destination_huawei': pd.DataFrame(),
    'ibm_en_destination_ios': pd.DataFrame(),
    'ibm_en_destination_mstreams': pd.DataFrame(),
    'ibm_en_destination_pagerduty': pd.DataFrame(),
    'ibm_en_destination_safari': pd.DataFrame(),
    'ibm_en_destination_slack': pd.DataFrame(),
    'ibm_en_destination_webhook': pd.DataFrame(),
    'ibm_en_ibmsource': pd.DataFrame(),
    'ibm_en_integration': pd.DataFrame(),
    'ibm_en_source': pd.DataFrame(),
    'ibm_en_subscription': pd.DataFrame(),
    'ibm_en_subscription_android': pd.DataFrame(),
    'ibm_en_subscription_ce': pd.DataFrame(),
    'ibm_en_subscription_cf': pd.DataFrame(),
    'ibm_en_subscription_chrome': pd.DataFrame(),
    'ibm_en_subscription_email': pd.DataFrame(),
    'ibm_en_subscription_firefox': pd.DataFrame(),
    'ibm_en_subscription_ios': pd.DataFrame(),
    'ibm_en_subscription_mstreams': pd.DataFrame(),
    'ibm_en_subscription_pagerduty': pd.DataFrame(),
    'ibm_en_subscription_safari': pd.DataFrame(),
    'ibm_en_subscription_slack': pd.DataFrame(),
    'ibm_en_subscription_sms': pd.DataFrame(),
    'ibm_en_subscription_sn': pd.DataFrame(),
    'ibm_en_subscription_webhook': pd.DataFrame(),
    'ibm_en_topic': pd.DataFrame(),

    # Event Streams
    'ibm_event_streams_schema': pd.DataFrame(),
    'ibm_event_streams_topic': pd.DataFrame(),

    # Functions
    'ibm_function_action': pd.DataFrame(),
    'ibm_function_namespace': pd.DataFrame(),
    'ibm_function_package': pd.DataFrame(),
    'ibm_function_rule': pd.DataFrame(),
    'ibm_function_trigger': pd.DataFrame(),

    # Global Tagging
    'ibm_resource_tag': pd.DataFrame(),

    # Push Notifications
    'ibm_pn_application_chrome': pd.DataFrame(),

    # Resource Management
    'ibm_resource_group': pd.DataFrame(),
    'ibm_resource_instance': pd.DataFrame(),
    'ibm_resource_key': pd.DataFrame(),

    # Schematics
    'ibm_schematics_action': pd.DataFrame(),
    'ibm_schematics_inventory': pd.DataFrame(),
    'ibm_schematics_job': pd.DataFrame(),
    'ibm_schematics_resource_query': pd.DataFrame(),
    'ibm_schematics_workspace': pd.DataFrame(),
}

# Made with Bob
