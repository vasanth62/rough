
from collections import OrderedDict


class Table():
    def __init__(self, size):
        self.size = size
        pass

    def size(self):
        ''' Return the size allocated '''
        return self.size

    def create_specs(self, count):
        ''' Create count number of unique specs and return a list of identifiers '''
        ''' Only match-table '''
        pass

    def get_spec(self, resource_id):
        ''' Return the spec used for APIs from the id'''
        pass

    def ent_add(self, target=None, params=None):
        ''' Add the entry into the table by calling thrift apis and return a unique id'''
        pass

    def verify_pkt(self, resource_id, pkt):
        ''' Verify that the pkt parameters conform to the expected transformations '''
        pass

class MatTable(Table):
    def __init__(self, size, resource_tbls, fn_map):
        super(MatTable, self).__init__(size)

        parameter_map = {}

        parameter_map['Match'] = 'match_spec'
        if 'Action' in resource_tbls:
            if resource_tbls['Action']['ref_type'] == 'DIRECT':
                parameter_map['Action'] = 'action_spec'
            else:
                parameter_map['Action'] = 'mbr'
        if 'Selector' in resource_tbls:
            parameter_map['Selector'] = 'grp'
        if 'Meter' in resource_tbls:
            if resource_tbls['Action']['ref_type'] == 'DIRECT':
                parameter_map['Action'] = 'meter_spec'
            
        self.parameter_map = parameter_map
        self.fn_map = fn_map

    def get_resources_needed(self, action_func):
        return self.fn_map[action_func]['resources']

    def create_specs(self, count):
        ip_dsts = ['%d.%d.%d.%d' % (x/(256*256*256), x/(256*256), x/256, x%256) for x in xrange(count)]
        ip_dst_masks = ["255.255.255.255" for _ xrange(count)]

        match_specs = []
        for ip_dst, ip_dst_mask in zip(ip_dsts, ip_dst_masks):
            if self.match_type == 'EXM':
                match_spec = bfd_test_match_tbl_match_spec_t(ip_dst)
            else:
                match_spec = bfd_test_match_tbl_match_spec_t(ip_dst, ip_dst_mask)
            match_specs.append(match_spec)
        return match_specs

    def get_spec(self, resource_id):
        ''' Return the spec used for APIs from the id'''
        return resource_id

    def ent_add(self, action_func=None, target=None, params=None):
        ''' Add the entry into the table by calling thrift apis '''
        dev_tgt = DevTarget_t(target['dev_id'], target['pipe_id'])
        fn_params = {
                     'sess_hdl' = target['sess_hdl']
                     'dev_tgt' = dev_tgt
                    }

        for ptype, spec in params.items():
            fn_params[self.parameter_map[ptype]] = spec

        # Based on the action func, call the right api
        entry_hdl = self.fn_map[action_func]['add'](**fn_params)
        # entry_hdl = self.client.match_tbl_table_add_with_tcp_sport_modify(**fn_params)
        return entry_hdl

    def verify_pkt(self, resource_id, pkt):
        ''' Verify that the pkt parameters conform to the expected transformations '''
        pass


class ActionTable(Table):
    def __init__(self, size, resource_tbls, fn_map):
        super(ActionTable, self).__init__(size)
        parameter_map = {}

        if 'Meter' in resource_tbls:
            if resource_tbls['Action']['ref_type'] == 'INDIRECT':
                parameter_map['Action'] = 'meter_idx'
        if 'Stats' in resource_tbls:
            if resource_tbls['Action']['ref_type'] == 'INDIRECT':
                parameter_map['Action'] = 'stat_idx'
            
        self.parameter_map = parameter_map
        self.fn_map = fn_map

    def get_resources_needed(self, action_func):
        return self.fn_map[action_func]['resources']

    def get_spec(self, resource_id):
        ''' Return the spec used for APIs from the id'''
        if self.ref_type == 'INDIRECT':
            return self.action_map[resource_id]["mbr_hdl"]

        return resource_id

    def ent_add(self, action_func=None, target=None, params=None):
        ''' Add the entry into the table by calling thrift apis '''
         # If it is a direct action, then just create the spec
         # In case of indirect action, add the entry by calling thrift
        action_param = (random.randint(0, 65536), 2)
        if action_func == 'tcp_sport_modify':
            action_spec = bfd_test_tcp_sport_modify_action_spec_t(*action_param)
        elif action_func == 'tcp_dport_modify':
            action_spec = bfd_test_tcp_sport_modify_action_spec_t(*action_param)
        elif action_func == 'tcp_ipsa_modify':
            action_spec = bfd_test_tcp_sport_modify_action_spec_t(*action_param)
        elif action_func == 'tcp_ipda_modify':
            action_spec = bfd_test_tcp_sport_modify_action_spec_t(*action_param)
        else:
            assert 0

        self.action_map[action_spec]["param"] = action_param
        if self.ref_type == 'INDIRECT':
            dev_tgt = DevTarget_t(target['dev_id'], target['pipe_id'])
            fn_params = {
                         'sess_hdl' = target['sess_hdl']
                         'dev_tgt' = dev_tgt
                        }

            for ptype, spec in params.items():
                fn_params[self.parameter_map[ptype]] = spec

            mbr_hdl = self.fn_map[action_func]['add'](**fn_params)
            self.action_map[action_spec]["mbr_hdl"] = mbr_hdl
        return action_spec

    def verify_pkt(self, resource_id, pkt):
        ''' Verify that the pkt parameters conform to the expected transformations '''
        pass

