# @file network.py
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

"""Network resource definitions for IBM Cloud."""

import pandas as pd

NETWORK_RESOURCES = {
    # Classic Infrastructure - Network
    'ibm_cdn': pd.DataFrame(),
    'ibm_dns_domain': pd.DataFrame(),
    'ibm_dns_domain_registration_nameservers': pd.DataFrame(),
    'ibm_dns_record': pd.DataFrame(),
    'ibm_dns_reverse_record': pd.DataFrame(),
    'ibm_dns_secondary': pd.DataFrame(),
    'ibm_firewall': pd.DataFrame(),
    'ibm_firewall_policy': pd.DataFrame(),
    'ibm_hardware_firewall_shared': pd.DataFrame(),
    'ibm_ipsec_vpn': pd.DataFrame(),
    'ibm_lb': pd.DataFrame(),
    'ibm_lb_service': pd.DataFrame(),
    'ibm_lb_service_group': pd.DataFrame(),
    'ibm_lb_vpx': pd.DataFrame(),
    'ibm_lb_vpx_ha': pd.DataFrame(),
    'ibm_lb_vpx_service': pd.DataFrame(),
    'ibm_lb_vpx_vip': pd.DataFrame(),
    'ibm_lbaas': pd.DataFrame(),
    'ibm_lbaas_health_monitor': pd.DataFrame(),
    'ibm_lbaas_server_instance_attachment': pd.DataFrame(),
    'ibm_multi_vlan_firewall': pd.DataFrame(),
    'ibm_network_gateway': pd.DataFrame(),
    'ibm_network_gateway_vlan_association': pd.DataFrame(),
    'ibm_network_interface_sg_attachment': pd.DataFrame(),
    'ibm_network_public_ip': pd.DataFrame(),
    'ibm_network_vlan': pd.DataFrame(),
    'ibm_network_vlan_spanning': pd.DataFrame(),
    'ibm_subnet': pd.DataFrame(),

    # DNS Services
    'ibm_dns_custom_resolver': pd.DataFrame(),
    'ibm_dns_custom_resolver_forwarding_rule': pd.DataFrame(),
    'ibm_dns_custom_resolver_location': pd.DataFrame(),
    'ibm_dns_custom_resolver_secondary_zone': pd.DataFrame(),
    'ibm_dns_glb': pd.DataFrame(),
    'ibm_dns_glb_monitor': pd.DataFrame(),
    'ibm_dns_glb_pool': pd.DataFrame(),
    'ibm_dns_glb_permitted_network': pd.DataFrame(),
    'ibm_dns_resource_record': pd.DataFrame(),
    'ibm_dns_zone': pd.DataFrame(),

    # Direct Link
    'ibm_dl_gateway': pd.DataFrame(),
    'ibm_dl_provider_gateway': pd.DataFrame(),
    'ibm_dl_route_report': pd.DataFrame(),
    'ibm_dl_virtual_connection': pd.DataFrame(),

    # Internet Services (CIS)
    'ibm_cis': pd.DataFrame(),
    'ibm_cis_alert': pd.DataFrame(),
    'ibm_cis_cache_settings': pd.DataFrame(),
    'ibm_cis_certificate_order': pd.DataFrame(),
    'ibm_cis_certificate_upload': pd.DataFrame(),
    'ibm_cis_custom_page': pd.DataFrame(),
    'ibm_cis_dns_record': pd.DataFrame(),
    'ibm_cis_dns_records_import': pd.DataFrame(),
    'ibm_cis_domain': pd.DataFrame(),
    'ibm_cis_domain_settings': pd.DataFrame(),
    'ibm_cis_edge_functions_action': pd.DataFrame(),
    'ibm_cis_edge_functions_trigger': pd.DataFrame(),
    'ibm_cis_filter': pd.DataFrame(),
    'ibm_cis_firewall': pd.DataFrame(),
    'ibm_cis_firewall_rules': pd.DataFrame(),
    'ibm_cis_global_load_balancer': pd.DataFrame(),
    'ibm_cis_healthcheck': pd.DataFrame(),
    'ibm_cis_logpush_jobs': pd.DataFrame(),
    'ibm_cis_mtlss': pd.DataFrame(),
    'ibm_cis_mtls_apps': pd.DataFrame(),
    'ibm_cis_origin_auth': pd.DataFrame(),
    'ibm_cis_origin_pool': pd.DataFrame(),
    'ibm_cis_page_rule': pd.DataFrame(),
    'ibm_cis_range_app': pd.DataFrame(),
    'ibm_cis_rate_limit': pd.DataFrame(),
    'ibm_cis_routing': pd.DataFrame(),
    'ibm_cis_tls_settings': pd.DataFrame(),
    'ibm_cis_waf_group': pd.DataFrame(),
    'ibm_cis_waf_package': pd.DataFrame(),
    'ibm_cis_waf_rule': pd.DataFrame(),
    'ibm_cis_waf_webhook': pd.DataFrame(),

    # Transit Gateway
    'ibm_connection_prefix_filter': pd.DataFrame(),
    'ibm_tg_connection': pd.DataFrame(),
    'ibm_tg_gateway': pd.DataFrame(),
    'ibm_tg_route_report': pd.DataFrame(),

    # VPC Infrastructure - Network
    'ibm_is_floating_ip': pd.DataFrame(),
    'ibm_is_flow_log': pd.DataFrame(),
    'ibm_is_ike_policy': pd.DataFrame(),
    'ibm_is_ipsec_policy': pd.DataFrame(),
    'ibm_is_lb': pd.DataFrame(),
    'ibm_is_lb_listener': pd.DataFrame(),
    'ibm_is_lb_listener_policy': pd.DataFrame(),
    'ibm_is_lb_listener_policy_rule': pd.DataFrame(),
    'ibm_is_lb_pool': pd.DataFrame(),
    'ibm_is_lb_pool_member': pd.DataFrame(),
    'ibm_is_network_acl': pd.DataFrame(),
    'ibm_is_network_acl_rule': pd.DataFrame(),
    'ibm_is_public_gateway': pd.DataFrame(),
    'ibm_is_security_group': pd.DataFrame(),
    'ibm_is_security_group_network_interface_attachment': pd.DataFrame(),
    'ibm_is_security_group_rule': pd.DataFrame(),
    'ibm_is_security_group_target': pd.DataFrame(),
    'ibm_is_subnet': pd.DataFrame(),
    'ibm_is_subnet_network_acl_attachment': pd.DataFrame(),
    'ibm_is_subnet_public_gateway_attachment': pd.DataFrame(),
    'ibm_is_subnet_reserved_ip': pd.DataFrame(),
    'ibm_is_subnet_routing_table_attachment': pd.DataFrame(),
    'ibm_is_virtual_endpoint_gateway': pd.DataFrame(),
    'ibm_is_virtual_endpoint_gateway_ip': pd.DataFrame(),
    'ibm_is_vpc': pd.DataFrame(),
    'ibm_is_vpc_address_prefix': pd.DataFrame(),
    'ibm_is_vpc_route': pd.DataFrame(),
    'ibm_is_vpc_routing_table': pd.DataFrame(),
    'ibm_is_vpc_routing_table_route': pd.DataFrame(),
    'ibm_is_vpn_gateway': pd.DataFrame(),
    'ibm_is_vpn_gateway_connection': pd.DataFrame(),
    'ibm_is_vpn_server': pd.DataFrame(),
    'ibm_is_vpn_server_client': pd.DataFrame(),
    'ibm_is_vpn_server_route': pd.DataFrame(),

    # Power Systems - Network
    'ibm_pi_cloud_connection': pd.DataFrame(),
    'ibm_pi_cloud_connection_network_attach': pd.DataFrame(),
    'ibm_pi_dhcp': pd.DataFrame(),
    'ibm_pi_network': pd.DataFrame(),
    'ibm_pi_network_port': pd.DataFrame(),
    'ibm_pi_network_port_attach': pd.DataFrame(),
    'ibm_pi_vpn_connection': pd.DataFrame(),
    'ibm_pi_vpn_ike_policy': pd.DataFrame(),
    'ibm_pi_vpn_ipsec_policy': pd.DataFrame(),
}

# Made with Bob
