import os, sys
import argparse

result={}
dns=["8.8.8.8","8.8.4.4","208.67.222.222","208.67.220.220","209.244.0.3","209.244.0.4","4.2.2.1","4.2.2.2","4.2.2.3","4.2.2.4","8.26.56.26","8.20.247.20","77.88.8.8","77.88.8.1"]
dnscnt=len(dns)
domains=[]


if __name__ == '__main__':
    parser=argparse.ArgumentParser(
        prog='python3 iplookup.py',
        description="Lootup a IPs with using some DNS servers.",
        epilog='(c) 2022.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i','--input-file-name',type=str,default='hosts',help="The input filename with a domains (default: hosts).",dest="domains")
    group.add_argument('-d','--domains',type=str,nargs='+',help="The list of the domains.",dest="domains")
    parser.add_argument('-o','--output-file-name',type=str,default='results',help="The name of a results file (default: results).",dest="ofilename")
    namespace=parser.parse_args()
    domains=namespace.domains
    ofilename=namespace.ofilename
    toolbar_width=len(dns)
    if not isinstance(domains, list):
        tmp_dns=""
        with open(domains,'rt') as ifile:
            for line in ifile:
                tmp_dns="%s %s"%(tmp_dns,line.replace('\n',''))
        domains=tmp_dns.replace(',',' ').split()
    for ditm in range(0,len(domains)):
        result[domains[ditm]]=[]
        sys.stdout.write("Searchin IP's for %s (%s DNS using) [%s]" % (domains[ditm],dnscnt," " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))
        for itm in dns:
            sys.stdout.write("#")
            sys.stdout.flush()
            out=os.popen("dig +short @{} {}".format(itm,domains[ditm])).read().split("\n")
            for i in out:
                if i not in result[domains[ditm]] and ''!=i:
                    result[domains[ditm]].append(i)
        sys.stdout.write("\n")
    if 0!=len(result):
        tmp_res=list(result.keys())
#        tmp_res.sort()
        with open(ofilename,'wt') as ofile:
            for itm in tmp_res:
                ofile.write("%s:\n"%itm)
                if []!=result[itm]:
                    for ip in result[itm]:
                        ofile.write("\t%s\n"%ip)
                else:
                    ofile.write("\tno IP found\n")
                ofile.write("\n")
