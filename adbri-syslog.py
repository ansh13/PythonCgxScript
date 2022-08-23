import cloudgenix
from cloudgenix import API, jd,jdout
from cloudgenix import jdout
from cloudgenix import Put

from cloudgenix import Get, interactive

# sdk = API(controller='https://api.hood.cloudgenix.com', ssl_verify=False)
sdk1 = API(controller='https://api.elcapitan.cloudgenix.com', ssl_verify=False)
# sdk2 = API()

sdk1.interactive.login(email='ansmittal@paloaltonetworks.com', password='Enterpriseconnect@13')
# sdk1.interactive.login()
# cgx_session = cloudgenix.API(controller='https://api.elcapitan.cloudgenix.com', ssl_verify=False)
# cgx_session.interactive.login(email='ansmittal@paloaltonetworks.com', password = 'Enterpriseconnect@13')

#rsp = jdout(sdk1.get.elements(tenant_id=10000,element_id=16240676735620113))
#print(rsp)

#sid = "15831977877090072"
#eid = "16159507549250064"
#snmp_agent_id = "16439668848610227"
tid = "10000"
#sysid = "16406254283320087"

for n in range(2):

    elements = sdk1.get.elements(tenant_id=tid)
    #jd(elements)
    sites = sdk1.get.sites(tenant_id=tid)
    #jd(sites)
    elementload = elements.cgx_content
    siteload = sites.cgx_content
    eid = elementload['items'][n]['id']
    sid = elementload['items'][n]['site_id']
    #print(elementload['items'][n]['name'])
    #print(elementload['items'][n]['id'])
    #print(elementload['items'][n]['site_id'])
    #print(siteload['items'][0]['id'])
    #print(siteload['items'][n]['name'])
    resp = sdk1.get.syslogservers(site_id=sid, element_id=eid, tenant_id=tid)
    #print(resp)
    #syslogidload = resp.cgx_content
    #syslogid = syslogidload['items'][0]['id']
    #print(syslogid)
    
    
    if resp.cgx_status:

        sysload = resp.cgx_content.get("items",None)
        #print(sysload)
        #print (type(sysload))
        #if resp.cgx_content:
        if len(sysload) == 0:
            print('No Syslog Found '+ siteload['items'][n]['name'])
        else:    
           resp = sdk1.get.syslogservers(site_id=sid, element_id=eid, tenant_id=tid)
           syslogidload = resp.cgx_content
           syslogid = syslogidload['items'][0]['id']
           sysload[0]["syslog_profile_id"] = "16439841341150044"
           sysload[0]['server_port'] = None
           #print(sysload[0])
           #sysload1['items'][0]["syslog_profile_id"] = "16406254283320087"
           #print(sysload)
           #sysload["syslog_profile_id"] = name
           resp = sdk1.put.syslogservers(element_id=eid, site_id=sid, syslogserver_id= syslogid, data=sysload[0])
           if resp.cgx_status:
                  print("Syslog Updated for "+ siteload['items'][n]['name'] )
           else:
                print("ERR: Could not PUT Syslog")
                cloudgenix.jd_detailed(resp)
    else:
         print("ERR: Could not GET Syslog")
         cloudgenix.jd_detailed(resp)