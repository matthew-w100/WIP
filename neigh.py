import sys
import argparse
import xml.etree.ElementTree as ET

def getKey(item):
    unitport = item[0][0].split(':',1)
    rval = []
    for x in unitport:
        rval.append(int(x))
    return rval

def getParams():
    parser = argparse.ArgumentParser(description='show lldp neighbours', prog='neigh.py')
    parser.add_argument('portlist', type=str, default='all', nargs='?', help='list of ports in usual Extreme format (no spaces)')
    parser.add_argument('-m', '--match', help='string to match output lines on')

    args = parser.parse_args()
    return args

def main():
    args = getParams()

    cmd = 'show lldp ports {0} neighbors detail'.format(args.portlist)

    try:
        xmlReply = exsh.clicmd(cmd, xml=True)
    except RuntimeError:
        print '"{0}" cli command failed to run'.format(cmd)
    else:
        validXml = '<blah>' + xmlReply + '</blah>'
        root = ET.fromstring(validXml)

        lldpNbr = {}

        for nbr in root.iter('lldpPortNbrInfoShort'):
            port = nbr.find('port').text
            nbrIndex = nbr.find('nbrIndex').text
            nbrAttrib = {}
            for child in nbr:
                if child.tag not in ('port', 'nbrIndex'):
                   nbrAttrib[child.tag] = child.text
            lldpNbr[(port, nbrIndex)] = nbrAttrib

        for tlv in root.iter('lldpPortNbrTlvInfo'):
            port = tlv.find('port').text
            nbrIndex = tlv.find('nbrIndex').text
            k, v = tlv.find('tlvASCIIDecode').text.split(':', 1)
            k = k.strip(' -')
            v = v.strip().strip('"')
            lldpNbr[(port, nbrIndex)][k] = v
    
        fmt = '{:4} {:>30.30} {:>15.15} {:>22.22} {:>4}'
        print fmt.format('Port', 'Rem Sys Name', 'Rem Port ID', 'Rem Port Desc', 'Age')
        print '==============================================================================='
        for (port, idx), vals in sorted(lldpNbr.items(), key=getKey):
            line = fmt.format(port, vals.get('System Name',''), vals['nbrPortID'], vals.get('Port Description',''), vals['age'])
            if args.match:
                if args.match in line:
                    print line
            else:
                print line

if __name__  == '__main__':
    try:
        main()
    except SystemExit:
        pass
