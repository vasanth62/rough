
import os
import json
import itertools

#The ordering in the tbls and stuff should be matching

action_funcs = ['tcp_sport_modify', 'tcp_dport_modify', 'ipsa_modify', 'ipda_modify']

match_info = {
                'tcam' : {
                            'size' : 4096,
                            'name' : 'match_tbl'
                         },
                'exm' : {
                            'size' : 8192,
                            'name' : 'match_tbl'
                        }
            }


action_info = {
                'size' : 2048,
                'name' : 'selector_profile',
                'action_funcs' : action_funcs[:]
               }

selector_info = None
idle_info = None
stat_info = None
meter_info = None
stful_info = None

tbls = { 'Match' : (0, match_info),
         'Action':(1, action_info),
         'Selector':(2, selector_info),
         'Idle':(3, idle_info),
         'Stat':(4, stat_info),
         'Meter':(5, meter_info),
         'Stful':(6, stful_info)
        }

def get_tbl_index(tbl):
    idx, info = tbls[tbl]
    return idx

stuff = [
      ["tcam", "exm"], #Match
      ["direct", "indirect"], #Action
#      ["imm", "direct", "indirect"], #Action
      ["off", "indirect"], #Selector
      ["off", "direct"], #Idle
      ["off", "direct", "indirect"], #Stat
      ["off", "direct", "indirect"], #Meter
      ["off", "direct", "indirect"] #Stful
      ]

count = 0
for x in itertools.product(*stuff):
    # With selector action can only be indirect
    try:
        if x[get_tbl_index('Selector')] == 'indirect' and x[get_tbl_index('Action')] != 'indirect':
            continue

        # Stateful, meters and select are mutually exclusive
        meter_bus = (x[get_tbl_index('Selector')], x[get_tbl_index('Meter')], x[get_tbl_index('Stful')])
        if (len(meter_bus) - meter_bus.count('off')) > 1:
            continue

        # Currently meter and idletime are exclusive
        idle_bus = (x[get_tbl_index('Idle')], x[get_tbl_index('Meter')])
        if (len(idle_bus) - idle_bus.count('off')) > 1:
            continue

        if x.count('indirect') > 2:
            continue
    except:
        pass

    print x
    count += 1
    continue

    inc_str = ''
    resource_map = {}

    match_type = x[get_tbl_index('Match')]
    match_size = match_info[match_type]['size']
    match_map = { 
                  'size' : match_size,
                  'match_type' : match_type,
                  'name' : match_info[match_type]['name']
                }

    inc_str += '#define MATCH_' + match_type.upper() + '\n'
    inc_str += '#define MATCH_COUNT %d\n' % match_size


    resource_map['Match'] = match_map

    for tbl in tbls.keys():
        if tbl == 'Match':
            continue
        idx, info = tbls[tbl]
        if info is None:
            continue
        if x[idx] != 'off':
            if x[idx] == 'direct':
                tbl_size = match_size
            else:
                tbl_size = info['size']
            tbl_map = {
                        'size' : tbl_size,
                        'ref_type' : x[idx].upper(),
                        'action_funcs' : info['action_funcs'],
                        'name' : info['name']
                      }
            resource_map[tbl] = tbl_map

            inc_str += '#define %s_%s\n' % (tbl.upper(), x[idx].upper())
            inc_str += '#define %s_COUNT %d\n' % (tbl.upper(), tbl_size)

    resource_map['Action_funcs'] = action_funcs

    print inc_str
    with open('../../programs/single_device/bfd_test/p4features.h', 'w') as include_file:
        include_file.write(inc_str)

    # Compile the target
    cmd  = 'touch programs/bfd_test/bfd_test.p4'
    ret = os.system(cmd)
    cmd  = './compile.sh --p4 bfd_test'
    ret = os.system(cmd)

    with open('bfd-test-info.json', 'w') as testfile:
        json.dump(resource_map, testfile, indent=2)

    print json.dumps(resource_map, indent = 2)
    raw_input('Compile completed')

    count += 1

print count

