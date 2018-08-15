import sys
import argparse
import xml.etree.ElementTree as ET
from sets import Set

def getParams():
    parser = argparse.ArgumentParser(description='strip all vlans from port(s)', prog='stripvlans.py')
    parser.add_argument('portlist', type=str, help='list of ports in usual Extreme format (no spaces)')
    parser.add_argument('-f', '--force', action='store_true', help='actually perform the removal, default is a dry-run')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress informational messages')

    args = parser.parse_args()
    return args

def main():
    args = getParams()

    cmd = 'show ports {0} information detail'.format(args.portlist)

    try:
        xmlReply = exsh.clicmd(cmd, xml=True)
    except RuntimeError:
        print '"{0}" cli command failed to run'.format(cmd)
        return

    validXml = '<blah>' + xmlReply + '</blah>'
    root = ET.fromstring(validXml)

    portVlan = {}
    vlans = {}

    for branch in root.iter('show_ports_info_detail_vlans'):
        port = branch.find('port').text
        tagStatus = branch.find('tagStatus').text
        vlanId = branch.find('vlanId').text
        vlanName = branch.find('vlanName').text
        if not port in portVlan:
            portVlan[port] = Set([(vlanName,vlanId,tagStatus)])
        else:
            portVlan[port].add((vlanName,vlanId,tagStatus))
        vlans[vlanName] = vlanId

    to_remove_tagged = {}
    to_remove_untagged = {}
    for port in portVlan:
        for vlan,vlanId,tagStatus in portVlan[port]:
            if tagStatus == '1':
                if not vlan in to_remove_tagged:
                    to_remove_tagged[vlan] = Set([port])
                else:
                    to_remove_tagged[vlan].add(port)
            elif tagStatus == '0':
                if not vlan in to_remove_untagged:
                    to_remove_untagged[vlan] = Set([port])
                else:
                    to_remove_untagged[vlan].add(port)
            else:
                print "WARNING: unknown tagStatus {0} for port {1} vlan {2}".format(tagStatus, port, vlan)


    cmds_to_remove = []
    cmds_to_add = []
    for vlan in sorted(to_remove_tagged):
        cmd_r = 'configure vlan {0} delete ports {1}'.format(vlan, ','.join(to_remove_tagged[vlan]))
        cmds_to_remove.append(cmd_r)
        cmd_a = 'configure vlan {0} add ports {1} tagged'.format(vlan, ','.join(to_remove_tagged[vlan]))
        cmds_to_add.append(cmd_a)
    for vlan in sorted(to_remove_untagged):
        cmd_r = 'configure vlan {0} delete ports {1}'.format(vlan, ','.join(to_remove_untagged[vlan]))
        cmds_to_remove.append(cmd_r)
        cmd_a = 'configure vlan {0} add ports {1} untagged'.format(vlan, ','.join(to_remove_untagged[vlan]))
        cmds_to_add.append(cmd_a)

    for cmd in cmds_to_remove:
        if args.force:
            try:
                resp = exsh.clicmd(cmd, capture=True)
            except:
                print '"{0}" cli command failed to run'.format(cmd)
            else:
                if resp:
                    print resp
        else:
            print "DRY-RUN:", cmd
    if not args.force:
        print "To execute these deletes, run sript again with '-f'/'--force'"

    if args.force and not args.quiet:
        print """\
Commands to reinstate
====================="""
        for cmd in cmds_to_add:
            print cmd

if __name__  == '__main__':
    try:
        main()
    except SystemExit:
        pass
