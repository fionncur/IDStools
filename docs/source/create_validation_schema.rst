##########################
 create_validation_schema
##########################

create validation schema using data dictionary validation attributes

*********************************
 Syntax create_validation_schema
*********************************

    .. command-output:: create_validation_schema -h


*************************
 Example create_db_entry
*************************

    .. code-block:: bash
        
        $ create_validation_schema -i core_profiles 
        # Schema File for IDS Validation Tool (create_validation_schema)
        # 1) in YAML format, comments starting with "#" and blank lines are allowed.
        # 2) 1st level lists IDS name, 2nd one is for path_doc and 3rd is for validation rule
        #
        # IDS validation schema is listed as below, also default schemas in Cerberus can be used. The schema is presumed
        # in the form of "A:B", where A is name of rule, B is in type of boolean or float. Regarding the rules having B
        # as "false", an error will be reported in case the validation fails, otherwise ignored with "true".
        #        A:               B
        #        ids_nan:         true/false
        #        ids_inf:         true/false
        #        ids_le:          float
        #        ids_ge:          float
        #        ids_lt:          float
        #        ids_gt:          float
        #        ids_psi_like:    true/false
        #        ids_b0_like:     true/false
        #        ids_dodpsi_like: true/false
        #        ids_q_like:      true/false
        #        ids_ip_like:     true/false
        #        ids_dPdpsi_like: true/false
        #        ids_dim:         true/false
        #        ids_bool:        true/false
        #        ids_eq:          float/int
        #        ids_cocos:       int
        #
        # *) The validation rules "ids_nan" and "ids_inf" are default so that the validation scripts as "idschk" and
        core_profiles:
            profiles_1d(itime)/grid/rho_tor_norm(:):
                empty: false
                ids_dim: false
            profiles_1d(itime)/grid/rho_tor(:):
                empty: false
                ids_dim: false
            profiles_1d(itime)/grid/rho_pol_norm(:):
                empty: false
                ids_dim: false
            profiles_1d(itime)/grid/psi(:):
                empty: false
                ids_dim: false
            profiles_1d(itime)/grid/volume(:):
                empty: false
                ids_dim: false
            profiles_1d(itime)/grid/area(:):
                empty: false
                ids_dim: false