class BFTest():
    ''' Bf-drivers test helper class'''

    def __init__(self, sess_hdl, dev_id, match_tbl, resource_tbls, action_fns):
        ''' Input is a dictionary of one match and associated tables '''
        self.match_tbl = match_tbl
        self.resources = resource_tbls
        self.sess_hdl = sess_hdl
        self.dev_id = dev_id

        self.modified_entries = []

        self.resource_ids = OrderedDict() 
        for resource_tbl in resource_tbls:
            self.resource_ids[resource_tbl] = OrderedDict()
            for action_func in action_fns:
                self.resource_ids[resource_tbl][action_func] = OrderedDict()



    def add_resource_entry(self, resource_tbl, action_func, resource_params={}, resource_record={}):
        # Figure out the resources needed to add an entry to this resource
        # resources_needed is a list of table types from which a resource is needed
        resources_needed = resource_tbl.get_resources_needed(action_func)
        target = {
                  "sess_hdl" : self.sess_hdl,
                  "dev_id" : self.dev_id,
                  "pipe_id" : hex_to_i16(0xFFFF)
                 }
        resource_record["dev_id"] = self.dev_id
        resource_record["pipe_id"] = hex_to_i16(0xFFFF)

        for resource_name in resources_needed:
            tbl = self.get_resource_tbl_by_name(resource_name)
            resource_id = random.choice(self.resource_ids[tbl][action_func].keys())
            resource_params[resource_name] = tbl.get_spec(resource_id)
            resource_record[resource_name] = resource_id
        resource_id = resource_tbl.ent_add(action_func= action_func, target=target, params = resource_params)
        self.resource_ids[resource_tbl][action_func][resource_id] = resource_record
        return resource_id

    def config_scale_test(self):
        # Add entries in each of the resource tables and gather their
        # result to add into the match tables

        # The tables in self.resources should be arranged based on their 
        # dependency. i.e. The first tables should not have any dependencies 

        for resource in self.resources:
            for i in xrange(resource.size()):
                action_func = random.choice(self.actions)
                self.add_resource_entry(resource, action_func)

        # Now add match entries
        match_ids = self.match_tbl.create_spec(match_tbl.size())

        for match_id in match_ids:
            match_spec = self.match_tbl.get_spec(match_id)

            mat_ent_hdl = self.add_resource_entry(self.match_tbl, action_func,
                    resource_params = {'Match' : self.match_tbl.get_spec(match_id)}, 
                    resource_record = {'match_id' : match_id})

            self.modified_entries.append(mat_ent_hdl)


    def verify(self):
        return
        ''' Verification function. All the entries that have been modified
            should be in a modification list and the verify function
            will verify all those entries in all the associated tables
        '''
        # Now send packets for a handful of entries
        for mat_ent_hdl in random.sample(self.modified_entries, 100):
            pkt_params = self.default_pkt_params()
            # exp_pkt_params = self.default_pkt_params()

            # Figure out the pkt params needed for this particular entry
            self.match_tbl.update_pkt_params(self.match_entries[mat_ent_hdl]["match_id"],
                    pkt_params)

            exp_port = None
            pkt_count = 1 
            # Figure out the expected pkt and the port
            for resource in self.resources.values():
                resource_id = self.match_entries[mat_ent_hdl][resource.name()]
                _exp_port, _pkt_count = resource.update_exp_port(resource_id)
                if _exp_port is not None:
                    exp_port = _exp_port
                pkt_count = max(pkt_count, _pkt_count) 
                # exp_port, pkt_count = resource.update_exp_pkt_params(resource_id, exp_pkt_params)

            pkt_to_send = self.create_pkt(pkt_params)
            exp_pkt = self.create_pkt(exp_pkt_params)

            for _ in xrange(pkt_count):
                self.send_packet(send_port, pkt_to_send)
                rcv_pkt = self.receive_packet(exp_port)

                # Verify that the received pkt matches all the required parameters
                for resource in self.resources.values():
                    resource_id = self.match_entries[mat_ent_hdl][resource.name()]
                    resource.verify_pkt(resource_id, rcv_pkt)
                

    def run_scale_test(self):
        config_scale_test()
        verify()
